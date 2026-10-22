#!/usr/bin/env python3
"""Builds and runs the C++ examples published in the lessons. Used by the Toolchains workflow.

Lessons mark their code blocks with HTML comments, which GitHub does not show:

    <!-- example: NAME -->              the next ```cpp block is a complete program;
    <!-- example: NAME source=PATH -->  ... and it must equal the file PATH (relative to the lesson);
    <!-- example: NAME exit=N -->        ... and it must exit with code N instead of 0;
    <!-- output: NAME -->               the next ```text block is the exact output of example NAME;
    <!-- input: NAME -->                the next ```text block is fed to example NAME on standard input, in
                                        a separate run of the same built program; the output blocks that
                                        follow it (up to the next input block of NAME) are the exact output
                                        of that run. An example with input blocks needs an input block
                                        before its first output block, and an output block after each input;
    <!-- broken: NAME at=LINE[:COLUMN] [errors=N] error=REGEX -->
                                        the next ```cpp block is a complete program with deliberate
                                        mistakes: it must FAIL TO COMPILE, and the first compiler
                                        error in main.cpp must be at LINE (and COLUMN), with a message
                                        matching REGEX (a Python regular expression); with errors=N,
                                        main.cpp must get exactly N errors;
    <!-- broken: NAME stage=link error=REGEX -->
                                        the next ```cpp block compiles, but must FAIL TO LINK: main.cpp
                                        compiles without errors (its object file is created), the link
                                        step fails ("linker command failed", no executable), and the
                                        build output matches REGEX somewhere (linker messages differ
                                        per platform, so REGEX may list alternatives);
    <!-- fragment -->                   the next ```cpp block is deliberately incomplete: not built.

Checks:
  * every ```cpp block in a lesson is marked (Module 0 lessons predate the markers and are
    skipped unless marked; their project is checked by the other steps of the workflow);
  * every example has at least one output block, and every output block has an example;
  * marked blocks are ASCII only, and the Polish lesson (X.md) and the English one (X.en.md)
    contain the same marked blocks, with the same markers, in the same order;
  * each example and each broken program is built as main.cpp of the lesson 0.5 project (its
    CMakeLists.txt) with CMake, Ninja and the given compiler. Examples are built with warnings
    as errors; broken programs with the project's own flags only, exactly as a learner builds
    them, so that the checked messages are the ones the learner sees (some messages are
    warnings on one system and errors on another).
    The configure step must succeed and report Clang 22 or newer, so that a broken environment
    is never mistaken for the expected compile error.
  * an example must build, exit with 0 (or its exit=N), print nothing to stderr, and print exactly the expected
    output (Windows line ends ignored). It is built once and run once per input block (or once with an
    empty standard input when it has none), each run within --timeout seconds. Only the program's own
    standard output is compared: typed input never appears in it, because nothing is typed.
    Each run may print at most OUTPUT_LIMIT bytes to stdout, and separately to stderr, counted as the
    program writes them (before Windows line ends are normalised). The checker keeps no more than
    that while the program runs, and stops the program as soon as one stream goes over the limit;
  * a broken program must fail to build because of compiler errors in main.cpp, as described
    by its marker; with stage=link, it must compile and then fail in the linker, as above.
    Its whole build output is printed, to compare the messages across systems.

The lessons are never modified: everything is built in copies under build/lesson-examples.

Run from the repository root, with the official compiler:
    python3 tests/toolchains/lesson_examples.py --cxx /usr/bin/clang++-22 [--make-program /usr/bin/ninja]
Check that the checker itself detects mistakes (in a temporary folder):
    python3 tests/toolchains/lesson_examples.py --self-test --cxx /usr/bin/clang++-22
"""

import argparse
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

MARKER = re.compile(r'^<!-- (?:(example|output|input|broken): ([a-z0-9_]+)(.*?)|(fragment)) -->$')
SOURCE = re.compile(r'^(?: source=(\S+))?(?: exit=(\d+))?$')
BROKEN = re.compile(r'^(?: stage=(link))?(?: at=(\d+)(?::(\d+))?)?(?: errors=(\d+))? error=(.+)$')
FENCE = re.compile(r'^```(\S*)$')
# A compiler error in main.cpp: GNU style (main.cpp:4:35: error: ...) or MSVC style (main.cpp(4,35): error: ...).
ERROR = re.compile(r'main\.cpp(?::(\d+):(\d+):|\((\d+),(\d+)\):) error: (.*)')
PROJECT = pathlib.Path('course/module_00_tooling/lesson_05_first_program/CMakeLists.txt')
WARNINGS = '-Wall -Wextra -pedantic-errors -Werror'
# The most one run of an example may print to stdout, and separately to stderr. Exactly this many bytes is allowed.
OUTPUT_LIMIT = 65536
# Messages and the log show at most this many characters of a program's output.
SHOWN_LIMIT = 1000

errors = []


def fail(message):
    errors.append(message)
    print(f'FAIL {message}')


def blocks(path):
    """Returns the marked code blocks of a lesson as (kind, name, attributes, language, text, line),
    and the line numbers of unmarked ```cpp blocks."""
    lines = path.read_text(encoding='utf-8').splitlines()
    found, unmarked, marker, i = [], [], None, 0
    while i < len(lines):
        line = lines[i]
        match = MARKER.match(line)
        fence = FENCE.match(line)
        if match:
            if marker:
                fail(f'{path}:{marker[3]}: marker not followed by a code block')
            kind = match[1] or match[4]
            attributes = match[3] or ''
            pattern = BROKEN if kind == 'broken' else SOURCE if kind == 'example' else re.compile('^$')
            parsed = pattern.match(attributes)
            # A compile-stage broken program needs at=; a link-stage one has no line in main.cpp to point to.
            if not parsed or (kind == 'broken' and bool(parsed[1]) == bool(parsed[2] or parsed[4])):
                fail(f'{path}:{i + 1}: cannot read the {kind} marker: {line}')
            marker = (kind, match[2], attributes, i + 1)
        elif fence:
            start, language, body = i + 1, fence[1], []
            i += 1
            while i < len(lines) and lines[i] != '```':
                body.append(lines[i])
                i += 1
            text = '\n'.join(body) + '\n'
            if marker:
                kind, name, attributes = marker[:3]
                expected = 'text' if kind in ('output', 'input') else 'cpp'
                if language != expected:
                    fail(f'{path}:{start}: {kind} marker on a ```{language} block, expected ```{expected}')
                found.append((kind, name, attributes, language, text, start))
            elif language == 'cpp':
                unmarked.append(start)
            marker = None
        elif line.strip() and marker:
            fail(f'{path}:{marker[3]}: marker not followed by a code block')
            marker = None
        i += 1
    return found, unmarked


def check_lesson(path, found):
    """Checks one lesson's markers; returns its examples, their runs and the broken programs.
    A run is (standard input, or None for none, [expected outputs])."""
    examples, broken = {}, {}
    for kind, name, attributes, _, text, line in found:
        if not text.isascii():
            fail(f'{path}:{line}: non-ASCII text in a marked block')
        if kind in ('example', 'broken'):
            if name in examples or name in broken:
                fail(f'{path}:{line}: program {name} defined twice')
        if kind == 'example':
            source = SOURCE.match(attributes)
            examples[name] = (text, int(source[2]) if source and source[2] else 0)
            if source and source[1]:
                original = (path.parent / source[1]).read_text(encoding='utf-8')
                if text != original:
                    fail(f'{path}:{line}: example {name} differs from {source[1]}')
                else:
                    print(f'ok   {path.name}: example {name} equals {source[1]}')
        elif kind == 'broken':
            expectation = BROKEN.match(attributes)
            if expectation:
                broken[name] = (text, expectation)
    runs = {}
    for kind, name, _, _, text, line in found:
        if kind not in ('output', 'input'):
            continue
        if name not in examples:
            fail(f'{path}:{line}: {kind} {name} has no example')
            continue
        name_runs = runs.setdefault(name, [])
        if kind == 'input':
            name_runs.append((text, []))
        else:
            if not name_runs:
                name_runs.append((None, []))
            name_runs[-1][1].append(text)
    for name in examples:
        name_runs = runs.get(name, [])
        if not any(outputs for _, outputs in name_runs):
            fail(f'{path}: example {name} has no output block')
        elif any(data is not None for data, _ in name_runs) and name_runs[0][0] is None:
            fail(f'{path}: example {name}: an output block comes before its first input block')
        elif any(not outputs for _, outputs in name_runs):
            fail(f'{path}: example {name}: an input block has no output block after it')
    return examples, runs, broken


def run(command):
    return subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')


def build(lesson, name, code, args, flags=WARNINGS):
    """Configures and builds a copy of the project with CODE as main.cpp.
    Returns (build directory, build result), or None when configuring failed."""
    work = pathlib.Path('build/lesson-examples') / lesson / name
    shutil.rmtree(work, ignore_errors=True)
    src = work / 'src'
    src.mkdir(parents=True)
    shutil.copy(PROJECT, src / 'CMakeLists.txt')
    # newline='\n': the same bytes on every system, as in the lesson.
    (src / 'main.cpp').write_text(code, encoding='ascii', newline='\n')
    configure = [args.cmake, '-S', str(src), '-B', str(work / 'build'), '-G', 'Ninja',
                 '-DCMAKE_BUILD_TYPE=Debug', f'-DCMAKE_CXX_COMPILER={args.cxx}', f'-DCMAKE_CXX_FLAGS={flags}']
    if args.make_program:
        configure.append(f'-DCMAKE_MAKE_PROGRAM={args.make_program}')
    result = run(configure)
    if result.returncode != 0:
        fail(f'{lesson}: {name}: configure failed (an environment problem, not a lesson result)\n'
             f'{result.stdout}{result.stderr}')
        return None
    compiler = re.search(r'The CXX compiler identification is (.*)', result.stdout)
    version = re.match(r'Clang (\d+)\.', compiler[1]) if compiler else None
    if not version or int(version[1]) < 22:
        fail(f'{lesson}: {name}: configured with {compiler[1] if compiler else "an unknown compiler"}')
        return None
    return work / 'build', run([args.cmake, '--build', str(work / 'build')])


def executable(build_dir):
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    return build_dir / (target + ('.exe' if sys.platform == 'win32' else ''))


def run_program(exe, data, timeout):
    """Runs EXE once, with DATA on standard input (None: an empty standard input).
    Returns (exit code, stdout bytes, stderr bytes, whether it timed out, the streams that went over OUTPUT_LIMIT).

    Each stream is read by its own thread while the program runs, so a program that fills one pipe never
    waits for the checker to read the other (the way subprocess.communicate reads on Windows). A thread
    keeps at most OUTPUT_LIMIT + 1 bytes: one byte more than allowed is proof enough, so it stops the
    program at once instead of collecting everything it would print."""
    # A pipe, not a terminal: the input is never echoed, so stdout is the program's output alone.
    # Without an input block the program gets an empty standard input, never the checker's own.
    with subprocess.Popen([str(exe)], stdin=subprocess.DEVNULL if data is None else subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        kept = {'stdout': bytearray(), 'stderr': bytearray()}
        over_limit = []

        def collect(stream, pipe):
            while chunk := pipe.read1(OUTPUT_LIMIT):
                kept[stream] += chunk[:OUTPUT_LIMIT + 1 - len(kept[stream])]
                if len(kept[stream]) > OUTPUT_LIMIT:
                    over_limit.append(stream)
                    process.kill()  # safe even if the program has just ended by itself
                    return

        def feed():
            # Then closed, so the program sees the end of its input after the last line.
            try:
                process.stdin.write(data.encode('ascii'))
                process.stdin.close()
            except OSError:  # the program ended without reading all of its input
                try:
                    process.stdin.close()
                except OSError:
                    pass

        threads = [threading.Thread(target=collect, args=('stdout', process.stdout)),
                   threading.Thread(target=collect, args=('stderr', process.stderr))]
        if data is not None:
            threads.append(threading.Thread(target=feed))
        for thread in threads:
            thread.start()
        timed_out = False
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            process.kill()
            process.wait()
        # The program has ended, so its pipes are closed and every thread finishes.
        for thread in threads:
            thread.join()
    return process.returncode, bytes(kept['stdout']), bytes(kept['stderr']), timed_out, over_limit


def shown(text):
    """TEXT for a message: its repr, cut after SHOWN_LIMIT characters."""
    if len(text) <= SHOWN_LIMIT:
        return repr(text)
    return f'{text[:SHOWN_LIMIT]!r} and {len(text) - SHOWN_LIMIT} more characters, not shown'


def check_example(lesson, name, code, exit_code, runs, args):
    built = build(lesson, name, code, args)
    if not built:
        return
    build_dir, result = built
    if result.returncode != 0:
        fail(f'{lesson}: example {name}: build failed\n{result.stdout}{result.stderr}')
        return
    exe = executable(build_dir)
    # The same program for every run: built once above, never rebuilt between inputs.
    for number, (data, expected) in enumerate(runs or [(None, [])], 1):
        label = f'example {name}' if data is None else f'example {name} (input {number} of {len(runs)})'
        returncode, stdout, stderr, timed_out, over_limit = run_program(exe, data, args.timeout)
        if over_limit:
            for stream in over_limit:
                fail(f'{lesson}: {label}: {stream} exceeded the {OUTPUT_LIMIT}-byte limit, so the program was stopped')
            continue
        if timed_out:
            fail(f'{lesson}: {label}: did not finish within {args.timeout} s')
            continue
        # Decoded and normalised only now, within the limit: the limit counts the bytes as printed.
        out = stdout.decode('ascii', errors='replace').replace('\r\n', '\n')
        problems = []
        if returncode != exit_code:
            problems.append(f'exit code {returncode}, expected {exit_code}')
        if stderr:
            problems.append(f'printed to stderr: {shown(stderr.decode("ascii", errors="replace"))}')
        mismatch = next((text for text in expected if out != text), None)
        if mismatch is not None:
            problems.append(f'output {shown(out)}, expected {shown(mismatch)}')
        if problems:
            for problem in problems:
                fail(f'{lesson}: {label}: {problem}')
            continue
        print(f'ok   {lesson}: {label} builds, runs, exits with {exit_code} '
              f'and prints the expected {len(expected)} output block(s):')
        for line in (data or '').splitlines():
            print(f'       < {line}')
        for line in out[:SHOWN_LIMIT].splitlines():
            print(f'       | {line}')
        if len(out) > SHOWN_LIMIT:
            print(f'       ({len(out) - SHOWN_LIMIT} more characters, not shown)')


def check_broken(lesson, name, code, expectation, args):
    built = build(lesson, name, code, args, flags='')
    if not built:
        return
    build_dir, result = built
    output = result.stdout + result.stderr
    if result.returncode == 0:
        fail(f'{lesson}: broken program {name} builds, but the lesson says it must not')
        return
    found = [(int(m[1] or m[3]), int(m[2] or m[4]), m[5]) for m in ERROR.finditer(output)]
    if expectation[1] == 'link':
        check_link_failure(lesson, name, build_dir, output, found, expectation[5])
        return
    if not found:
        fail(f'{lesson}: broken program {name}: the build failed, but not with a compiler error in main.cpp\n{output}')
        return
    line, column, message = found[0]
    _, want_line, want_column, want_count, want_error = expectation.groups()
    problems = []
    if line != int(want_line) or (want_column and column != int(want_column)):
        problems.append(f'first error at {line}:{column}, expected {want_line}' + (f':{want_column}' if want_column else ''))
    if not re.search(want_error, message):
        problems.append(f'first error says {message!r}, expected a match for {want_error!r}')
    if want_count and len(found) != int(want_count):
        problems.append(f'{len(found)} errors in main.cpp, expected {want_count}')
    if problems:
        fail(f'{lesson}: broken program {name}: ' + '; '.join(problems) + f'\n{output}')
        return
    print(f'ok   {lesson}: broken program {name} fails to compile as described: {len(found)} error(s), '
          f'the first at {line}:{column}: {message}')
    print('     build output:')
    for text in output.splitlines():
        print(f'       | {text}')


def check_link_failure(lesson, name, build_dir, output, compile_errors, want_error):
    """The stage=link checks: compiled, then failed in the linker for the expected reason."""
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    objects = [p for p in build_dir.rglob('main.cpp.o*') if p.suffix in ('.o', '.obj')]
    exe = build_dir / (target + ('.exe' if sys.platform == 'win32' else ''))
    problems = []
    if compile_errors:
        problems.append(f'main.cpp has compiler errors, so the build stopped before linking')
    elif not objects:
        problems.append('no object file for main.cpp, so compiling did not succeed')
    if 'linker command failed' not in output:
        problems.append('the build failed, but not in the linker ("linker command failed" is missing)')
    if exe.exists():
        problems.append(f'the program {exe.name} was created')
    if not re.search(want_error, output, re.MULTILINE):
        problems.append(f'the linker output has no match for {want_error!r}')
    if problems:
        fail(f'{lesson}: broken program {name} (stage=link): ' + '; '.join(problems) + f'\n{output}')
        return
    print(f'ok   {lesson}: broken program {name} compiles ({objects[0].name} created) and fails to link as described')
    print('     build output:')
    for text in output.splitlines():
        print(f'       | {text}')


def check_course(args):
    """Checks every lesson under course/ in the current folder; returns the number of problems."""
    errors.clear()
    lessons = sorted(p for p in pathlib.Path('course').rglob('*.md') if not p.name.endswith('.en.md'))
    checked = 0
    for pl in lessons:
        en = pl.with_name(pl.stem + '.en.md')
        pl_blocks, pl_unmarked = blocks(pl)
        en_blocks, en_unmarked = blocks(en) if en.exists() else ([], [])
        if not pl_blocks and not en_blocks and 'module_00_tooling' in pl.parts:
            continue
        checked += 1
        print(f'=== {pl} and {en.name}')
        if not en.exists():
            fail(f'{pl}: no English version {en.name}')
        for path, unmarked in ((pl, pl_unmarked), (en, en_unmarked)):
            for line in unmarked:
                fail(f'{path}:{line}: ```cpp block without a marker')
        pl_marked = [(kind, name, attributes, text) for kind, name, attributes, _, text, _ in pl_blocks]
        en_marked = [(kind, name, attributes, text) for kind, name, attributes, _, text, _ in en_blocks]
        if pl_marked != en_marked:
            fail(f'{pl}: the marked code blocks differ between {pl.name} and {en.name}')
        else:
            print(f'ok   {len(pl_marked)} marked blocks are identical in {pl.name} and {en.name}')
        examples, runs, broken = check_lesson(pl, pl_blocks)
        if en.exists():
            check_lesson(en, en_blocks)
        fragments = sum(1 for block in pl_blocks if block[0] == 'fragment')
        inputs = sum(1 for block in pl_blocks if block[0] == 'input')
        print(f'     {len(examples)} examples to build and run ({inputs} runs with standard input), '
              f'{len(broken)} broken programs that must not compile, '
              f'{fragments} fragments (deliberately incomplete, not built)')
        for name, (code, exit_code) in examples.items():
            check_example(pl.stem, name, code, exit_code, runs.get(name, []), args)
        for name, (code, expectation) in broken.items():
            check_broken(pl.stem, name, code, expectation, args)
    if checked == 0:
        fail('no lesson contains marked examples')
    print(f'{"PASSED" if not errors else "FAILED"}: {checked} lesson(s), {len(errors)} problem(s)')
    return len(errors)


GOOD = '#include <iostream>\n\nint main() {\n    std::cout << "Hi!\\n";\n}\n'
NO_SEMICOLON = GOOD.replace('\\n";', '\\n"')
RETURN_3 = GOOD.replace('\n}\n', '\n    return 3;\n}\n')
MIAN = GOOD.replace('int main()', 'int mian()').replace('\n}\n', '\n    return 0;\n}\n')
READ_INT = ('#include <iostream>\n\nint main() {\n    int count{0};\n    std::cin >> count;\n'
            '    std::cout << "Count: " << count << "\\n";\n}\n')
READ_TWO = ('#include <iostream>\n\nint main() {\n    int laps{0};\n    double lap_km{0.0};\n'
            '    std::cin >> laps;\n    std::cin >> lap_km;\n    std::cout << "Total: " << laps * lap_km << "\\n";\n}\n')
# Never finishes on its own (the volatile counter keeps the loop from being optimised away).
ENDLESS = '#include <iostream>\n\nint main() {\n    volatile int steps{0};\n    for (;;) {\n        steps = steps + 1;\n    }\n}\n'
# Prints COUNT letters x, with no line end (the same bytes on every system), to stdout or, given 1, to stderr.
PRINT_X = ('#include <iostream>\n\nint main() {\n    int count{0};\n    int to_stderr{0};\n    std::cin >> count >> to_stderr;\n'
           '    for (int i{0}; i < count; ++i) {\n        if (to_stderr == 1) {\n            std::cerr << \'x\';\n'
           '        } else {\n            std::cout << \'x\';\n        }\n    }\n}\n')
# Writes to stderr, then stdout, then stderr again; more than a Windows pipe holds, within the limit.
BOTH_STREAMS = ('#include <iostream>\n\nint main() {\n    for (int round{0}; round < 3; ++round) {\n'
                '        for (int i{0}; i < 30000; ++i) {\n            if (round == 1) {\n                std::cout << \'o\';\n'
                '            } else {\n                std::cerr << \'e\';\n            }\n        }\n    }\n}\n')
# Reads numbers until its input ends; it finishes only if the input is closed after the data.
READ_ALL = ('#include <iostream>\n\nint main() {\n    int value{0};\n    int count{0};\n    while (std::cin >> value) {\n'
            '        count = count + 1;\n    }\n    std::cout << "Values: " << count << "\\n";\n}\n')


def lesson(*parts):
    """A fixture lesson made of (marker, language, code) parts."""
    return ''.join(f'<!-- {marker} -->\n```{language}\n{code}```\n\n' for marker, language, code in parts)


def self_test(args):
    """Runs the checker on small fixture courses; each must give the expected verdict."""
    good = [('example: hi', 'cpp', GOOD), ('output: hi', 'text', 'Hi!\n')]
    semicolon = "broken: no_semicolon at=4 errors=1 error=expected ';'"
    link = 'broken: mian stage=link error=undefined reference to .main\'|undefined symbol: main\\b|"_main", referenced from'
    cases = [
        ('correct examples pass', lesson(*good), None, None),
        ('a wrong expected output is detected',
         lesson(('example: hi', 'cpp', GOOD), ('output: hi', 'text', 'Hello!\n')), None, 'example hi: output'),
        ('an example with exit=3 that returns 3 passes',
         lesson(('example: hi exit=3', 'cpp', RETURN_3), ('output: hi', 'text', 'Hi!\n')), None, None),
        ('an unexpected exit code is detected',
         lesson(('example: hi', 'cpp', RETURN_3), ('output: hi', 'text', 'Hi!\n')), None, 'exit code 3, expected 0'),
        ('a program that fails to link as described passes (stage=link)',
         lesson(*good, (link, 'cpp', MIAN)), None, None),
        ('a stage=link program that fails to compile is detected',
         lesson(*good, (link, 'cpp', NO_SEMICOLON)), None, 'compiler errors, so the build stopped before linking'),
        ('a stage=link program that builds is detected',
         lesson(*good, (link, 'cpp', GOOD)), None, 'builds, but the lesson says it must not'),
        ('a different linker message is detected (stage=link)',
         lesson(*good, ('broken: mian stage=link error=undefined symbol: nothing_like_this', 'cpp', MIAN)),
         None, 'the linker output has no match'),
        ('a broken program that fails as described passes',
         lesson(*good, (semicolon, 'cpp', NO_SEMICOLON)), None, None),
        ('a broken program that suddenly compiles is detected',
         lesson(*good, (semicolon, 'cpp', GOOD)), None, 'builds, but the lesson says it must not'),
        ('a different diagnostic is detected',
         lesson(*good, ("broken: no_semicolon at=4 error=use of undeclared identifier", 'cpp', NO_SEMICOLON)),
         None, 'first error says'),
        ('a diagnostic on another line is detected',
         lesson(*good, ("broken: no_semicolon at=5 error=expected ';'", 'cpp', NO_SEMICOLON)), None, 'first error at'),
        ('a different number of errors is detected',
         lesson(*good, ("broken: no_semicolon at=4 errors=2 error=expected ';'", 'cpp', NO_SEMICOLON)),
         None, 'errors in main.cpp, expected 2'),
        ('different PL and EN code is detected',
         lesson(*good), lesson(('example: hi', 'cpp', GOOD.replace('Hi', 'Hey')), ('output: hi', 'text', 'Hey!\n')),
         'differ between'),
        ('an unmarked cpp block is detected', lesson(*good) + '```cpp\nint main() {}\n```\n', None, 'without a marker'),
        # A missing compiler breaks configuring: that must never pass as the expected compile error.
        ('a broken environment is not taken for the expected error',
         lesson((semicolon, 'cpp', NO_SEMICOLON)), None, 'configure failed (an environment problem'),
        # Standard input (input: blocks).
        ('an example with standard input passes',
         lesson(('example: count', 'cpp', READ_INT), ('input: count', 'text', '5\n'),
                ('output: count', 'text', 'Count: 5\n')), None, None),
        ('two inputs run the same program separately, and both pass',
         lesson(('example: count', 'cpp', READ_INT), ('input: count', 'text', '5\n'), ('output: count', 'text', 'Count: 5\n'),
                ('input: count', 'text', '12\n'), ('output: count', 'text', 'Count: 12\n')), None, None),
        ('input in several lines passes',
         lesson(('example: total', 'cpp', READ_TWO), ('input: total', 'text', '4\n1.25\n'),
                ('output: total', 'text', 'Total: 5\n')), None, None),
        ('a wrong output for the second input is detected',
         lesson(('example: count', 'cpp', READ_INT), ('input: count', 'text', '5\n'), ('output: count', 'text', 'Count: 5\n'),
                ('input: count', 'text', '12\n'), ('output: count', 'text', 'Count: 13\n')),
         None, 'example count (input 2 of 2): output'),
        ('an output block before the first input block is detected',
         lesson(('example: count', 'cpp', READ_INT), ('output: count', 'text', 'Count: 0\n'),
                ('input: count', 'text', '5\n'), ('output: count', 'text', 'Count: 5\n')),
         None, 'an output block comes before its first input block'),
        ('an input block without an output block is detected',
         lesson(('example: count', 'cpp', READ_INT), ('input: count', 'text', '5\n'), ('output: count', 'text', 'Count: 5\n'),
                ('input: count', 'text', '12\n')),
         None, 'an input block has no output block after it'),
        ('an input block without an example is detected',
         lesson(*good, ('input: other', 'text', '5\n')), None, 'input other has no example'),
        ('different PL and EN input is detected',
         lesson(('example: count', 'cpp', READ_INT), ('input: count', 'text', '5\n'), ('output: count', 'text', 'Count: 5\n')),
         lesson(('example: count', 'cpp', READ_INT), ('input: count', 'text', '6\n'), ('output: count', 'text', 'Count: 5\n')),
         'differ between'),
        ('a program that never finishes is stopped and detected',
         lesson(('example: endless', 'cpp', ENDLESS), ('output: endless', 'text', '')), None, 'did not finish within'),
        ('the input is closed after the data, and each run reads only its own input',
         lesson(('example: values', 'cpp', READ_ALL), ('input: values', 'text', '4\n5\n6\n'), ('output: values', 'text', 'Values: 3\n'),
                ('input: values', 'text', '7\n'), ('output: values', 'text', 'Values: 1\n')), None, None),
        # The output limit (the exact boundary is checked by self_test_limits, without line ends).
        ('stdout over the limit is detected, in a short message',
         lesson(('example: flood', 'cpp', PRINT_X), ('input: flood', 'text', '65537 0\n'), ('output: flood', 'text', 'x\n')),
         None, 'stdout exceeded the 65536-byte limit'),
        ('stderr over the limit is detected, in a short message',
         lesson(('example: flood', 'cpp', PRINT_X), ('input: flood', 'text', '65537 1\n'), ('output: flood', 'text', 'x\n')),
         None, 'stderr exceeded the 65536-byte limit'),
        ('a program writing to stderr and stdout in turns runs to its end, in a short message',
         lesson(('example: both', 'cpp', BOTH_STREAMS), ('output: both', 'text', 'o\n')), None, 'printed to stderr'),
        ('a long wrong output is detected, in a short message',
         lesson(('example: flood', 'cpp', PRINT_X), ('input: flood', 'text', '50000 0\n'), ('output: flood', 'text', 'x\n')),
         None, 'more characters, not shown'),
    ]
    project = PROJECT.resolve()
    home = os.getcwd()
    failures = 0
    for title, pl_text, en_text, expected_failure in cases:
        case_args = argparse.Namespace(**vars(args))
        if 'environment' in title:
            case_args.cxx = str(pathlib.Path(tempfile.gettempdir()) / 'no-such-compiler' / 'clang++')
        if 'never finishes' in title:
            case_args.timeout = 3
        with tempfile.TemporaryDirectory() as root:
            os.chdir(root)
            try:
                PROJECT.parent.mkdir(parents=True)
                shutil.copy(project, PROJECT)
                folder = pathlib.Path('course/module_99_self_test')
                folder.mkdir(parents=True)
                (folder / 'lesson.md').write_text(pl_text, encoding='utf-8')
                (folder / 'lesson.en.md').write_text(en_text or pl_text, encoding='utf-8')
                print(f'\n##### self-test: {title}')
                check_course(case_args)
                if expected_failure is None:
                    verdict = not errors
                else:
                    verdict = len(errors) > 0 and any(expected_failure in e for e in errors)
                if 'short message' in title:
                    verdict = verdict and all(len(e) <= 4 * SHOWN_LIMIT for e in errors)
            finally:
                os.chdir(home)
        print(f'##### {"ok  " if verdict else "FAIL"} self-test: {title}')
        failures += not verdict
    limit_failures, limit_cases = self_test_limits(args)
    failures += limit_failures
    print(f'\n{"PASSED" if not failures else "FAILED"}: self-test, {len(cases) + limit_cases} cases, {failures} failed')
    return failures


def self_test_limits(args):
    """Runs PRINT_X directly, to check the output limit exactly at its boundary on every system.
    Returns (failures, number of checks)."""
    checks = [  # (title, input, stream, whether the stream must go over the limit)
        ('exactly 65536 bytes on stdout are allowed', '65536 0\n', 'stdout', False),
        ('65537 bytes on stdout are over the limit', '65537 0\n', 'stdout', True),
        ('exactly 65536 bytes on stderr are allowed', '65536 1\n', 'stderr', False),
        ('65537 bytes on stderr are over the limit', '65537 1\n', 'stderr', True),
        ('a program printing 10 MB to stdout is stopped early, keeping 65537 bytes', '10000000 0\n', 'stdout', True),
        ('a program printing 10 MB to stderr, and nothing to stdout, is stopped early', '10000000 1\n', 'stderr', True),
    ]
    project = PROJECT.resolve()
    home = os.getcwd()
    failures = 0
    with tempfile.TemporaryDirectory() as root:
        os.chdir(root)
        try:
            PROJECT.parent.mkdir(parents=True)
            shutil.copy(project, PROJECT)
            built = build('self_test', 'output_limit', PRINT_X, args)
            if not built or built[1].returncode != 0:
                print('##### FAIL self-test: the output-limit program did not build')
                return len(checks), len(checks)
            exe = executable(built[0])
            for title, data, stream, over in checks:
                start = time.monotonic()
                returncode, stdout, stderr, timed_out, over_limit = run_program(exe, data, args.timeout)
                seconds = time.monotonic() - start
                kept = len(stdout if stream == 'stdout' else stderr)
                expected_kept = OUTPUT_LIMIT + 1 if over else int(data.split()[0])
                verdict = (over_limit == ([stream] if over else []) and kept == expected_kept and not timed_out
                           and (over or returncode == 0))
                print(f'\n##### self-test: {title}: kept {kept} bytes of {stream}, '
                      f'over the limit: {", ".join(over_limit) or "none"}, timed out: {timed_out}, {seconds:.2f} s')
                print(f'##### {"ok  " if verdict else "FAIL"} self-test: {title}')
                failures += not verdict
        finally:
            os.chdir(home)
    return failures, len(checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--cxx', required=True, help='full path to the official clang++')
    parser.add_argument('--cmake', default='cmake')
    parser.add_argument('--make-program', help='Ninja to use, if not the one on PATH')
    parser.add_argument('--timeout', type=float, default=10, help='seconds each run of an example may take')
    parser.add_argument('--self-test', action='store_true', help='check the checker on small fixture lessons')
    args = parser.parse_args()
    if args.self_test:
        return 1 if self_test(args) else 0
    return 1 if check_course(args) else 0


if __name__ == '__main__':
    sys.exit(main())
