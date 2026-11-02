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

A program in several files has, besides its example or broken block (its main.cpp), at least one file block and
exactly one cmake block with the same NAME, anywhere in the lesson:

    <!-- file: NAME PATH -->            the next ```cpp block is the file PATH of program NAME: a lowercase name
                                        of at most 24 characters ending in .cpp or .hpp, with no folders;
    <!-- cmake: NAME -->                the next ```cmake block is the CMakeLists.txt of program NAME: the lesson 0.5
                                        file with only the sources of add_executable(first_program ...) changed,
                                        on one line, main.cpp included; an example lists all of its .cpp files.
                                        Its quoted #include lines must name its .hpp files exactly (comments are
                                        skipped), and #if, #ifdef and #ifndef aren't allowed. It is built one job at
                                        a time. A broken program in several files can only be stage=link: then every
                                        listed source must compile, only the link step of first_program may fail,
                                        and REGEX must match that step's output.

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

MARKER = re.compile(r'^<!-- (?:(example|output|input|broken|file|cmake): ([a-z0-9_]+)(.*?)|(fragment)) -->$')
SOURCE = re.compile(r'^(?: source=(\S+))?(?: exit=(\d+))?$')
BROKEN = re.compile(r'^(?: stage=(link))?(?: at=(\d+)(?::(\d+))?)?(?: errors=(\d+))? error=(.+)$')
FILE = re.compile(r'^ (\S+)$')
FENCE = re.compile(r'^```(\S*)$')
# The file name of a file block: lowercase, a letter first, .cpp or .hpp, at most 24 characters, no folders.
FILE_NAME = re.compile(r'^[a-z][a-z0-9_]{0,19}\.(?:cpp|hpp)$')
# Device names that Windows reserves, even with an extension.
WINDOWS_DEVICES = {'con', 'prn', 'aux', 'nul', *(f'com{n}' for n in range(1, 10)), *(f'lpt{n}' for n in range(1, 10))}
ADD_EXECUTABLE = re.compile(r'^add_executable\(first_program((?: [^ ()]+)+)\)$')
DIRECTIVE = re.compile(r'^\s*#\s*([a-z_]+)')
INCLUDE = re.compile(r'^#include (?:<[^<>]+>|"([^"]*)")$')
CONDITIONALS = {'if', 'ifdef', 'ifndef', 'elif', 'elifdef', 'elifndef', 'else', 'endif'}
# A failed Ninja step: "FAILED: [code=1] OUTPUT ..." (Ninja 1.12 and newer) or "FAILED: OUTPUT ..." (older).
FAILED_STEP = re.compile(r'^FAILED: (?:\[code=\d+\] )?(\S+)')
STEP_START = re.compile(r'^(?:\[\d+/\d+\] |FAILED: |ninja: )')
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
            pattern = BROKEN if kind == 'broken' else SOURCE if kind == 'example' else FILE if kind == 'file' else re.compile('^$')
            parsed = pattern.match(attributes)
            # A compile-stage broken program needs at=; a link-stage one has no line in main.cpp to point to,
            # and no compile errors to count, so it takes neither at= nor errors=.
            if not parsed or (kind == 'broken' and (bool(parsed[1]) == bool(parsed[2]) or (parsed[1] and parsed[4]))):
                fail(f'{path}:{i + 1}: cannot read the {kind} marker{unsupported(kind, attributes)}: {line}')
                kind = 'unreadable'
            marker = (kind, match[2], attributes, i + 1)
        elif fence:
            start, language, body = i + 1, fence[1], []
            i += 1
            while i < len(lines) and lines[i] != '```':
                body.append(lines[i])
                i += 1
            text = '\n'.join(body) + '\n'
            if marker and marker[0] == 'unreadable':
                pass  # already reported: its block is neither built nor compared
            elif marker:
                kind, name, attributes = marker[:3]
                expected = 'text' if kind in ('output', 'input') else 'cmake' if kind == 'cmake' else 'cpp'
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


def unsupported(kind, attributes):
    """Why a broken marker that can't be read asks for something this check doesn't support, or ''.
    Only the part before error= counts: the regular expression after it may contain anything."""
    if kind != 'broken':
        return ''
    head = attributes.split(' error=', 1)[0]
    if re.search(r'(?:^| )in=', head):
        return ' (in= is not supported yet: a compile error located in another file of a program is not checked)'
    stage = re.search(r'(?:^| )stage=(\S+)', head)
    if stage and stage[1] != 'link':
        return f' (stage={stage[1]} is not supported: a broken program can only fail to compile or, with stage=link, to link)'
    return ''


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


def check_projects(path, found, examples, broken):
    """Checks the file and cmake blocks of the programs in several files, before anything is built.
    Returns {NAME: (its other files {file name: text}, its CMakeLists.txt)} for the programs that may be built,
    and the set of names that must not be built. A program without file and cmake blocks is in neither."""
    files, cmakes, refused = {}, {}, set()
    for kind, name, attributes, language, text, line in found:
        if kind not in ('file', 'cmake'):
            continue
        label = f'file {attributes.strip()} of {name}' if kind == 'file' else f'cmake block of {name}'
        if name not in examples and name not in broken:
            fail(f'{path}:{line}: {label} has no program: no example or broken block {name} in this lesson')
            continue
        if language != ('cmake' if kind == 'cmake' else 'cpp'):
            refused.add(name)  # the fence is already reported
        if kind == 'cmake':
            if name in cmakes:
                fail(f'{path}:{line}: {label} defined twice')
                refused.add(name)
            cmakes.setdefault(name, text)
            continue
        file_name = attributes.strip()
        problem = file_name_problem(file_name)
        if problem:
            fail(f'{path}:{line}: {label}: {problem}')
            refused.add(name)
        elif file_name in files.setdefault(name, {}):
            fail(f'{path}:{line}: {label} defined twice')
            refused.add(name)
        else:
            files[name][file_name] = text
    projects = {}
    for name in sorted(set(files) | set(cmakes)):
        program_files = files.get(name, {})
        problems = []
        if name not in cmakes:
            problems.append('it has file blocks but no cmake block (a program in several files has exactly one)')
        else:
            problems += cmake_problems(cmakes[name], program_files, name in examples)
        if not program_files:
            problems.append('it has a cmake block but no file blocks '
                            '(show the CMakeLists.txt of a one-file program as an unmarked block)')
        if name in broken and broken[name][1][1] != 'link':
            problems.append('a compile error in a program of several files is not supported yet: '
                            'a broken program in several files can only be stage=link')
        code = examples[name][0] if name in examples else broken[name][0]
        problems += include_problems(code, program_files)
        for problem in problems:
            fail(f'{path}: program {name}: {problem}')
        if problems or name in refused:
            refused.add(name)
        else:
            projects[name] = (program_files, cmakes[name])
    return projects, refused


def file_name_problem(file_name):
    """What is wrong with the file name of a file block, or None."""
    if file_name == 'main.cpp':
        return "main.cpp is the program's own block (its example or broken block), not a file block"
    if not FILE_NAME.match(file_name):
        return ('not a valid file name: lowercase letters, digits and _, starting with a letter, '
                'ending in .cpp or .hpp, at most 24 characters, no folders')
    if file_name.split('.')[0] in WINDOWS_DEVICES:
        return 'a reserved name on Windows'
    return None


def cmake_problems(text, files, is_example):
    """What is wrong with the CMakeLists.txt of a program in several files: it must be the lesson 0.5 file with only
    the sources of add_executable(first_program ...) changed. No CMake code is interpreted."""
    template = PROJECT.read_text(encoding='utf-8').splitlines()
    at = next(i for i, line in enumerate(template) if line.startswith('add_executable('))
    lines = text.splitlines()
    if any(line.startswith('add_executable(') and not line.endswith(')') for line in lines):
        return ['add_executable must list its sources on one line']
    if len(lines) != len(template) or any(line != model for i, (line, model) in enumerate(zip(lines, template)) if i != at):
        return ['the cmake block differs from the lesson 0.5 CMakeLists.txt outside add_executable']
    command = ADD_EXECUTABLE.match(lines[at])
    if not command:
        return ['the cmake block must have add_executable(first_program SOURCES) on one line, '
                'with the sources separated by single spaces']
    sources = command[1].split()
    names = {name.lower(): name for name in ['main.cpp', *files]}
    problems = []
    for number, source in enumerate(sources):
        if source in sources[:number]:
            problems.append(f'add_executable lists {source} twice')
        elif source.endswith('.hpp'):
            problems.append(f'add_executable lists the header {source}: headers are not listed in add_executable')
        elif source == 'main.cpp' or (source in files and source.endswith('.cpp')):
            continue
        elif source.lower() in names:
            problems.append(f'add_executable lists {source}, which differs in case from {names[source.lower()]}')
        else:
            problems.append(f'add_executable lists {source}, which is not a .cpp file of the program '
                            '(CMake would stop at configuration, and stage=configure is not supported)')
    if 'main.cpp' not in sources:
        problems.append('add_executable must list main.cpp')
    if is_example:
        for name in files:
            if name.endswith('.cpp') and name not in sources:
                problems.append(f'{name} is not in add_executable (an example lists all of its .cpp files; '
                                'leaving one out is allowed only in a broken stage=link program)')
    return problems


def include_problems(code, files):
    """What is wrong with the preprocessor directives of a program in several files. Comments are skipped.
    Conditional directives are refused rather than interpreted, so every #include found is a real one."""
    names = {name.lower(): name for name in ['main.cpp', *files]}
    problems = []
    for file_name, text in [('main.cpp', code), *files.items()]:
        for number, line in enumerate(active_lines(text), 1):
            directive = DIRECTIVE.match(line)
            if not directive:
                continue
            where = f'{file_name}:{number}'
            if directive[1] in CONDITIONALS:
                problems.append(f'{where}: #{directive[1]}: conditional preprocessor directives are not supported '
                                'in programs of several files (a header uses #pragma once)')
            elif directive[1] == 'include':
                problem = include_problem(line, files, names)
                if problem:
                    problems.append(f'{where}: {problem}')
    return problems


def include_problem(line, files, names):
    """What is wrong with one #include LINE of a program in several files, or None. NAMES maps the lowercase name
    of every file of the program to its real name."""
    unsupported_form = (f'unsupported #include form: {line.strip()} '
                        '(use #include <...>, or #include "name.hpp" for a header of the program)')
    form = INCLUDE.match(line.rstrip())
    if not form:
        return unsupported_form
    header = form[1]
    if header is None or (header in files and header.endswith('.hpp')):
        return None
    real = names.get(header.lower())
    if real and real != header and real.endswith('.hpp'):
        return f'#include "{header}" differs in case from {real}'
    if not (FILE_NAME.match(header) and header.endswith('.hpp')):
        return unsupported_form
    return f'#include "{header}" is not a file of the program (a missing header can\'t be checked yet)'


def active_lines(code):
    """CODE's lines without comments: // to the end of the line, and /* ... */ across lines. String and character
    literals are kept whole, so that a // or /* inside them starts nothing. Not a C++ preprocessor: just enough
    to find the directives outside comments."""
    lines, current, i, in_comment = [], [], 0, False
    while i < len(code):
        pair, char = code[i:i + 2], code[i]
        if in_comment:
            if pair == '*/':
                in_comment, i = False, i + 2
                continue
            if char == '\n':
                lines.append(''.join(current))
                current = []
            i += 1
        elif pair == '//':
            end = code.find('\n', i)
            i = len(code) if end < 0 else end
        elif pair == '/*':
            current.append(' ')
            in_comment, i = True, i + 2
        elif char == '"' or (char == "'" and not ''.join(current)[-1:].isalnum()):
            end = i + 1
            while end < len(code) and code[end] not in (char, '\n'):
                end += 2 if code[end] == '\\' else 1
            current.append(code[i:end + 1])
            i = end + 1
        elif char == '\n':
            lines.append(''.join(current))
            current = []
            i += 1
        else:
            current.append(char)
            i += 1
    lines.append(''.join(current))
    return lines


def failed_steps(output):
    """Ninja's failed steps in a build OUTPUT, as (kind, what, the step's own output). The kind is 'scan' or 'compile'
    of a source (what is its file name), 'link' of the program, or 'other' (what is the step's output file)."""
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    steps, lines = [], None
    for line in output.splitlines():
        failed = FAILED_STEP.match(line)
        if failed:
            name = failed[1].replace('\\', '/').rsplit('/', 1)[-1]
            source = re.match(r'^(.+\.cpp)\.(?:o|obj)(\.ddi)?$', name)
            if source:
                kind, what = ('scan' if source[2] else 'compile'), source[1]
            elif name in (target, target + '.exe'):
                kind, what = 'link', name
            else:
                kind, what = 'other', failed[1]
            lines = []
            steps.append((kind, what, lines))
        elif lines is not None and STEP_START.match(line):
            lines = None
        elif lines is not None:
            lines.append(line)
    return [(kind, what, '\n'.join(text)) for kind, what, text in steps]


def step_failure(kind, what):
    """A failed step in words."""
    return {'scan': f'{what} failed dependency scanning', 'compile': f'{what} failed to compile',
            'link': 'the program failed to link'}.get(kind, f'the build step {what} failed')


def run(command):
    return subprocess.run(command, capture_output=True, text=True, encoding='utf-8', errors='replace')


def build(lesson, name, code, args, flags=WARNINGS, project=None):
    """Configures and builds a copy of the project with CODE as main.cpp.
    PROJECT is None for a one-file program (the lesson 0.5 CMakeLists.txt), or, for a program in several files,
    (its other files {file name: text}, its CMakeLists.txt); such a program is built one job at a time.
    Returns (build directory, build result), or None when configuring failed."""
    work = pathlib.Path('build/lesson-examples') / lesson / name
    shutil.rmtree(work, ignore_errors=True)
    src = work / 'src'
    src.mkdir(parents=True)
    if project is None:
        shutil.copy(PROJECT, src / 'CMakeLists.txt')
    else:
        files, cmake = project
        for file_name, text in [*files.items(), ('CMakeLists.txt', cmake)]:
            target = src / file_name
            # The names were checked before; this makes sure that nothing is ever written outside src.
            if target.resolve().parent != src.resolve():
                fail(f'{lesson}: {name}: {file_name} would be written outside {src}')
                return None
            target.write_text(text, encoding='ascii', newline='\n')
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
    command = [args.cmake, '--build', str(work / 'build')]
    if project is not None:
        # One job at a time: the steps run, and a failed build stops, in the same order on every system.
        command += ['-j', '1']
    return work / 'build', run(command)


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


def check_example(lesson, name, code, exit_code, runs, args, project=None):
    built = build(lesson, name, code, args, project=project)
    if not built:
        return
    build_dir, result = built
    if result.returncode != 0:
        # A program in several files names its first failed step: a source that didn't compile, or the link.
        steps = failed_steps(result.stdout + result.stderr) if project else []
        reason = f': {step_failure(*steps[0][:2])}' if steps else ''
        fail(f'{lesson}: example {name}: build failed{reason}\n{result.stdout}{result.stderr}')
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


def check_project_link(lesson, name, code, expectation, project, args):
    """A broken program in several files (only stage=link): every source in add_executable compiled, and then only
    the link of the program failed, for the expected reason. A failure of any earlier step is rejected."""
    built = build(lesson, name, code, args, flags='', project=project)
    if not built:
        return
    build_dir, result = built
    output = result.stdout + result.stderr
    if result.returncode == 0:
        fail(f'{lesson}: broken program {name} builds, but the lesson says it must not')
        return
    steps = failed_steps(output)
    sources = ADD_EXECUTABLE.match(next(line for line in project[1].splitlines() if line.startswith('add_executable(')))[1].split()
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    objects = build_dir / 'CMakeFiles' / f'{target}.dir'
    exe = executable(build_dir)
    problems = []
    early = [(kind, what) for kind, what, _ in steps if kind != 'link']
    if early:
        problems.append(f'{step_failure(*early[0])}, so the build stopped before linking')
    elif [kind for kind, _, _ in steps] != ['link']:
        problems.append('the build failed, but no link step of the program failed')
    else:
        link_output = steps[0][2]
        missing = [source for source in sources
                   if not (objects / f'{source}.o').exists() and not (objects / f'{source}.obj').exists()]
        if missing:
            problems.append(f'no object file for {", ".join(missing)}, so compiling did not succeed')
        if 'linker command failed' not in link_output:
            problems.append('the link step failed, but not in the linker ("linker command failed" is missing)')
        if exe.exists():
            problems.append(f'the program {exe.name} was created')
        if not re.search(expectation[5], link_output, re.MULTILINE):
            problems.append(f"the link step's output has no match for {expectation[5]!r}")
    if problems:
        fail(f'{lesson}: broken program {name} (stage=link, several files): ' + '; '.join(problems) + f'\n{output}')
        return
    print(f'ok   {lesson}: broken program {name} compiles {", ".join(sources)} and fails to link as described')
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
        projects, refused = check_projects(pl, pl_blocks, examples, broken)
        if en.exists():
            en_examples, _, en_broken = check_lesson(en, en_blocks)
            check_projects(en, en_blocks, en_examples, en_broken)
        fragments = sum(1 for block in pl_blocks if block[0] == 'fragment')
        inputs = sum(1 for block in pl_blocks if block[0] == 'input')
        print(f'     {len(examples)} examples to build and run ({inputs} runs with standard input), '
              f'{len(broken)} broken programs that must not compile, '
              f'{fragments} fragments (deliberately incomplete, not built)')
        if projects or refused:
            print(f'     {len(projects)} of these programs in several files (file and cmake blocks), '
                  f'{len(refused)} not built because of the problems above')
        # Programs without file and cmake blocks take the same path as before.
        for name, (code, exit_code) in examples.items():
            if name not in refused:
                check_example(pl.stem, name, code, exit_code, runs.get(name, []), args, projects.get(name))
        for name, (code, expectation) in broken.items():
            if name in projects:
                check_project_link(pl.stem, name, code, expectation, projects[name], args)
            elif name not in refused:
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
# A program in several files: main.cpp calls twice(), declared in tools.hpp and defined in tools.cpp.
TWICE_MAIN = ('#include <iostream>\n\n#include "tools.hpp"\n\nint main() {\n    int value{0};\n\n    std::cin >> value;\n'
              '    std::cout << "Twice: " << twice(value) << "\\n";\n}\n')
TOOLS_HPP = '#pragma once\n\nint twice(int value);\n'
TOOLS_CPP = '#include "tools.hpp"\n\nint twice(int value) {\n    return value * 2;\n}\n'
# twice(int) missing at link time, in the wording of GNU ld, lld-link and Apple's ld (as in lesson 5.6).
TWICE_LINK = ('broken: twice stage=link error=undefined reference to .twice\\(int\\)\'|undefined symbol: int __cdecl twice\\(int\\)'
              '|"twice\\(int\\)", referenced from')


def lesson(*parts):
    """A fixture lesson made of (marker, language, code) parts."""
    return ''.join(f'<!-- {marker} -->\n```{language}\n{code}```\n\n' for marker, language, code in parts)


def self_test(args):
    """Runs the checker on small fixture courses; each must give the expected verdict."""
    good = [('example: hi', 'cpp', GOOD), ('output: hi', 'text', 'Hi!\n')]
    semicolon = "broken: no_semicolon at=4 errors=1 error=expected ';'"
    link = 'broken: mian stage=link error=undefined reference to .main\'|undefined symbol: main\\b|"_main", referenced from'
    # Programs in several files: the lesson 0.5 CMakeLists.txt, with tools.cpp added or (template) left out.
    template = PROJECT.read_text(encoding='utf-8')
    cmake_two = template.replace('add_executable(first_program main.cpp)', 'add_executable(first_program main.cpp tools.cpp)')

    def program(owner='example: twice', main=TWICE_MAIN, cpp=TOOLS_CPP, cmake=cmake_two, hpp=TOOLS_HPP):
        """The parts of program twice, with some of them replaced."""
        return [(owner, 'cpp', main), ('file: twice tools.hpp', 'cpp', hpp), ('file: twice tools.cpp', 'cpp', cpp),
                ('cmake: twice', 'cmake', cmake)]

    def with_sources(sources):
        return cmake_two.replace('main.cpp tools.cpp)', f'{sources})')

    twice_runs = [('input: twice', 'text', '4\n'), ('output: twice', 'text', 'Twice: 8\n'),
                  ('input: twice', 'text', '-3\n'), ('output: twice', 'text', 'Twice: -6\n')]
    twice = program() + twice_runs
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
        # A broken marker that can't be read is reported, and its program is never built.
        ('a compile-stage broken marker with errors= but without at= is reported, and nothing is built',
         lesson(("broken: no_semicolon errors=1 error=expected ';'", 'cpp', NO_SEMICOLON)), None, 'cannot read the broken marker'),
        ('a compile-stage broken marker with neither at= nor errors= is reported, and nothing is built',
         lesson(("broken: no_semicolon error=expected ';'", 'cpp', NO_SEMICOLON)), None, 'cannot read the broken marker'),
        ('a stage=link marker with at= is reported, and nothing is built',
         lesson(('broken: mian stage=link at=4 error=main', 'cpp', MIAN)), None, 'cannot read the broken marker'),
        ('a stage=link marker with errors= is reported, and nothing is built',
         lesson(('broken: mian stage=link errors=1 error=main', 'cpp', MIAN)), None, 'cannot read the broken marker'),
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
        # Programs in several files, checked before anything is built (no CMake, no compiler).
        ('a file marker without a file name is reported, and nothing is built',
         lesson(*program()[:1], ('file: twice', 'cpp', TOOLS_HPP), *program()[2:], *twice_runs), None,
         'cannot read the file marker'),
        ('a cmake marker with an attribute is reported, and nothing is built',
         lesson(*program()[:3], ('cmake: twice extra', 'cmake', cmake_two), *twice_runs), None, 'cannot read the cmake marker'),
        ('a cmake marker on a text block is reported, and nothing is built',
         lesson(*program()[:3], ('cmake: twice', 'text', cmake_two), *twice_runs), None,
         'cmake marker on a ```text block, expected ```cmake'),
        ('a file block without a program of its name is reported, and nothing is built',
         lesson(('file: other tools.cpp', 'cpp', TOOLS_CPP)), None, 'file tools.cpp of other has no program'),
        ('a commented-out #include "missing.hpp" is not a dependency, while an active #include is checked; nothing is built',
         lesson(*program(main=TWICE_MAIN.replace('#include "tools.hpp"\n', '// #include "missing.hpp"\n/* #include "missing.hpp"\n'
                                                 '   #include "missing.hpp" */\n#include "Tools.hpp" // twice()\n')), *twice_runs),
         None, '#include "Tools.hpp" differs in case from tools.hpp'),
        ('a file block repeated in one program is reported, and nothing is built',
         lesson(*twice, ('file: twice tools.cpp', 'cpp', TOOLS_CPP)), None, 'file tools.cpp of twice defined twice'),
        ('a cmake block repeated in one program is reported, and nothing is built',
         lesson(*twice, ('cmake: twice', 'cmake', cmake_two)), None, 'cmake block of twice defined twice'),
        ('a file name with ../ is reported, and nothing is built',
         lesson(*program()[:2], ('file: twice ../tools.cpp', 'cpp', TOOLS_CPP), *program()[3:], *twice_runs), None,
         'file ../tools.cpp of twice: not a valid file name'),
        ('a file name with a capital letter is reported, and nothing is built',
         lesson(*program()[:1], ('file: twice Tools.hpp', 'cpp', TOOLS_HPP), *program()[2:], *twice_runs), None,
         'file Tools.hpp of twice: not a valid file name'),
        ('a file name reserved on Windows is reported, and nothing is built',
         lesson(*program()[:1], ('file: twice con.hpp', 'cpp', TOOLS_HPP), *program()[2:], *twice_runs), None,
         'file con.hpp of twice: a reserved name on Windows'),
        ('a file block named main.cpp is reported, and nothing is built',
         lesson(*twice, ('file: twice main.cpp', 'cpp', TWICE_MAIN)), None, "main.cpp is the program's own block"),
        ('a file name longer than 24 characters is reported, and nothing is built',
         lesson(*twice, ('file: twice abcdefghijklmnopqrstu.cpp', 'cpp', TOOLS_CPP)), None,
         'file abcdefghijklmnopqrstu.cpp of twice: not a valid file name'),
        ('file blocks without a cmake block are reported, and nothing is built',
         lesson(*program()[:3], *twice_runs), None, 'it has file blocks but no cmake block'),
        ('a cmake block without file blocks is reported, and nothing is built',
         lesson(*good, ('cmake: hi', 'cmake', template)), None, 'it has a cmake block but no file blocks'),
        ('a cmake block with a changed setting is reported, and nothing is built',
         lesson(*program(cmake=cmake_two.replace('CXX_EXTENSIONS OFF', 'CXX_EXTENSIONS ON')), *twice_runs), None,
         'differs from the lesson 0.5 CMakeLists.txt outside add_executable'),
        ('a cmake block with an added command is reported, and nothing is built',
         lesson(*program(cmake=cmake_two + 'target_compile_options(first_program PRIVATE -w)\n'), *twice_runs), None,
         'differs from the lesson 0.5 CMakeLists.txt outside add_executable'),
        ('sources of add_executable on several lines are reported, and nothing is built',
         lesson(*program(cmake=with_sources('\n    main.cpp\n    tools.cpp\n')), *twice_runs), None,
         'add_executable must list its sources on one line'),
        ('a source in add_executable that is not a file of the program is reported, and nothing is built',
         lesson(*program(cmake=with_sources('main.cpp tools.cpp tool.cpp')), *twice_runs), None,
         'add_executable lists tool.cpp, which is not a .cpp file of the program'),
        ('a source in add_executable with another case is reported, and nothing is built',
         lesson(*program(cmake=with_sources('main.cpp Tools.cpp')), *twice_runs), None,
         'add_executable lists Tools.cpp, which differs in case from tools.cpp'),
        ('a source listed twice in add_executable is reported, and nothing is built',
         lesson(*program(cmake=with_sources('main.cpp tools.cpp tools.cpp')), *twice_runs), None,
         'add_executable lists tools.cpp twice'),
        ('add_executable without main.cpp is reported, and nothing is built',
         lesson(*program(cmake=with_sources('tools.cpp')), *twice_runs), None, 'add_executable must list main.cpp'),
        ('a header in add_executable is reported, and nothing is built',
         lesson(*program(cmake=with_sources('main.cpp tools.cpp tools.hpp')), *twice_runs), None,
         'headers are not listed in add_executable'),
        ('an example that leaves a source out of add_executable is reported, and nothing is built',
         lesson(*program(cmake=template), *twice_runs), None, 'tools.cpp is not in add_executable'),
        ('an #include with another case is reported in an example, and nothing is built',
         lesson(*program(main=TWICE_MAIN.replace('"tools.hpp"', '"Tools.hpp"')), *twice_runs), None,
         '#include "Tools.hpp" differs in case from tools.hpp'),
        ('an #include with another case is reported in a stage=link program, and nothing is built',
         lesson(*program(owner=TWICE_LINK, main=TWICE_MAIN.replace('"tools.hpp"', '"Tools.hpp"'), cmake=template)), None,
         '#include "Tools.hpp" differs in case from tools.hpp'),
        ('an #include of a header that is not a file of the program is reported, and nothing is built',
         lesson(*program(main=TWICE_MAIN.replace('"tools.hpp"', '"tool.hpp"')), *twice_runs), None,
         '#include "tool.hpp" is not a file of the program'),
        ('an #include with a folder is reported, and nothing is built',
         lesson(*program(main=TWICE_MAIN.replace('"tools.hpp"', '"lib/tools.hpp"')), *twice_runs), None,
         'unsupported #include form'),
        ('a compile-stage broken program in several files is refused as not supported, and nothing is built',
         lesson(*program(owner="broken: twice at=4 errors=1 error=expected ';'")), None,
         'a compile error in a program of several files is not supported yet'),
        ('#ifndef in a program in several files is reported, and nothing is built',
         lesson(*program(hpp='#ifndef TOOLS_HPP\n#define TOOLS_HPP\n\nint twice(int value);\n\n#endif\n'), *twice_runs), None,
         'conditional preprocessor directives are not supported'),
        ('a broken marker with in= is refused as not supported, and nothing is built',
         lesson(("broken: no_semicolon in=main.cpp at=4 errors=1 error=expected ';'", 'cpp', NO_SEMICOLON)), None,
         'in= is not supported yet'),
        ('a broken marker with stage=configure is refused as not supported, and nothing is built',
         lesson(('broken: mian stage=configure error=main', 'cpp', MIAN)), None, 'stage=configure is not supported'),
        # Programs in several files, really built with CMake and Ninja (and run where they build).
        ('a program in several files (two .cpp files, a local .hpp) builds, links and passes two runs',
         lesson(*twice), None, None),
        ('a wrong output of the second run of a program in several files is detected',
         lesson(*twice[:-1], ('output: twice', 'text', 'Twice: -5\n')), None, 'example twice (input 2 of 2): output'),
        ('a one-file example and a program in several files in one lesson both pass, and the one-file example is built as before',
         lesson(*good, *twice), None, None),
        ('a source left out of add_executable fails to link as described (stage=link, several files)',
         lesson(*program(owner=TWICE_LINK, cmake=template)), None, None),
        ('a stage=link program in several files whose source fails to compile is detected',
         lesson(*program(owner=TWICE_LINK, cpp=TOOLS_CPP.replace('* 2;', '* 2'))), None,
         'tools.cpp failed to compile, so the build stopped before linking'),
        ('a stage=link program in several files that builds is detected',
         lesson(*program(owner=TWICE_LINK)), None, 'builds, but the lesson says it must not'),
        # The build output says "Building CXX object" before the link step: only the link step's own output counts.
        ('a message found only outside the link step is detected (stage=link, several files)',
         lesson(*program(owner='broken: twice stage=link error=Building CXX object', cmake=template)), None,
         "the link step's output has no match"),
        ('a stage=link program in several files that fails at dependency scanning is detected',
         lesson(*program(owner=TWICE_LINK, cpp='#include <no_such_header>\n' + TOOLS_CPP)), None,
         'tools.cpp failed dependency scanning, so the build stopped before linking'),
        ('an example in several files whose second source fails to compile is reported with its file',
         lesson(*program(cpp=TOOLS_CPP.replace('* 2;', '* 2')), *twice_runs), None, 'build failed: tools.cpp failed to compile'),
        ('an example in several files that fails to link is reported as a link failure',
         lesson(*program(cpp=TOOLS_CPP.replace('int twice(int value) {', 'int twice_value(int value) {')), *twice_runs), None,
         'build failed: the program failed to link'),
        ('an unexpected exit code of a program in several files is detected',
         lesson(*program(main=TWICE_MAIN.replace('<< "\\n";\n}\n', '<< "\\n";\n    return 3;\n}\n')), *twice_runs[:2]), None,
         'exit code 3, expected 0'),
        ('different PL and EN files of a program in several files are detected',
         lesson(*twice), lesson(*program(cpp=TOOLS_CPP.replace('* 2', '* 3')), *twice_runs), 'differ between'),
        ('a broken environment is not taken for the result of a program in several files',
         lesson(*twice), None, 'configure failed (an environment problem'),
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
                if 'nothing is built' in title:
                    verdict = verdict and not pathlib.Path('build').exists()
                if 'is not a dependency' in title:
                    verdict = verdict and not any('missing.hpp' in e for e in errors)
                if 'built as before' in title:
                    # The one-file example got the lesson 0.5 project as it is; the other one its own four files.
                    old = pathlib.Path('build/lesson-examples/lesson/hi/src')
                    new = pathlib.Path('build/lesson-examples/lesson/twice/src')
                    verdict = (verdict and sorted(p.name for p in old.iterdir()) == ['CMakeLists.txt', 'main.cpp']
                               and (old / 'CMakeLists.txt').read_bytes() == PROJECT.read_bytes()
                               and sorted(p.name for p in new.iterdir()) == ['CMakeLists.txt', 'main.cpp', 'tools.cpp', 'tools.hpp'])
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
