#!/usr/bin/env python3
"""Builds and runs the C++ examples published in the lessons. Used by the Toolchains workflow.

Lessons mark their code blocks with HTML comments, which GitHub does not show:

    <!-- example: NAME -->              the next ```cpp block is a complete program;
    <!-- example: NAME source=PATH -->  ... and it must equal the file PATH (relative to the lesson);
    <!-- output: NAME -->               the next ```text block is the exact output of example NAME;
    <!-- fragment -->                   the next ```cpp block is deliberately incomplete: not built.

Checks:
  * every ```cpp block in a lesson is marked as an example or a fragment (Module 0 lessons
    predate the markers and are skipped unless marked; their project is checked by the
    other steps of the workflow);
  * every example has at least one output block, and every output block has an example;
  * marked blocks are ASCII only, and the Polish lesson (X.md) and the English one (X.en.md)
    contain the same marked blocks, in the same order;
  * each example is built as main.cpp of the lesson 0.5 project (its CMakeLists.txt) with
    CMake, Ninja and the given compiler, with warnings as errors, then run: it must exit with 0,
    print nothing to stderr, and print exactly the expected output (Windows line ends ignored).
    The configure step must report Clang 22 or newer.

Run from the repository root, with the official compiler:
    python3 tests/toolchains/lesson_examples.py --cxx /usr/bin/clang++-22 [--make-program /usr/bin/ninja]
"""

import argparse
import pathlib
import re
import shutil
import subprocess
import sys

MARKER = re.compile(r'^<!-- (?:(example|output): ([a-z0-9_]+)(?: source=(\S+))?|(fragment)) -->$')
FENCE = re.compile(r'^```(\S*)$')
PROJECT = pathlib.Path('course/module_00_tooling/lesson_05_first_program/CMakeLists.txt')
WARNINGS = '-Wall -Wextra -pedantic-errors -Werror'

errors = []


def fail(message):
    errors.append(message)
    print(f'FAIL {message}')


def blocks(path):
    """Returns the marked code blocks of a lesson as (kind, name, source, language, text, line),
    and the line numbers of unmarked ```cpp blocks."""
    lines = path.read_text(encoding='utf-8').splitlines()
    found, unmarked, marker, i = [], [], None, 0
    while i < len(lines):
        line = lines[i]
        match = MARKER.match(line)
        fence = FENCE.match(line)
        if match:
            if marker:
                fail(f'{path}:{marker[5]}: marker not followed by a code block')
            kind = match[1] or match[4]
            marker = (kind, match[2], match[3], None, None, i + 1)
        elif fence:
            start, language, body = i + 1, fence[1], []
            i += 1
            while i < len(lines) and lines[i] != '```':
                body.append(lines[i])
                i += 1
            text = '\n'.join(body) + '\n'
            if marker:
                kind, name, source = marker[:3]
                expected = 'text' if kind == 'output' else 'cpp'
                if language != expected:
                    fail(f'{path}:{start}: {kind} marker on a ```{language} block, expected ```{expected}')
                found.append((kind, name, source, language, text, start))
            elif language == 'cpp':
                unmarked.append(start)
            marker = None
        elif line.strip() and marker:
            fail(f'{path}:{marker[5]}: marker not followed by a code block')
            marker = None
        i += 1
    return found, unmarked


def check_lesson(path, found):
    examples = {}
    for kind, name, source, _, text, line in found:
        if not text.isascii():
            fail(f'{path}:{line}: non-ASCII text in a marked block')
        if kind == 'example':
            if name in examples:
                fail(f'{path}:{line}: example {name} defined twice')
            examples[name] = text
            if source:
                original = (path.parent / source).read_text(encoding='utf-8')
                if text != original:
                    fail(f'{path}:{line}: example {name} differs from {source}')
                else:
                    print(f'ok   {path.name}: example {name} equals {source}')
    outputs = {}
    for kind, name, _, _, text, line in found:
        if kind == 'output':
            if name not in examples:
                fail(f'{path}:{line}: output {name} has no example')
            outputs.setdefault(name, []).append(text)
    for name in examples:
        if name not in outputs:
            fail(f'{path}: example {name} has no output block')
    return examples, outputs


def run(command, **kwargs):
    return subprocess.run(command, capture_output=True, text=True, **kwargs)


def build_and_run(lesson, name, code, expected, args):
    work = pathlib.Path('build/lesson-examples') / lesson / name
    shutil.rmtree(work, ignore_errors=True)
    src = work / 'src'
    src.mkdir(parents=True)
    shutil.copy(PROJECT, src / 'CMakeLists.txt')
    # newline='\n': the same bytes on every system, as in the lesson.
    (src / 'main.cpp').write_text(code, encoding='ascii', newline='\n')
    configure = [args.cmake, '-S', str(src), '-B', str(work / 'build'), '-G', 'Ninja',
                 '-DCMAKE_BUILD_TYPE=Debug', f'-DCMAKE_CXX_COMPILER={args.cxx}', f'-DCMAKE_CXX_FLAGS={WARNINGS}']
    if args.make_program:
        configure.append(f'-DCMAKE_MAKE_PROGRAM={args.make_program}')
    for step, command in (('configure', configure), ('build', [args.cmake, '--build', str(work / 'build')])):
        result = run(command)
        if result.returncode != 0:
            fail(f'{lesson}: example {name}: {step} failed\n{result.stdout}{result.stderr}')
            return
        if step == 'configure':
            compiler = re.search(r'The CXX compiler identification is (.*)', result.stdout)
            version = re.match(r'Clang (\d+)\.', compiler[1]) if compiler else None
            if not version or int(version[1]) < 22:
                fail(f'{lesson}: example {name}: configured with {compiler[1] if compiler else "an unknown compiler"}')
                return
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    exe = work / 'build' / (target + ('.exe' if sys.platform == 'win32' else ''))
    result = subprocess.run([str(exe)], capture_output=True)
    out = result.stdout.decode('ascii', errors='replace').replace('\r\n', '\n')
    if result.returncode != 0:
        fail(f'{lesson}: example {name}: exit code {result.returncode}')
    if result.stderr:
        fail(f'{lesson}: example {name}: printed to stderr: {result.stderr!r}')
    for text in expected:
        if out != text:
            fail(f'{lesson}: example {name}: output {out!r}, expected {text!r}')
            return
    print(f'ok   {lesson}: example {name} builds, runs and prints the expected {len(expected)} output block(s):')
    for line in out.splitlines():
        print(f'       | {line}')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--cxx', required=True, help='full path to the official clang++')
    parser.add_argument('--cmake', default='cmake')
    parser.add_argument('--make-program', help='Ninja to use, if not the one on PATH')
    args = parser.parse_args()

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
        for path, unmarked in ((pl, pl_unmarked), (en, en_unmarked)):
            for line in unmarked:
                fail(f'{path}:{line}: ```cpp block without an example or fragment marker')
        if not en.exists():
            fail(f'{pl}: no English version {en.name}')
        pl_marked = [(kind, name, source, text) for kind, name, source, _, text, _ in pl_blocks]
        en_marked = [(kind, name, source, text) for kind, name, source, _, text, _ in en_blocks]
        if pl_marked != en_marked:
            fail(f'{pl}: the marked code blocks differ between {pl.name} and {en.name}')
        else:
            print(f'ok   {len(pl_marked)} marked blocks are identical in {pl.name} and {en.name}')
        examples, outputs = check_lesson(pl, pl_blocks)
        if en.exists():
            check_lesson(en, en_blocks)
        fragments = sum(1 for block in pl_blocks if block[0] == 'fragment')
        print(f'     {len(examples)} examples to build, {fragments} fragments (deliberately incomplete, not built)')
        for name, code in examples.items():
            build_and_run(pl.stem, name, code, outputs.get(name, []), args)

    if checked == 0:
        fail('no lesson contains marked examples')
    print(f'{"PASSED" if not errors else "FAILED"}: {checked} lesson(s), {len(errors)} problem(s)')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
