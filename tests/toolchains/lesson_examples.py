#!/usr/bin/env python3
"""Builds and runs the C++ examples published in the lessons. Used by the Toolchains workflow.

Lessons mark their code blocks with HTML comments, which GitHub does not show:

    <!-- example: NAME -->              the next ```cpp block is a complete program;
    <!-- example: NAME source=PATH -->  ... and it must equal the file PATH (relative to the lesson);
    <!-- example: NAME exit=N -->        ... and it must exit with code N instead of 0;
    <!-- output: NAME -->               the next ```text block is the exact output of example NAME;
    <!-- broken: NAME at=LINE[:COLUMN] [errors=N] error=REGEX -->
                                        the next ```cpp block is a complete program with deliberate
                                        mistakes: it must FAIL TO COMPILE, and the first compiler
                                        error in main.cpp must be at LINE (and COLUMN), with a message
                                        matching REGEX (a Python regular expression); with errors=N,
                                        main.cpp must get exactly N errors;
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
    output (Windows line ends ignored);
  * a broken program must fail to build because of compiler errors in main.cpp, as described
    by its marker. Its whole build output is printed, to compare the messages across systems.

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

MARKER = re.compile(r'^<!-- (?:(example|output|broken): ([a-z0-9_]+)(.*?)|(fragment)) -->$')
SOURCE = re.compile(r'^(?: source=(\S+))?(?: exit=(\d+))?$')
BROKEN = re.compile(r'^ at=(\d+)(?::(\d+))?(?: errors=(\d+))? error=(.+)$')
FENCE = re.compile(r'^```(\S*)$')
# A compiler error in main.cpp: GNU style (main.cpp:4:35: error: ...) or MSVC style (main.cpp(4,35): error: ...).
ERROR = re.compile(r'main\.cpp(?::(\d+):(\d+):|\((\d+),(\d+)\):) error: (.*)')
PROJECT = pathlib.Path('course/module_00_tooling/lesson_05_first_program/CMakeLists.txt')
WARNINGS = '-Wall -Wextra -pedantic-errors -Werror'

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
            if not pattern.match(attributes):
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
                expected = 'text' if kind == 'output' else 'cpp'
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
    """Checks one lesson's markers; returns its examples, outputs and broken programs."""
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
    outputs = {}
    for kind, name, _, _, text, line in found:
        if kind == 'output':
            if name not in examples:
                fail(f'{path}:{line}: output {name} has no example')
            outputs.setdefault(name, []).append(text)
    for name in examples:
        if name not in outputs:
            fail(f'{path}: example {name} has no output block')
    return examples, outputs, broken


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


def check_example(lesson, name, code, exit_code, expected, args):
    built = build(lesson, name, code, args)
    if not built:
        return
    build_dir, result = built
    if result.returncode != 0:
        fail(f'{lesson}: example {name}: build failed\n{result.stdout}{result.stderr}')
        return
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    exe = build_dir / (target + ('.exe' if sys.platform == 'win32' else ''))
    result = subprocess.run([str(exe)], capture_output=True)
    out = result.stdout.decode('ascii', errors='replace').replace('\r\n', '\n')
    if result.returncode != exit_code:
        fail(f'{lesson}: example {name}: exit code {result.returncode}, expected {exit_code}')
    if result.stderr:
        fail(f'{lesson}: example {name}: printed to stderr: {result.stderr!r}')
    for text in expected:
        if out != text:
            fail(f'{lesson}: example {name}: output {out!r}, expected {text!r}')
            return
    print(f'ok   {lesson}: example {name} builds, runs, exits with {exit_code} '
          f'and prints the expected {len(expected)} output block(s):')
    for line in out.splitlines():
        print(f'       | {line}')


def check_broken(lesson, name, code, expectation, args):
    built = build(lesson, name, code, args, flags='')
    if not built:
        return
    _, result = built
    output = result.stdout + result.stderr
    if result.returncode == 0:
        fail(f'{lesson}: broken program {name} builds, but the lesson says it must not')
        return
    found = [(int(m[1] or m[3]), int(m[2] or m[4]), m[5]) for m in ERROR.finditer(output)]
    if not found:
        fail(f'{lesson}: broken program {name}: the build failed, but not with a compiler error in main.cpp\n{output}')
        return
    line, column, message = found[0]
    want_line, want_column, want_count, want_error = expectation.groups()
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
        examples, outputs, broken = check_lesson(pl, pl_blocks)
        if en.exists():
            check_lesson(en, en_blocks)
        fragments = sum(1 for block in pl_blocks if block[0] == 'fragment')
        print(f'     {len(examples)} examples to build and run, {len(broken)} broken programs that must not compile, '
              f'{fragments} fragments (deliberately incomplete, not built)')
        for name, (code, exit_code) in examples.items():
            check_example(pl.stem, name, code, exit_code, outputs.get(name, []), args)
        for name, (code, expectation) in broken.items():
            check_broken(pl.stem, name, code, expectation, args)
    if checked == 0:
        fail('no lesson contains marked examples')
    print(f'{"PASSED" if not errors else "FAILED"}: {checked} lesson(s), {len(errors)} problem(s)')
    return len(errors)


GOOD = '#include <iostream>\n\nint main() {\n    std::cout << "Hi!\\n";\n}\n'
NO_SEMICOLON = GOOD.replace('\\n";', '\\n"')
RETURN_3 = GOOD.replace('\n}\n', '\n    return 3;\n}\n')


def lesson(*parts):
    """A fixture lesson made of (marker, language, code) parts."""
    return ''.join(f'<!-- {marker} -->\n```{language}\n{code}```\n\n' for marker, language, code in parts)


def self_test(args):
    """Runs the checker on small fixture courses; each must give the expected verdict."""
    good = [('example: hi', 'cpp', GOOD), ('output: hi', 'text', 'Hi!\n')]
    semicolon = "broken: no_semicolon at=4 errors=1 error=expected ';'"
    cases = [
        ('correct examples pass', lesson(*good), None, None),
        ('a wrong expected output is detected',
         lesson(('example: hi', 'cpp', GOOD), ('output: hi', 'text', 'Hello!\n')), None, 'example hi: output'),
        ('an example with exit=3 that returns 3 passes',
         lesson(('example: hi exit=3', 'cpp', RETURN_3), ('output: hi', 'text', 'Hi!\n')), None, None),
        ('an unexpected exit code is detected',
         lesson(('example: hi', 'cpp', RETURN_3), ('output: hi', 'text', 'Hi!\n')), None, 'exit code 3, expected 0'),
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
    ]
    project = PROJECT.resolve()
    home = os.getcwd()
    failures = 0
    for title, pl_text, en_text, expected_failure in cases:
        case_args = argparse.Namespace(**vars(args))
        if 'environment' in title:
            case_args.cxx = str(pathlib.Path(tempfile.gettempdir()) / 'no-such-compiler' / 'clang++')
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
            finally:
                os.chdir(home)
        print(f'##### {"ok  " if verdict else "FAIL"} self-test: {title}')
        failures += not verdict
    print(f'\n{"PASSED" if not failures else "FAILED"}: self-test, {len(cases)} cases, {failures} failed')
    return failures


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--cxx', required=True, help='full path to the official clang++')
    parser.add_argument('--cmake', default='cmake')
    parser.add_argument('--make-program', help='Ninja to use, if not the one on PATH')
    parser.add_argument('--self-test', action='store_true', help='check the checker on small fixture lessons')
    args = parser.parse_args()
    if args.self_test:
        return 1 if self_test(args) else 0
    return 1 if check_course(args) else 0


if __name__ == '__main__':
    sys.exit(main())
