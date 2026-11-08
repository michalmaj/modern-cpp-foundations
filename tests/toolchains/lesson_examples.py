#!/usr/bin/env python3
"""Builds and runs the C++ examples published in the lessons. Used by the Toolchains workflow.

Lessons mark their code blocks with HTML comments, which GitHub does not show:

    <!-- example: NAME -->              the next ```cpp block is a complete program;
    <!-- example: NAME source=PATH -->  ... and it must equal the file PATH (relative to the lesson);
    <!-- example: NAME exit=N -->        ... and it must exit with code N instead of 0;
    <!-- example: NAME target=function_tests [exit=N] -->
                                        ... a program in several files with two targets, of which only the test
                                        program function_tests is run (see below);
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
                                        a time. A broken stage=link program in several files passes only if every
                                        listed source compiles, only the link step of first_program fails, and
                                        REGEX matches that step's output;
    <!-- broken: NAME [in=PATH] at=LINE[:COLUMN] [errors=N] error=REGEX -->
                                        for a broken program in several files: it must FAIL TO COMPILE. PATH is
                                        main.cpp (the default) or one of its file blocks, a .cpp or a .hpp, and the
                                        program lists all of its .cpp files in add_executable. The first failed step
                                        of the build must compile one of its sources (not scan dependencies, not
                                        link), and the first compiler error of that step must be located in PATH, at
                                        LINE (and COLUMN), with a message matching REGEX; with errors=N, that step
                                        must report exactly N errors located in PATH. An error in a header is
                                        reported by the source that includes it, so in=PATH may name a header.

An example in several files may have a second target, function_tests: a test program built from the same sources as the
program. Its marker has target=function_tests (before exit=, never with source=), and its cmake block is the lesson 0.5
file with the sources of first_program, an empty line, and the same three lines for function_tests:
add_executable(function_tests SOURCES) and lesson 0.5's two property lines. first_program lists main.cpp, function_tests
lists the file block function_tests.cpp, and every other .cpp file of the program is listed by both; main.cpp includes a
header of the program, and function_tests.cpp at least one of the same headers (a shared interface, not a proof of what
the tests call). Both targets are built, and a failed step of either fails the example; then only function_tests is
run, once, with an empty standard input, against exactly one output block. Such an example has no input blocks, run
markers or data files, and a broken program never has two targets.

An example that reads a data file declares each of its runs with a run marker, anywhere in the lesson:

    <!-- run: NAME -->                  a line of its own, with no code block: it starts the next run of example NAME
                                        (runs are numbered from 1 in the order of their markers). The input,
                                        datafile and output blocks of NAME after it, up to NAME's next run marker,
                                        belong to that run, whatever blocks of other programs stand in between: at
                                        most one input block (without it, the run gets an empty standard input), at
                                        most one datafile block (without it, the run's folder is empty, so the file
                                        is missing), and exactly one output block;
    <!-- datafile: NAME PATH [noeol] --> the next ```text block is the file PATH that this run of NAME finds in its
                                        working directory: a lowercase name of at most 24 characters ending in .txt,
                                        with no folders. Each line of the block is written followed by one line end
                                        (LF), with no BOM and no other change: an empty block is an empty file, and a
                                        block of one empty line a file of one line end. noeol leaves out the final
                                        line end; it isn't allowed on an empty block or after an empty last line.
    Each run of such an example gets a new, empty folder (build/lesson-examples/<lesson>/<NAME>/run_N) as its working
    directory, holding only its own data file, and the folder is removed after the run, whatever its result. Such an
    example has all of its input and output blocks in its runs. An example without run markers runs exactly as above,
    in the checker's working directory, and can't have data files.

Checks:
  * every ```cpp block in a lesson is marked (Module 0 lessons predate the markers and are
    skipped unless marked; their project is checked by the other steps of the workflow), and a line that looks like a
    marker (a kind and a colon, however spaced or indented) is one exactly; other HTML comments are ordinary text;
  * every example has at least one output block, and every output block has an example;
  * marked blocks are ASCII only, and the Polish lesson (X.md) and the English one (X.en.md)
    contain the same marked blocks, with the same markers, in the same order, and the same run markers among them;
    data files are compared byte for byte;
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
  * a broken program must fail to build because of compiler errors in main.cpp (in a program in several files,
    in its file PATH), as described by its marker; with stage=link, it must compile and then fail in the linker,
    as above. Its whole build output is printed, to compare the messages across systems.

The lessons are never modified: everything is built in copies under build/lesson-examples.

Run from the repository root, with the official compiler:
    python3 tests/toolchains/lesson_examples.py --cxx /usr/bin/clang++-22 [--make-program /usr/bin/ninja]
Only part K of N of the lessons, for example to split the work between two CI jobs (every lesson is still read and
checked before building; part K builds and runs its own lessons only):
    python3 tests/toolchains/lesson_examples.py --cxx /usr/bin/clang++-22 --shard 1/2
Check that the checker itself detects mistakes (in a temporary folder):
    python3 tests/toolchains/lesson_examples.py --self-test --cxx /usr/bin/clang++-22
"""

import argparse
import contextlib
import io
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time

MARKER = re.compile(r'^<!-- (?:(example|output|input|broken|file|cmake|run|datafile): ([a-z0-9_]+)(.*?)|(fragment)) -->$')
SOURCE = re.compile(r'^(?: source=(\S+))?(?: target=(\S+))?(?: exit=(\d+))?$')
BROKEN = re.compile(r'^(?: stage=(link))?(?: in=(\S+))?(?: at=(\d+)(?::(\d+))?)?(?: errors=(\d+))? error=(.+)$')
FILE = re.compile(r'^ (\S+)$')
DATAFILE = re.compile(r'^ (\S+)(?: (noeol))?$')
# A line that means to be a marker: the name of a kind (or its plural) followed by a colon, or "fragment" followed by a
# colon or by the end of the comment, however spaced or indented. Such a line must be a marker exactly. Other HTML
# comments are ordinary text.
MARKER_LIKE = re.compile(r'^\s*<!--\s*(?:(?:example|output|input|broken|file|cmake|run|datafile)s?\s*:|fragment\s*(?::|-->))')
# Characters that end a line for str.splitlines() but not in a data file: they would split one line of data into two.
SPLITTING = re.compile('[\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]')
FENCE = re.compile(r'^```(\S*)$')
# The file name of a file block: lowercase, a letter first, .cpp or .hpp, at most 24 characters, no folders.
FILE_NAME = re.compile(r'^[a-z][a-z0-9_]{0,19}\.(?:cpp|hpp)$')
# The file name of a data file: the same rule, with .txt.
DATA_FILE_NAME = re.compile(r'^[a-z][a-z0-9_]{0,19}\.txt$')
# Device names that Windows reserves, even with an extension.
WINDOWS_DEVICES = {'con', 'prn', 'aux', 'nul', *(f'com{n}' for n in range(1, 10)), *(f'lpt{n}' for n in range(1, 10))}
ADD_EXECUTABLE = re.compile(r'^add_executable\(first_program((?: [^ ()]+)+)\)$')
# The second target of a program with two targets: the test program, the file of its main, and its add_executable line.
TEST_TARGET = 'function_tests'
TEST_MAIN = 'function_tests.cpp'
ADD_TEST_EXECUTABLE = re.compile(r'^add_executable\(function_tests((?: [^ ()]+)+)\)$')
DIRECTIVE = re.compile(r'^\s*#\s*([a-z_]+)')
INCLUDE = re.compile(r'^#include (?:<[^<>]+>|"([^"]*)")$')
CONDITIONALS = {'if', 'ifdef', 'ifndef', 'elif', 'elifdef', 'elifndef', 'else', 'endif'}
# A failed Ninja step: "FAILED: [code=1] OUTPUT ..." (Ninja 1.12 and newer) or "FAILED: OUTPUT ..." (older).
FAILED_STEP = re.compile(r'^FAILED: (?:\[code=\d+\] )?(\S+)')
STEP_START = re.compile(r'^(?:\[\d+/\d+\] |FAILED: |ninja: )')
# A compiler error in main.cpp: GNU style (main.cpp:4:35: error: ...) or MSVC style (main.cpp(4,35): error: ...).
ERROR = re.compile(r'main\.cpp(?::(\d+):(\d+):|\((\d+),(\d+)\):) error: (.*)')
# A compiler error in any file, in the same two styles: the file's name (after the last / or \), its line, column and
# message. Notes, "fatal error" and the "In file included from main.cpp:3:" lines before an error in a header don't match.
DIAGNOSTIC = re.compile(r'(?:^|[/\\])([^/\\\s:()]+)(?::(\d+):(\d+):|\((\d+),(\d+)\):) error: (.*)', re.MULTILINE)
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
    and the line numbers of unmarked ```cpp blocks. A run marker has no block: its language is None and its text ''.
    The text of a data file is its exact content: each line of the block followed by a line end, so an empty block is
    an empty file and a block of one empty line a file of one line end (noeol is applied later).
    An unreadable run or datafile marker is kept as ('unreadable', name, ...), so that its program isn't run."""
    raw = path.read_text(encoding='utf-8')
    lines = raw.splitlines()
    found, unmarked, marker, after_run, i = [], [], None, None, 0
    while i < len(lines):
        line = lines[i]
        match = MARKER.match(line)
        fence = FENCE.match(line)
        if after_run and line.strip():
            if fence:
                fail(f'{path}:{after_run}: run marker directly followed by a code block: '
                     'mark the block (input, datafile or output), or put text between them')
            after_run = None
        if match:
            if marker:
                fail(f'{path}:{marker[3]}: marker not followed by a code block')
            kind = match[1] or match[4]
            attributes = match[3] or ''
            pattern = (BROKEN if kind == 'broken' else SOURCE if kind == 'example' else FILE if kind == 'file'
                       else DATAFILE if kind == 'datafile' else re.compile('^$'))
            parsed = pattern.match(attributes)
            # A compile-stage broken program needs at=; a link-stage one has no file and line to point to,
            # and no compile errors to count, so it takes neither in=, at= nor errors=.
            if not parsed or (kind == 'broken' and (bool(parsed[1]) == bool(parsed[3]) or (parsed[1] and (parsed[2] or parsed[5])))):
                fail(f'{path}:{i + 1}: cannot read the {kind} marker{unsupported(kind, attributes)}: {line}')
                if kind in ('run', 'datafile'):
                    found.append(('unreadable', match[2], attributes, None, '', i + 1))
                kind = 'unreadable' if kind != 'run' else 'run_unreadable'
            if kind == 'run':
                # A run marker stands alone: it starts a run of its program, and no code block belongs to it.
                found.append(('run', match[2], '', None, '', i + 1))
                after_run = i + 1
                marker = None
            elif kind == 'run_unreadable':
                marker = None
            else:
                marker = (kind, match[2], attributes, i + 1)
        elif MARKER_LIKE.match(line):
            fail(f'{path}:{i + 1}: a line that looks like a marker but is not one: {line} '
                 '(a marker is a line of its own, not indented, exactly "<!-- KIND: NAME ... -->")')
            if marker:
                fail(f'{path}:{marker[3]}: marker not followed by a code block')
                marker = None
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
                expected = 'text' if kind in ('output', 'input', 'datafile') else 'cmake' if kind == 'cmake' else 'cpp'
                if language != expected:
                    fail(f'{path}:{start}: {kind} marker on a ```{language} block, expected ```{expected}')
                if kind == 'datafile':
                    text = ''.join(f'{body_line}\n' for body_line in body)
                found.append((kind, name, attributes, language, text, start))
            elif language == 'cpp':
                unmarked.append(start)
            marker = None
        elif line.strip() and marker:
            fail(f'{path}:{marker[3]}: marker not followed by a code block')
            marker = None
        i += 1
    data_files = [block for block in found if block[0] == 'datafile']
    if data_files and SPLITTING.search(raw):
        # These characters were already taken as line ends above, so a data file would silently get other bytes.
        for number, raw_line in enumerate(raw.split('\n'), 1):
            if SPLITTING.search(raw_line):
                fail(f'{path}:{number}: a control character that splits lines ({SPLITTING.search(raw_line)[0]!r}) '
                     'in a lesson with data files')
        # No program of this lesson runs with a data file that may not be the lesson's.
        found += [('unreadable', name, '', None, '', line) for _, name, _, _, _, line in data_files]
    return found, unmarked


def unsupported(kind, attributes):
    """Why an example or broken marker that can't be read asks for something this check doesn't support, or ''.
    For a broken marker only the part before error= counts: the regular expression after it may contain anything."""
    if kind == 'example' and re.search(r'(?:^| )target=', attributes):
        return f' (expected target={TEST_TARGET} [exit=N], in this order)'
    if kind != 'broken':
        return ''
    head = attributes.split(' error=', 1)[0]
    if re.search(r'(?:^| )target=', head):
        return ' (target= is only for an example: a broken program has one target)'
    stage = re.search(r'(?:^| )stage=(\S+)', head)
    if stage and stage[1] != 'link':
        return f' (stage={stage[1]} is not supported: a broken program can only fail to compile or, with stage=link, to link)'
    if re.search(r'(?:^| )in=', head):
        if stage:
            return ' (in= is not allowed with stage=link: a link error has no file and line to point to)'
        if not re.search(r'(?:^| )at=', head):
            return ' (in= needs at=: in= names the file of an expected compile error, at= its line)'
        return ' (expected in=PATH at=LINE[:COLUMN] [errors=N] error=REGEX, in this order)'
    return ''


def check_lesson(path, found):
    """Checks one lesson's markers; returns its examples, their runs, the broken programs, the runs of the programs with
    run markers, and the names of those programs that must not be run because of a problem found here.
    An example is (its code, its exit code, its target: None, or function_tests for a program with two targets).
    A run is (standard input, or None for none, [expected outputs]); a run of a program with run markers is
    (standard input or None, its data file as (name, bytes) or None, [its one expected output])."""
    examples, broken, targets = {}, {}, {}
    for kind, name, attributes, _, text, line in found:
        if not text.isascii():
            fail(f'{path}:{line}: non-ASCII text in a marked block')
        if kind in ('example', 'broken'):
            if name in examples or name in broken:
                fail(f'{path}:{line}: program {name} defined twice')
        if kind == 'example':
            source = SOURCE.match(attributes)
            target = source[2] if source else None
            examples[name] = (text, int(source[3]) if source and source[3] else 0, target)
            if target:
                targets[name] = (line, bool(source[1]))  # checked below, against the program's other blocks
            elif source and source[1]:
                original = (path.parent / source[1]).read_text(encoding='utf-8')
                if text != original:
                    fail(f'{path}:{line}: example {name} differs from {source[1]}')
                else:
                    print(f'ok   {path.name}: example {name} equals {source[1]}')
        elif kind == 'broken':
            expectation = BROKEN.match(attributes)
            if expectation:
                broken[name] = (text, expectation)
    folder_runs, refused = check_folder_runs(path, found, examples, broken)
    for name, (line, with_source) in targets.items():
        problem = target_problem(examples[name][2], with_source, [kind for kind, block_name, *_ in found if block_name == name])
        if problem:
            fail(f'{path}:{line}: example {name}: {problem}')
            refused.add(name)
    runs = {}
    for kind, name, _, _, text, line in found:
        if kind not in ('output', 'input'):
            continue
        if name in folder_runs or name in refused:
            continue  # a program with run markers, or with a data file: its blocks are checked above
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
        if name in folder_runs or name in refused:
            continue
        name_runs = runs.get(name, [])
        if not any(outputs for _, outputs in name_runs):
            fail(f'{path}: example {name} has no output block')
        elif any(data is not None for data, _ in name_runs) and name_runs[0][0] is None:
            fail(f'{path}: example {name}: an output block comes before its first input block')
        elif any(not outputs for _, outputs in name_runs):
            fail(f'{path}: example {name}: an input block has no output block after it')
    return examples, runs, broken, folder_runs, refused


def target_problem(target, with_source, kinds):
    """What is wrong with target=TARGET on an example whose blocks are of KINDS (WITH_SOURCE: its marker has source=
    too), or None. Its CMakeLists.txt and files are checked with the other programs in several files (check_projects)."""
    if target != TEST_TARGET:
        return f'unknown target {target} (an example can name only target={TEST_TARGET})'
    if with_source:
        return "target= can't be combined with source= (source= is for the lesson 0.5 main.cpp, a program with one target)"
    if 'file' not in kinds and 'cmake' not in kinds:
        return f'target={TEST_TARGET} is only for a program in several files with two targets'
    if any(kind in kinds for kind in ('input', 'run', 'datafile')):
        return (f'an example with target={TEST_TARGET} runs once, with an empty standard input: '
                'no input blocks, run markers or data files')
    if kinds.count('output') > 1:
        return f'an example with target={TEST_TARGET} has exactly one output block, not {kinds.count("output")}'
    return None


def check_folder_runs(path, found, examples, broken):
    """Checks the run, input, datafile and output blocks of the programs with run markers. Each run marker starts a run
    of its program; the program's input, datafile and output blocks after it, up to its next run marker, belong to that
    run, whatever the blocks of other programs in between. Returns ({NAME: [(standard input or None, data file as
    (name, bytes) or None, [expected output])]}, the names of programs with run markers that must not be run)."""
    with_runs = {name for kind, name, *_ in found if kind == 'run'}
    unreadable = {name for kind, name, *_ in found if kind == 'unreadable'}
    runs, refused = {}, set()

    def problem(name, message):
        fail(message)
        refused.add(name)

    for kind, name, attributes, language, text, line in found:
        if kind not in ('run', 'datafile') and not (kind in ('input', 'output') and name in with_runs):
            continue
        where = f'{path}:{line}: {kind} {name}'
        if kind != 'run' and language != 'text':
            refused.add(name)  # the fence is already reported
        if name not in examples:
            reason = 'a broken program is never run' if name in broken else f'no example {name} in this lesson'
            problem(name, f'{where}: {reason}')
            continue
        if name not in with_runs:
            problem(name, f'{where}: a data file belongs to a run: put "<!-- run: {name} -->" before it')
            continue
        name_runs = runs.setdefault(name, [])
        if kind == 'run':
            name_runs.append({'input': None, 'datafile': None, 'outputs': [], 'line': line})
            continue
        if not name_runs:
            problem(name, f'{where}: comes before the first run marker of {name} (a program with run markers has '
                          'all of its input, datafile and output blocks in its runs)')
            continue
        run = name_runs[-1]
        number = len(name_runs)
        if kind == 'input':
            if run['input'] is not None:
                problem(name, f'{where}: a second input block in run {number} of {name}')
            run['input'] = text
        elif kind == 'output':
            run['outputs'].append(text)
            if len(run['outputs']) == 2:
                problem(name, f'{where}: a second output block in run {number} of {name} (a run has exactly one)')
        else:
            file_name, noeol = DATAFILE.match(attributes).groups()
            reasons = data_file_problems(file_name, noeol, text)
            for reason in reasons:
                problem(name, f'{where}: {reason}')
            if run['datafile'] is not None:
                problem(name, f'{where}: a second data file in run {number} of {name} (a run has at most one)')
            elif not reasons:
                content = text[:-1] if noeol else text
                run['datafile'] = (file_name, content.encode('ascii'))
    for name, name_runs in runs.items():
        for number, run in enumerate(name_runs, 1):
            if not run['outputs']:
                problem(name, f'{path}:{run["line"]}: run {number} of {name} has no output block')
    refused |= unreadable & set(examples)
    return ({name: [(run['input'], run['datafile'], run['outputs']) for run in name_runs]
             for name, name_runs in runs.items() if name not in refused}, refused)


def data_file_problems(file_name, noeol, text):
    """What is wrong with a data file named FILE_NAME, with the TEXT of its block (each line followed by a line end)
    and noeol or not: a list of reasons, empty when it may be written."""
    reasons = []
    if not DATA_FILE_NAME.match(file_name):
        reasons.append(f'{file_name} is not a valid data-file name: lowercase letters, digits and _, starting with a '
                       'letter, ending in .txt, at most 24 characters, no folders')
    elif file_name.split('.')[0] in WINDOWS_DEVICES:
        reasons.append(f'{file_name} is a reserved name on Windows')
    if noeol and not text:
        reasons.append('noeol on an empty data file: there is no line end to remove')
    elif noeol and (text == '\n' or text.endswith('\n\n')):
        reasons.append('noeol after an empty last line: these bytes are written without noeol and without that line')
    bad = sorted({c for c in text if c not in '\t\n' and not ' ' <= c <= '~'})
    if bad:
        reasons.append(f'control characters in the data: {", ".join(repr(c) for c in bad)} (only printable ASCII, '
                       'spaces and tabs)')
    return reasons


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
        # A broken program with a compile error is built from all of its sources, as an example is, so that a source
        # left out can't hide where the error is. Only a stage=link program may leave one out.
        compile_error = name in broken and broken[name][1][1] != 'link'
        code = examples[name][0] if name in examples else broken[name][0]
        with_target = name in examples and examples[name][2] == TEST_TARGET
        problems = []
        if name not in cmakes:
            problems.append('it has file blocks but no cmake block (a program in several files has exactly one)')
        elif with_target or has_second_target(cmakes[name]):
            # The form with two targets: only for an example with target=function_tests, and the other way round.
            problems += two_target_problems(cmakes[name], program_files, code, name in examples, with_target)
        else:
            lists_all = 'an example' if name in examples else 'a broken program with a compile error' if compile_error else None
            problems += cmake_problems(cmakes[name], program_files, lists_all)
        if not program_files:
            problems.append('it has a cmake block but no file blocks '
                            '(show the CMakeLists.txt of a one-file program as an unmarked block)')
        if compile_error and broken[name][1][2]:
            problem = in_problem(broken[name][1][2], program_files)
            if problem:
                problems.append(problem)
        problems += include_problems(code, program_files)
        for problem in problems:
            fail(f'{path}: program {name}: {problem}')
        if problems or name in refused:
            refused.add(name)
        else:
            projects[name] = (program_files, cmakes[name])
    for name, (_, expectation) in broken.items():
        if expectation[2] and name not in files and name not in cmakes:
            fail(f'{path}: program {name}: in= is only for a program in several files '
                 '(the errors of a one-file program are always in main.cpp)')
            refused.add(name)
    return projects, refused


def in_problem(file_name, files):
    """What is wrong with in=FILE_NAME of a broken program in several files whose other files are FILES, or None."""
    if file_name == 'main.cpp' or file_name in files:
        return None
    real = {name.lower(): name for name in ['main.cpp', *files]}.get(file_name.lower())
    if real:
        return f'in={file_name} differs in case from {real}'
    if not FILE_NAME.match(file_name):
        return (f'in={file_name} is not a valid file name: main.cpp or the name of a file block of the program, '
                'ending in .cpp or .hpp, with no folders')
    return f'in={file_name} is not a file of the program'


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


def cmake_problems(text, files, lists_all):
    """What is wrong with the CMakeLists.txt of a program in several files: it must be the lesson 0.5 file with only
    the sources of add_executable(first_program ...) changed. No CMake code is interpreted. LISTS_ALL names the kind of
    program that must list all of its .cpp files, or is None for a broken stage=link program, which may leave some out."""
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
    problems = list_problems(sources, files)
    if 'main.cpp' not in sources:
        problems.append('add_executable must list main.cpp')
    if lists_all:
        for name in files:
            if name.endswith('.cpp') and name not in sources:
                problems.append(f'{name} is not in add_executable ({lists_all} lists all of its .cpp files; '
                                'leaving one out is allowed only in a broken stage=link program)')
    return problems


def list_problems(sources, files, command='add_executable'):
    """What is wrong with the SOURCES of one add_executable line (COMMAND in the messages): each listed once, no headers,
    only main.cpp and the .cpp files among FILES, written exactly as their names."""
    names = {name.lower(): name for name in ['main.cpp', *files]}
    problems = []
    for number, source in enumerate(sources):
        if source in sources[:number]:
            problems.append(f'{command} lists {source} twice')
        elif source.endswith('.hpp'):
            problems.append(f'{command} lists the header {source}: headers are not listed in add_executable')
        elif source == 'main.cpp' or (source in files and source.endswith('.cpp')):
            continue
        elif source.lower() in names:
            problems.append(f'{command} lists {source}, which differs in case from {names[source.lower()]}')
        else:
            problems.append(f'{command} lists {source}, which is not a .cpp file of the program '
                            '(CMake would stop at configuration, and stage=configure is not supported)')
    return problems


def has_second_target(text):
    """Whether the CMakeLists.txt TEXT means to have the second target: a line starts with add_executable(function_tests."""
    return any(line.startswith(f'add_executable({TEST_TARGET}') for line in text.splitlines())


def two_target_problems(text, files, code, example, with_target):
    """What is wrong with a program with two targets, whose CMakeLists.txt is TEXT, whose other files are FILES and whose
    main.cpp is CODE. EXAMPLE says whether it is an example (a broken program never has two targets), WITH_TARGET whether
    its marker has target=function_tests. The CMakeLists.txt must be the lesson 0.5 file with the sources of
    first_program, an empty line, and lesson 0.5's add_executable line and the lines after it, for function_tests. No
    CMake code is interpreted. first_program lists main.cpp, function_tests lists function_tests.cpp, and the other .cpp
    files of the program are the same in both, at least one. main.cpp includes a header of the program, and
    function_tests.cpp at least one of the same: that checks a shared interface, not which functions the tests call."""
    if not example:
        return [f'a broken program has one target (a CMakeLists.txt with two targets is for an example with '
                f'target={TEST_TARGET})']
    if not with_target:
        return [f'a CMakeLists.txt with two targets needs target={TEST_TARGET} on the example']
    if not has_second_target(text):
        return [f'target={TEST_TARGET} needs the CMakeLists.txt with two targets (the lesson 0.5 file, an empty line, '
                f'and the same three lines for {TEST_TARGET})']
    if TEST_MAIN not in files:
        return [f'target={TEST_TARGET} needs a file block {TEST_MAIN}, the file of the main function of the tests']
    template = PROJECT.read_text(encoding='utf-8').splitlines()
    at = next(i for i, line in enumerate(template) if line.startswith('add_executable('))
    first = re.search(r'add_executable\((\S+)', template[at])[1]
    model = template + [''] + [line.replace(f'({first} ', f'({TEST_TARGET} ') for line in template[at:]]
    second = len(template) + 1
    lines = text.splitlines()
    if any(line.startswith('add_executable(') and not line.endswith(')') for line in lines):
        return ['add_executable must list its sources on one line']
    if len(lines) != len(model) or any(line != expected for i, (line, expected) in enumerate(zip(lines, model))
                                       if i not in (at, second)):
        return [f'the cmake block differs from the CMakeLists.txt with two targets (the lesson 0.5 file with the sources '
                f'of {first}, an empty line, and the same three lines for {TEST_TARGET}, nothing else)']
    commands = ADD_EXECUTABLE.match(lines[at]), ADD_TEST_EXECUTABLE.match(lines[second])
    if not all(commands):
        return [f'the cmake block must have add_executable({first} SOURCES) and add_executable({TEST_TARGET} SOURCES), '
                'each on one line, with the sources separated by single spaces']
    program, tests = (command[1].split() for command in commands)
    problems = list_problems(program, files, f'add_executable({first} ...)')
    problems += list_problems(tests, files, f'add_executable({TEST_TARGET} ...)')
    if 'main.cpp' not in program:
        problems.append(f'add_executable({first} ...) must list main.cpp')
    if TEST_MAIN in program:
        problems.append(f'{first} must not list {TEST_MAIN} (it has its own main function)')
    if TEST_MAIN not in tests:
        problems.append(f'{TEST_TARGET} must list {TEST_MAIN}')
    if 'main.cpp' in tests:
        problems.append(f'{TEST_TARGET} must not list main.cpp (it has its own main function)')
    # The shared sources: the program's own .cpp files in each list, other than the two files of a main function.
    shared = [{source for source in sources if source in files and source.endswith('.cpp') and source != TEST_MAIN}
              for sources in (program, tests)]
    for source in sorted(shared[0] - shared[1]):
        problems.append(f'{source} is listed by {first} but not by {TEST_TARGET} '
                        '(the tests build from the same sources as the program)')
    for source in sorted(shared[1] - shared[0]):
        problems.append(f'{source} is listed by {TEST_TARGET} but not by {first} '
                        '(the tests build from the same sources as the program)')
    if not shared[0] | shared[1]:
        problems.append(f'{first} and {TEST_TARGET} share no .cpp file, so the tests are not built from the '
                        "program's implementation")
    for name in files:
        if name.endswith('.cpp') and name != TEST_MAIN and name not in program and name not in tests:
            problems.append(f'{name} is in neither add_executable (a program with two targets lists {TEST_MAIN} in '
                            f'{TEST_TARGET}, and each of its other .cpp files in both)')
    headers = local_headers(code, files)
    if not headers:
        problems.append('main.cpp includes no header of the program, so the two targets share no interface')
    elif not local_headers(files[TEST_MAIN], files) & headers:
        problems.append(f'{TEST_MAIN} includes none of the headers of the program that main.cpp includes '
                        f'({", ".join(sorted(headers))}), so the two targets share no interface')
    return problems


def local_headers(code, files):
    """The headers of the program (among FILES) that CODE includes with #include "name.hpp", outside comments. A header
    written with another case, or one that isn't a file of the program, isn't among them (include_problems reports it)."""
    found = set()
    for line in active_lines(code):
        form = INCLUDE.match(line.rstrip())
        if form and form[1] in files and form[1].endswith('.hpp'):
            found.add(form[1])
    return found


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


def failed_steps(output, two_targets=False):
    """Ninja's failed steps in a build OUTPUT, as (kind, what, the step's own output). The kind is 'scan' or 'compile'
    of a source (what is its file name), 'link' of the program, or 'other' (what is the step's output file).
    For a program with two targets (TWO_TARGETS), the link of either target is 'link' (what is the target's name), and
    what of a source's step names the target it is compiled for too: 'rules.cpp (target function_tests)'."""
    target = re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    steps, lines = [], None
    for line in output.splitlines():
        failed = FAILED_STEP.match(line)
        if failed:
            path = failed[1].replace('\\', '/')
            name = path.rsplit('/', 1)[-1]
            program = name[:-len('.exe')] if name.endswith('.exe') else name
            source = re.match(r'^(.+\.cpp)\.(?:o|obj)(\.ddi)?$', name)
            folder = re.search(r'(?:^|/)CMakeFiles/([^/]+)\.dir/', path)
            if source:
                kind, what = ('scan' if source[2] else 'compile'), source[1]
                if two_targets and folder:
                    what += f' (target {folder[1]})'
            elif two_targets and program in (target, TEST_TARGET):
                kind, what = 'link', program
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


def step_failure(kind, what, two_targets=False):
    """A failed step in words. In a program with two targets (TWO_TARGETS), a link names its target."""
    link = f'{what} failed to link' if two_targets else 'the program failed to link'
    return {'scan': f'{what} failed dependency scanning', 'compile': f'{what} failed to compile',
            'link': link}.get(kind, f'the build step {what} failed')


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


def executable(build_dir, target=None):
    """The program TARGET built in BUILD_DIR; by default the one target of the lesson 0.5 project, first_program."""
    target = target or re.search(r'add_executable\((\S+)', PROJECT.read_text(encoding='utf-8'))[1]
    return build_dir / (target + ('.exe' if sys.platform == 'win32' else ''))


def run_program(exe, data, timeout, cwd=None):
    """Runs EXE once, with DATA on standard input (None: an empty standard input), in the folder CWD (None: the
    checker's own working directory, as for every program without run markers).
    Returns (exit code, stdout bytes, stderr bytes, whether it timed out, the streams that went over OUTPUT_LIMIT).

    Each stream is read by its own thread while the program runs, so a program that fills one pipe never
    waits for the checker to read the other (the way subprocess.communicate reads on Windows). A thread
    keeps at most OUTPUT_LIMIT + 1 bytes: one byte more than allowed is proof enough, so it stops the
    program at once instead of collecting everything it would print."""
    # A pipe, not a terminal: the input is never echoed, so stdout is the program's output alone.
    # Without an input block the program gets an empty standard input, never the checker's own.
    with subprocess.Popen([str(exe)], stdin=subprocess.DEVNULL if data is None else subprocess.PIPE,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd) as process:
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


def check_example(lesson, name, code, exit_code, runs, args, project=None, folder_runs=None, target=None):
    """Builds example NAME and runs it once per run; returns the number of runs it started (0 if it didn't build).
    FOLDER_RUNS is None for a program without run markers (RUNS are its runs, in the checker's working directory), or
    the runs of a program with run markers, each run in a new folder of its own (check_folder_runs).
    TARGET is None, or function_tests for a program with two targets: the whole project is built, as always, so a failed
    step of either target fails the example, both programs must exist, and only TARGET is run."""
    built = build(lesson, name, code, args, project=project)
    if not built:
        return 0
    build_dir, result = built
    label = f'example {name} (target {target})' if target else f'example {name}'
    if result.returncode != 0:
        # A program in several files names its first failed step: a source that didn't compile, or the link.
        steps = failed_steps(result.stdout + result.stderr, bool(target)) if project else []
        reason = f': {step_failure(*steps[0][:2], bool(target))}' if steps else ''
        fail(f'{lesson}: {label}: build failed{reason}\n{result.stdout}{result.stderr}')
        return 0
    if target:
        missing = [exe.name for exe in (executable(build_dir), executable(build_dir, target)) if not exe.exists()]
        if missing:
            fail(f'{lesson}: {label}: the build succeeded, but {" and ".join(missing)} was not created')
            return 0
    exe = executable(build_dir, target)
    if folder_runs is not None:
        return run_in_folders(lesson, name, exe, exit_code, folder_runs, build_dir.parent, args)
    # The same program for every run: built once above, never rebuilt between inputs.
    for number, (data, expected) in enumerate(runs or [(None, [])], 1):
        run_label = label if data is None else f'example {name} (input {number} of {len(runs)})'
        judge_run(lesson, run_label, run_program(exe, data, args.timeout), exit_code, expected,
                  [f'       < {line}' for line in (data or '').splitlines()], args)
    return len(runs or [(None, [])])


def judge_run(lesson, label, result, exit_code, expected, details, args):
    """Reports one run of an example: its RESULT from run_program against EXIT_CODE and the EXPECTED outputs.
    On success, prints the DETAILS lines (the input, the data file) and then the output."""
    returncode, stdout, stderr, timed_out, over_limit = result
    if over_limit:
        for stream in over_limit:
            fail(f'{lesson}: {label}: {stream} exceeded the {OUTPUT_LIMIT}-byte limit, so the program was stopped')
        return
    if timed_out:
        fail(f'{lesson}: {label}: did not finish within {args.timeout} s')
        return
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
        return
    print(f'ok   {lesson}: {label} builds, runs, exits with {exit_code} '
          f'and prints the expected {len(expected)} output block(s):')
    for line in details:
        print(line)
    for line in out[:SHOWN_LIMIT].splitlines():
        print(f'       | {line}')
    if len(out) > SHOWN_LIMIT:
        print(f'       ({len(out) - SHOWN_LIMIT} more characters, not shown)')


def run_in_folders(lesson, name, exe, exit_code, runs, work, args):
    """Runs example NAME once per run marker, in order. Each run gets a new, empty folder WORK/run_N as its working
    directory, holding only that run's data file (if it has one), and the folder is removed after the run, whatever
    its result. Returns the number of runs."""
    # Started from another working directory, so by its absolute path: a relative one would be looked up from the
    # run's folder on Linux and macOS, and from the checker's own on Windows.
    exe = exe.resolve()
    for number, (data, data_file, expected) in enumerate(runs, 1):
        label = f'example {name} (run {number} of {len(runs)})'
        folder = work / f'run_{number}'
        result, removed = run_in_folder(exe, data, data_file, folder, args.timeout)
        if not removed:
            fail(f'{lesson}: {label}: its folder {folder} could not be removed after the run')
        if isinstance(result, str):
            fail(f'{lesson}: {label}: {result}')
            continue
        details = [f'       < {line}' for line in (data or '').splitlines()]
        if data_file is None:
            details.append('       (no data file in its folder)')
        else:
            file_name, content = data_file
            lines = content.count(b'\n') + (0 if content.endswith(b'\n') or not content else 1)
            ending = '' if content.endswith(b'\n') or not content else ', no line end after the last line'
            details.append(f'       data file {file_name}: {lines} line(s), {len(content)} byte(s){ending}')
        judge_run(lesson, label, result, exit_code, expected, details, args)
    return len(runs)


def run_in_folder(exe, data, data_file, folder, timeout):
    """Runs EXE once with standard input DATA (None: none) in FOLDER, created new and empty, holding only DATA_FILE
    ((name, bytes), or None for no file). FOLDER is removed afterwards, whatever happens.
    Returns (run_program's result, or a message why the program wasn't run; whether FOLDER was removed)."""
    shutil.rmtree(folder, ignore_errors=True)  # never a file of an earlier check
    try:
        folder.mkdir(parents=True)
        result = None
        if data_file is not None:
            target = folder / data_file[0]
            # The names were checked before; this makes sure that nothing is ever written outside the run's folder.
            if target.resolve().parent != folder.resolve():
                result = f'its data file {data_file[0]} would be written outside {folder}'
            else:
                target.write_bytes(data_file[1])  # bytes: no line ends are translated on any system
        if result is None:
            try:
                result = run_program(exe, data, timeout, cwd=folder)
            except OSError as error:
                result = f'could not be started: {error}'
    finally:
        removed = remove_folder(folder)
    return result, removed


def remove_folder(folder):
    """Removes FOLDER and everything in it. The program has ended by now, but on Windows a file can stay locked for a
    moment (a virus scanner, for example), so it tries a few times. Returns whether FOLDER is gone."""
    for attempt in range(5):
        shutil.rmtree(folder, ignore_errors=True)
        if not folder.exists():
            return True
        time.sleep(0.2 * (attempt + 1))
    return False


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
        check_link_failure(lesson, name, build_dir, output, found, expectation[6])
        return
    if not found:
        fail(f'{lesson}: broken program {name}: the build failed, but not with a compiler error in main.cpp\n{output}')
        return
    line, column, message = found[0]
    _, _, want_line, want_column, want_count, want_error = expectation.groups()
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
    """A broken stage=link program in several files: every source in add_executable compiled, and then only
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
        if not re.search(expectation[6], link_output, re.MULTILINE):
            problems.append(f"the link step's output has no match for {expectation[6]!r}")
    if problems:
        fail(f'{lesson}: broken program {name} (stage=link, several files): ' + '; '.join(problems) + f'\n{output}')
        return
    print(f'ok   {lesson}: broken program {name} compiles {", ".join(sources)} and fails to link as described')
    print('     build output:')
    for text in output.splitlines():
        print(f'       | {text}')


def check_project_compile(lesson, name, code, expectation, project, args):
    """A broken program in several files with a compile error: the first failed step of the build compiles one of its
    sources, and that step's first compiler error is located in the file in=PATH (main.cpp by default), as described.
    The build runs one job at a time and stops at that step, so only its own diagnostics are read: an error in a
    header is reported by the first source that includes it, never added up over several sources. A failed
    configuration, dependency scan or link is never taken for the expected compile error."""
    built = build(lesson, name, code, args, flags='', project=project)
    if not built:
        return
    build_dir, result = built
    output = result.stdout + result.stderr
    if result.returncode == 0:
        fail(f'{lesson}: broken program {name} builds, but the lesson says it must not')
        return
    steps = failed_steps(output)
    want_path = expectation[2] or 'main.cpp'
    _, _, want_line, want_column, want_count, want_error = expectation.groups()
    problems = []
    if not steps:
        problems.append('the build failed, but no failed step was found in its output')
    elif steps[0][0] == 'scan':
        problems.append(f'{steps[0][1]} failed dependency scanning, before compiling (a scan error is not a compile error)')
    elif steps[0][0] == 'link':
        problems.append('the program failed to link, so every source compiled without errors')
    elif steps[0][0] != 'compile':
        problems.append(f'{step_failure(*steps[0][:2])}, not a compile step')
    if problems:
        fail(f'{lesson}: broken program {name} (in={want_path}): ' + '; '.join(problems) + f'\n{output}')
        return
    source, step_output = steps[0][1], steps[0][2]
    found = [(m[1], int(m[2] or m[4]), int(m[3] or m[5]), m[6]) for m in DIAGNOSTIC.finditer(step_output)]
    if not found:
        fail(f'{lesson}: broken program {name} (in={want_path}): {source} failed to compile, '
             f'but with no compiler error that names a file and a line\n{output}')
        return
    file_name, line, column, message = found[0]
    in_path = [error for error in found if error[0] == want_path]
    if file_name != want_path:
        problems.append(f'the first error when compiling {source} is in {file_name} at {line}:{column}, expected in {want_path}')
    else:
        if line != int(want_line) or (want_column and column != int(want_column)):
            problems.append(f'first error at {line}:{column}, expected {want_line}' + (f':{want_column}' if want_column else ''))
        if not re.search(want_error, message):
            problems.append(f'first error says {message!r}, expected a match for {want_error!r}')
    if want_count and len(in_path) != int(want_count):
        problems.append(f'{len(in_path)} errors in {want_path} when compiling {source}, expected {want_count}')
    if problems:
        fail(f'{lesson}: broken program {name} (in={want_path}): ' + '; '.join(problems) + f'\n{output}')
        return
    print(f'ok   {lesson}: broken program {name} fails to compile {source} as described: {len(in_path)} error(s) '
          f'in {want_path}, the first at {line}:{column}: {message}')
    print('     build output:')
    for text in output.splitlines():
        print(f'       | {text}')


def check_course(args):
    """Checks every lesson under course/ in the current folder; returns the number of problems.
    With args.shard = (K, N), every lesson is still read and checked before building (PL/EN, markers, names, files),
    but only the lessons of part K of N are built and run: the checked lessons in sorted order, numbered from 0, go
    to part (number % N) + 1. So every lesson is in exactly one part, and a new lesson needs no configuration."""
    errors.clear()
    lessons = sorted(p for p in pathlib.Path('course').rglob('*.md') if not p.name.endswith('.en.md'))
    shard = getattr(args, 'shard', None)
    # For each part: [lessons, examples, broken programs, runs] it builds and runs, counted before building.
    parts = [[0, 0, 0, 0] for _ in range(shard[1])] if shard else []
    built_examples = built_broken = started_runs = 0
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
        # Run markers and data files are compared too: the same runs, the same file names and the same bytes.
        pl_marked = [(kind, name, attributes, text) for kind, name, attributes, _, text, _ in pl_blocks]
        en_marked = [(kind, name, attributes, text) for kind, name, attributes, _, text, _ in en_blocks]
        run_markers = sum(1 for block in pl_blocks if block[0] == 'run')
        if pl_marked != en_marked:
            fail(f'{pl}: the marked code blocks differ between {pl.name} and {en.name}')
        else:
            also = f', and so are their {run_markers} run markers' if run_markers else ''
            print(f'ok   {len(pl_marked) - run_markers} marked blocks are identical in {pl.name} and {en.name}{also}')
        examples, runs, broken, folder_runs, refused_runs = check_lesson(pl, pl_blocks)
        projects, refused = check_projects(pl, pl_blocks, examples, broken)
        refused |= refused_runs
        if en.exists():
            en_examples, _, en_broken, _, _ = check_lesson(en, en_blocks)
            check_projects(en, en_blocks, en_examples, en_broken)
        fragments = sum(1 for block in pl_blocks if block[0] == 'fragment')
        inputs = sum(1 for block in pl_blocks if block[0] == 'input')
        print(f'     {len(examples)} examples to build and run ({inputs} runs with standard input), '
              f'{len(broken)} broken programs that must not compile, '
              f'{fragments} fragments (deliberately incomplete, not built)')
        if folder_runs:
            in_folders = sum(len(name_runs) for name_runs in folder_runs.values())
            with_files = sum(1 for name_runs in folder_runs.values() for _, data_file, _ in name_runs if data_file)
            print(f'     {len(folder_runs)} of these examples with run markers: {in_folders} runs, each in a folder of its own, '
                  f'{with_files} of them with a data file')
        if projects or refused:
            print(f'     {len(projects)} of these programs in several files (file and cmake blocks), '
                  f'{len(refused)} not built because of the problems above')
        with_tests = sum(1 for name in projects if name in examples and examples[name][2] and name not in refused)
        if with_tests:
            print(f'     {with_tests} of these programs with two targets (both built, {TEST_TARGET} run)')
        if shard:
            part = (checked - 1) % shard[1] + 1
            counts = parts[part - 1]
            counts[0] += 1
            counts[1] += sum(1 for name in examples if name not in refused)
            counts[2] += sum(1 for name in broken if name not in refused)
            counts[3] += sum(len(folder_runs.get(name) or runs.get(name) or [None]) for name in examples if name not in refused)
            if part != shard[0]:
                print(f'     part {part} of {shard[1]}: built and run by that part, not by this one ({shard[0]} of {shard[1]})')
                continue
            print(f'     part {part} of {shard[1]}: built and run here')
        # Programs without file and cmake blocks take the same path as before.
        for name, (code, exit_code, target) in examples.items():
            if name not in refused:
                built_examples += 1
                started_runs += check_example(pl.stem, name, code, exit_code, runs.get(name, []), args, projects.get(name),
                                              folder_runs.get(name), target)
        for name, (code, expectation) in broken.items():
            if name not in refused:
                built_broken += 1
            if name in projects and expectation[1] == 'link':
                check_project_link(pl.stem, name, code, expectation, projects[name], args)
            elif name in projects:
                check_project_compile(pl.stem, name, code, expectation, projects[name], args)
            elif name not in refused:
                check_broken(pl.stem, name, code, expectation, args)
    if checked == 0:
        fail('no lesson contains marked examples')
    if not shard:
        print(f'{"PASSED" if not errors else "FAILED"}: {checked} lesson(s), {len(errors)} problem(s)')
        return len(errors)
    for number, (count, examples_count, broken_count, runs_count) in enumerate(parts, 1):
        print(f'part {number} of {shard[1]}: {count} lesson(s), {examples_count} example(s), '
              f'{broken_count} broken program(s), {runs_count} run(s)')
    if parts[shard[0] - 1][0] == 0:
        fail(f'part {shard[0]} of {shard[1]} has no lessons to build: use fewer parts')
    print(f'{"PASSED" if not errors else "FAILED"}: part {shard[0]} of {shard[1]}: {len(lessons)} lesson file(s) read, '
          f'{checked} lesson(s) checked before building, {parts[shard[0] - 1][0]} of them built and run in this part '
          f'({built_examples} example(s), {built_broken} broken program(s), {started_runs} run(s)), {len(errors)} problem(s)')
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
# The compile error of tools.cpp without the semicolon after "value * 2": line 4, column 21.
TOOLS_ERROR = "broken: twice in=tools.cpp at=4:21 errors=1 error=^expected ';' after return statement$"
# A type in a header without #pragma once, and a main.cpp that includes it twice: Record is defined twice in one
# translation unit, and the error is located in record.hpp, though only main.cpp is compiled.
RECORD_HPP = 'struct Record {\n    int id{0};\n    int points{0};\n};\n'
RECORD_MAIN = ('#include <iostream>\n\n#include "record.hpp"\n#include "record.hpp"\n\nint main() {\n    Record record{7, 12};\n\n'
               '    std::cout << "Record " << record.id << ": " << record.points << "\\n";\n}\n')
# A header that uses Record without including record.hpp: main.cpp includes record.hpp first and compiles, but
# report.cpp, which includes only report.hpp, fails, with the first error located in report.hpp.
REPORT_HPP = '#pragma once\n\nint doubled_points(Record record);\n'
REPORT_CPP = '#include "report.hpp"\n\nint doubled_points(Record record) {\n    return record.points * 2;\n}\n'
REPORT_MAIN = ('#include <iostream>\n\n#include "record.hpp"\n#include "report.hpp"\n\nint main() {\n    Record record{7, 12};\n\n'
               '    std::cout << "Doubled: " << doubled_points(record) << "\\n";\n}\n')


# Reads data.txt as bytes and prints how many there are, their sum and the last one (-1: none), or that it can't open
# the file. bytes_output() is what it prints for CONTENT (None: no file).
BYTES = ('#include <fstream>\n#include <iostream>\n\nint main() {\n    std::ifstream input{"data.txt", std::ios::binary};\n\n'
         '    if (input.fail()) {\n        std::cout << "Cannot open data.txt\\n";\n        return 0;\n    }\n\n'
         '    int size{0};\n    int sum{0};\n    int last{-1};\n    char c{};\n\n    while (input.get(c)) {\n        ++size;\n'
         '        sum += c;\n        last = c;\n    }\n\n'
         '    std::cout << "Bytes: " << size << ", sum: " << sum << ", last: " << last << "\\n";\n}\n')
# A program in several files that prints the name of its working directory, the files in it, and the lines of steps.txt.
LISTING_MAIN = '#include "listing.hpp"\n\nint main() {\n    print_folder();\n}\n'
LISTING_HPP = '#pragma once\n\nvoid print_folder();\n'
LISTING_CPP = ('#include "listing.hpp"\n\n#include <algorithm>\n#include <filesystem>\n#include <fstream>\n#include <iostream>\n'
               '#include <string>\n#include <vector>\n\nvoid print_folder() {\n    std::vector<std::string> names{};\n\n'
               '    for (const std::filesystem::directory_entry& entry : std::filesystem::directory_iterator{"."}) {\n'
               '        names.push_back(entry.path().filename().string());\n    }\n\n    std::sort(names.begin(), names.end());\n'
               '    std::cout << "Folder: " << std::filesystem::current_path().filename().string() << "\\n";\n'
               '    std::cout << "Files:";\n\n    for (const std::string& name : names) {\n        std::cout << " " << name;\n    }\n\n'
               '    std::cout << "\\n";\n    std::ifstream input{"steps.txt"};\n    std::string line{};\n\n'
               '    while (std::getline(input, line)) {\n        std::cout << "Line: " << line << "\\n";\n    }\n}\n')
# Reads a file name from standard input (data.txt when there is none) and prints the first line of that file.
NAMED_FILE = ('#include <fstream>\n#include <iostream>\n#include <string>\n\nint main() {\n    std::string file_name{};\n'
              '    std::getline(std::cin, file_name);\n\n    if (std::cin.fail()) {\n        std::cout << "No standard input\\n";\n'
              '        file_name = "data.txt";\n    }\n\n    std::ifstream input{file_name};\n\n    if (input.fail()) {\n'
              '        std::cout << "Cannot open " << file_name << "\\n";\n        return 0;\n    }\n\n    std::string line{};\n'
              '    std::getline(input, line);\n    std::cout << file_name << ": " << line << "\\n";\n}\n')
# Reads a number, and tells whether a folder named course is in its working directory (it is in the checker's own).
WHERE = ('#include <filesystem>\n#include <iostream>\n\nint main() {\n    int value{0};\n    std::cin >> value;\n'
         '    std::cout << "Value: " << value << ", course folder here: " << (std::filesystem::exists("course") ? "yes" : "no")'
         ' << "\\n";\n}\n')
# A program with two targets: first_program (main.cpp) and the test program function_tests (function_tests.cpp), both
# built from rules.cpp, declared in rules.hpp. The tests print PASS or FAIL per check and exit with 1 if one failed.
RULES_HPP = '#pragma once\n\nint parking_fee(int hours);\n'
RULES_CPP = ('#include "rules.hpp"\n\nint parking_fee(int hours) {\n    if (hours < 0 || hours > 8) {\n        return -1;\n'
             '    }\n\n    if (hours == 0) {\n        return 0;\n    }\n\n    return 5 + 3 * (hours - 1);\n}\n')
# Each further hour costs 2 instead of 3: parking_fee(2) is 7 and parking_fee(8) is 19.
RULES_BUG = RULES_CPP.replace('5 + 3 *', '5 + 2 *')
# The definition of parking_fee alone, without the #include line: a copy for the test program.
PARKING_FEE_COPY = RULES_CPP.split('\n', 2)[2]
PARKING_MAIN = ('#include <iostream>\n\n#include "rules.hpp"\n\nint main() {\n    int hours{0};\n    std::cin >> hours;\n\n'
                '    if (std::cin.fail()) {\n        std::cout << "Input error\\n";\n        return 0;\n    }\n\n'
                '    const int fee{parking_fee(hours)};\n\n    if (fee < 0) {\n        std::cout << "Invalid hours\\n";\n'
                '        return 0;\n    }\n\n    std::cout << "Fee: " << fee << "\\n";\n}\n')
PARKING_TESTS = ('#include <iostream>\n#include <string>\n\n#include "rules.hpp"\n\n'
                 'void check_int(const std::string& name, int expected, int actual, int& checks, int& failed) {\n'
                 '    ++checks;\n\n    if (actual == expected) {\n        std::cout << "PASS " << name << "\\n";\n'
                 '    } else {\n        std::cout << "FAIL " << name << ": expected " << expected << ", actual " << actual'
                 ' << "\\n";\n        ++failed;\n    }\n}\n\nint main() {\n    int checks{0};\n    int failed{0};\n\n'
                 + ''.join(f'    check_int("parking_fee({hours})", {fee}, parking_fee({hours}), checks, failed);\n'
                           for hours, fee in ((-1, -1), (0, 0), (1, 5), (2, 8), (8, 26), (9, -1)))
                 + '\n    std::cout << "Checks: " << checks << ", failed: " << failed << "\\n";\n\n'
                 '    if (failed > 0) {\n        return 1;\n    }\n\n    return 0;\n}\n')
PARKING_PASS = ''.join(f'PASS parking_fee({hours})\n' for hours in (-1, 0, 1, 2, 8, 9)) + 'Checks: 6, failed: 0\n'
PARKING_FAIL = ('PASS parking_fee(-1)\nPASS parking_fee(0)\nPASS parking_fee(1)\nFAIL parking_fee(2): expected 8, actual 7\n'
                'FAIL parking_fee(8): expected 26, actual 19\nPASS parking_fee(9)\nChecks: 6, failed: 2\n')
CHECK_HPP = ('#pragma once\n\n#include <string>\n\n'
             'void check_int(const std::string& name, int expected, int actual, int& checks, int& failed);\n')
# Two main functions in one program, in the wording of GNU ld, lld-link and Apple's ld.
DUPLICATE_MAIN = "multiple definition of .main'|duplicate symbol: main\\b|duplicate symbol '_main' in:"


def bytes_output(content):
    if content is None:
        return 'Cannot open data.txt\n'
    return f'Bytes: {len(content)}, sum: {sum(content)}, last: {content[-1] if content else -1}\n'


def lesson(*parts):
    """A fixture lesson made of (marker, language, code) parts. A part with no language is a marker alone (a run
    marker), and a part with no marker is text as it is."""
    return ''.join(code if marker is None else f'<!-- {marker} -->\n\n' if language is None
                   else f'<!-- {marker} -->\n```{language}\n{code}```\n\n' for marker, language, code in parts)


def run_parts(name, output, data=None, file_name='data.txt', noeol=False, stdin=None):
    """The parts of one run of program NAME: its run marker, its input and data file (if any) and its output."""
    parts = [(f'run: {name}', None, '')]
    if stdin is not None:
        parts.append((f'input: {name}', 'text', stdin))
    if data is not None:
        parts.append((f'datafile: {name} {file_name}{" noeol" if noeol else ""}', 'text', data))
    return parts + [(f'output: {name}', 'text', output)]


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

    def record(owner, hpp=RECORD_HPP):
        """The parts of program record: main.cpp and record.hpp, with the lesson 0.5 add_executable."""
        return [(owner, 'cpp', RECORD_MAIN), ('file: record record.hpp', 'cpp', hpp), ('cmake: record', 'cmake', template)]

    no_semicolon = TOOLS_CPP.replace('* 2;', '* 2')
    report = [("broken: report in=report.hpp at=3:20 errors=1 error=^unknown type name 'Record'$", 'cpp', REPORT_MAIN),
              ('file: report record.hpp', 'cpp', '#pragma once\n\n' + RECORD_HPP), ('file: report report.hpp', 'cpp', REPORT_HPP),
              ('file: report report.cpp', 'cpp', REPORT_CPP),
              ('cmake: report', 'cmake', template.replace('main.cpp)', 'main.cpp report.cpp)'))]
    wrong_details = ("broken: twice in=tools.cpp at=4:20 errors=2 error=^expected '\\)'",
                     "first error at 4:21, expected 4:20; first error says \"expected ';' after return statement\", "
                     "expected a match for \"^expected '\\\\)'\"; 1 errors in tools.cpp when compiling tools.cpp, expected 2")

    twice_runs = [('input: twice', 'text', '4\n'), ('output: twice', 'text', 'Twice: 8\n'),
                  ('input: twice', 'text', '-3\n'), ('output: twice', 'text', 'Twice: -6\n')]
    twice = program() + twice_runs
    # Programs that read a data file. bytes_cases: (the file's exact bytes, or None for no file; noeol).
    bytes_cases = [(b'Alpha\n', False), (b'Alpha', True), (b'', False), (b'\n', False), (b'Alpha\n\n', False),
                   (b' a\tb \n', False), (None, False)]
    bytes_runs = [part for content, noeol in bytes_cases
                  for part in run_parts('bytes', bytes_output(content),
                                        None if content is None else content.decode('ascii') + ('\n' if noeol else ''),
                                        noeol=noeol)]
    listing = [('example: listing', 'cpp', LISTING_MAIN), ('file: listing listing.hpp', 'cpp', LISTING_HPP),
               ('file: listing listing.cpp', 'cpp', LISTING_CPP),
               ('cmake: listing', 'cmake', template.replace('main.cpp)', 'main.cpp listing.cpp)'))]
    bad_names = ['Steps.txt', '../steps.txt', 'con.txt', 'steps.csv', 'steps', 'abcdefghijklmnopqrstu.txt', 'my steps.txt']
    misused = [('data.txt noeol', '', 'text'), ('data.txt noeol', 'Alpha\n\n', 'text'), ('data.txt noeol noeol', 'x\n', 'text'),
               ('data.txt eol', 'x\n', 'text'), ('noeol data.txt', 'x\n', 'text'), ('data.txt', 'x\n', 'cpp')]
    structure = [
        ('example: s_1', 'cpp', GOOD), ('datafile: s_1 data.txt', 'text', 'x\n'), ('output: s_1', 'text', 'Hi!\n'),
        ('example: s_2', 'cpp', GOOD), ('output: s_2', 'text', 'Hi!\n'), *run_parts('s_2', 'Hi!\n'),
        ('example: s_3', 'cpp', GOOD), ('run: s_3', None, ''), (None, None, '```text\nx\n```\n\n'),
        ('example: s_4', 'cpp', GOOD), *run_parts('s_4', 'Hi!\n'), ('output: s_4', 'text', 'Hi!\n'),
        ('example: s_5', 'cpp', READ_INT), ('run: s_5', None, ''), ('input: s_5', 'text', '1\n'), ('input: s_5', 'text', '2\n'),
        ('output: s_5', 'text', 'Count: 1\n'),
        ('example: s_6', 'cpp', GOOD), ('run: s_6', None, ''), ('datafile: s_6 a.txt', 'text', 'x\n'),
        ('datafile: s_6 b.txt', 'text', 'y\n'), ('output: s_6', 'text', 'Hi!\n'),
        ("broken: s_7 at=4 errors=1 error=expected ';'", 'cpp', NO_SEMICOLON), *run_parts('s_7', 'Hi!\n'),
        *run_parts('s_8', 'Hi!\n'),
    ]
    marker_like = ['<!-- datafiles: hi data.txt -->', '<!--run: hi-->', '  <!-- run: hi -->', '<!-- output : hi -->',
                   '<!-- fragment: x -->', '<!--fragment-->']
    # Programs with two targets. Their cmake block is written out in full, so the checker's own form, derived from the
    # lesson 0.5 file, is compared with it.
    cmake_tests = ('cmake_minimum_required(VERSION 3.28)\nproject(first_program LANGUAGES CXX)\n\n'
                   'add_executable(first_program main.cpp rules.cpp)\ntarget_compile_features(first_program PRIVATE cxx_std_20)\n'
                   'set_target_properties(first_program PROPERTIES CXX_EXTENSIONS OFF)\n\n'
                   'add_executable(function_tests function_tests.cpp rules.cpp)\n'
                   'target_compile_features(function_tests PRIVATE cxx_std_20)\n'
                   'set_target_properties(function_tests PROPERTIES CXX_EXTENSIONS OFF)\n')

    def two_lists(program='main.cpp rules.cpp', tests='function_tests.cpp rules.cpp'):
        """The cmake block with two targets, with other sources of first_program or function_tests."""
        return (cmake_tests.replace('(first_program main.cpp rules.cpp)', f'(first_program {program})')
                .replace('(function_tests function_tests.cpp rules.cpp)', f'(function_tests {tests})'))

    def parking(name='parking', marker=' target=function_tests', owner='example', main=PARKING_MAIN, cpp=RULES_CPP,
                tests=PARKING_TESTS, cmake=cmake_tests, output=PARKING_PASS, extra=()):
        """The parts of program NAME with two targets, with some of them replaced, rules.cpp left out when CPP is None,
        more file blocks EXTRA ((name, text)), and no output block when OUTPUT is None."""
        parts = [(f'{owner}: {name}{marker}', 'cpp', main), (f'file: {name} rules.hpp', 'cpp', RULES_HPP)]
        if cpp is not None:
            parts.append((f'file: {name} rules.cpp', 'cpp', cpp))
        parts += [(f'file: {name} function_tests.cpp', 'cpp', tests), *[(f'file: {name} {file_name}', 'cpp', text)
                                                                        for file_name, text in extra]]
        parts.append((f'cmake: {name}', 'cmake', cmake))
        return parts + ([(f'output: {name}', 'text', output)] if output is not None else [])

    with_copy = PARKING_TESTS.replace('#include "rules.hpp"\n\n', '#include "rules.hpp"\n\n' + PARKING_FEE_COPY + '\n')
    # A copy that doesn't clash with rules.cpp: static, in a file that doesn't include rules.hpp.
    static_copy = PARKING_TESTS.replace('#include "rules.hpp"\n\n', 'static ' + PARKING_FEE_COPY + '\n')
    two_target_form = 'the cmake block differs from the CMakeLists.txt with two targets'
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
        # This program used to be refused as not supported; now it is built, and its build must fail.
        ('a compile-stage broken program in several files that builds is detected',
         lesson(*program(owner="broken: twice at=4 errors=1 error=expected ';'")), None,
         'builds, but the lesson says it must not'),
        ('#ifndef in a program in several files is reported, and nothing is built',
         lesson(*program(hpp='#ifndef TOOLS_HPP\n#define TOOLS_HPP\n\nint twice(int value);\n\n#endif\n'), *twice_runs), None,
         'conditional preprocessor directives are not supported'),
        ('a broken marker with in= in a one-file program is refused, and nothing is built',
         lesson(("broken: no_semicolon in=main.cpp at=4 errors=1 error=expected ';'", 'cpp', NO_SEMICOLON)), None,
         'in= is only for a program in several files'),
        # in= of a broken program in several files, checked before anything is built.
        ('a broken marker with in= and stage=link is reported, and nothing is built',
         lesson(*program(owner='broken: twice stage=link in=tools.cpp error=twice')), None,
         'in= is not allowed with stage=link'),
        ('a broken marker with in= but without at= is reported, and nothing is built',
         lesson(*program(owner="broken: twice in=tools.cpp errors=1 error=expected ';'", cpp=no_semicolon)), None,
         'in= needs at='),
        ('a broken marker with in= and an unreadable at= is reported, and nothing is built',
         lesson(*program(owner="broken: twice in=tools.cpp at=4: error=expected ';'", cpp=no_semicolon)), None,
         'expected in=PATH at=LINE[:COLUMN] [errors=N] error=REGEX, in this order'),
        ('a broken marker with in= after at= is reported, and nothing is built',
         lesson(*program(owner="broken: twice at=4 in=tools.cpp error=expected ';'", cpp=no_semicolon)), None,
         'expected in=PATH at=LINE[:COLUMN] [errors=N] error=REGEX, in this order'),
        # The other program has no cmake block, so it is refused too, and nothing at all is built.
        ('in= naming a file of another program is reported, and nothing is built',
         lesson(*program(owner="broken: twice in=other.hpp at=3 error=expected", cpp=no_semicolon),
                ('example: other', 'cpp', GOOD), ('output: other', 'text', 'Hi!\n'), ('file: other other.hpp', 'cpp', TOOLS_HPP)),
         None, 'in=other.hpp is not a file of the program'),
        ('in= with a folder is reported, and nothing is built',
         lesson(*program(owner="broken: twice in=src/tools.cpp at=4 error=expected", cpp=no_semicolon)), None,
         'in=src/tools.cpp is not a valid file name'),
        ('in= with an extension other than .cpp and .hpp is reported, and nothing is built',
         lesson(*program(owner="broken: twice in=tools.h at=4 error=expected", cpp=no_semicolon)), None,
         'in=tools.h is not a valid file name'),
        ('in= with another case is reported, and nothing is built',
         lesson(*program(owner="broken: twice in=Tools.cpp at=4 error=expected", cpp=no_semicolon)), None,
         'in=Tools.cpp differs in case from tools.cpp'),
        ('a broken program with a compile error that leaves a source out of add_executable is reported, and nothing is built',
         lesson(*program(owner=TOOLS_ERROR, cpp=no_semicolon, cmake=template)), None,
         'tools.cpp is not in add_executable (a broken program with a compile error lists all of its .cpp files'),
        ('a missing header is still refused in a broken program with a compile error, and nothing is built',
         lesson(*program(owner="broken: twice at=3 error=file not found", main=TWICE_MAIN.replace('"tools.hpp"', '"tool.hpp"'))),
         None, '#include "tool.hpp" is not a file of the program'),
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
        # Compile errors in a program in several files (in=), really built.
        ('a compile error in a second .cpp file fails as described (in=tools.cpp)',
         lesson(*program(owner=TOOLS_ERROR, cpp=no_semicolon)), None, None),
        ('a compile error in a second .cpp file expected in main.cpp is detected',
         lesson(*program(owner="broken: twice in=main.cpp at=4 error=expected ';'", cpp=no_semicolon)), None,
         'the first error when compiling tools.cpp is in tools.cpp at 4:21, expected in main.cpp'),
        ('a different column, message and number of errors in a second .cpp file are detected',
         lesson(*program(owner=wrong_details[0], cpp=no_semicolon)), None, wrong_details[1]),
        # Both sources include the broken header; tools.cpp is listed first, so it is compiled, and fails, first.
        ('an error in a header included by two sources fails as described, reported by the first source compiled (in=tools.hpp)',
         lesson(*program(owner="broken: twice in=tools.hpp at=3:21 errors=1 error=^expected ';' after top level declarator$",
                         hpp=TOOLS_HPP.replace('value);', 'value)'), cmake=with_sources('tools.cpp main.cpp'))), None, None),
        ('a type defined twice in one translation unit fails as described (in=record.hpp)',
         lesson(*record("broken: record in=record.hpp at=1:8 errors=1 error=^redefinition of 'Record'$")), None, None),
        # "In file included from .../main.cpp:4:" stands just before the error, but the error is located in record.hpp.
        ('an error in a header is not taken for an error at its #include line (in=main.cpp)',
         lesson(*record("broken: record in=main.cpp at=4 error=redefinition")), None,
         'the first error when compiling main.cpp is in record.hpp at 1:8, expected in main.cpp'),
        ('an error on another line of a header is detected',
         lesson(*record("broken: record in=record.hpp at=2 error=redefinition")), None, 'first error at 1:8, expected 2'),
        ('a header included twice with #pragma once builds and runs',
         lesson(*record('example: record', hpp='#pragma once\n\n' + RECORD_HPP), ('output: record', 'text', 'Record 7: 12\n')),
         None, None),
        ('a header that uses a type without including its header fails as described (in=report.hpp)',
         lesson(*report), None, None),
        ('an expected compile error that is really a dependency-scanning error is detected',
         lesson(*program(owner='broken: twice in=tools.cpp at=1:10 error=file not found',
                         cpp='#include <no_such_header>\n' + TOOLS_CPP)), None,
         'tools.cpp failed dependency scanning, before compiling'),
        ('an expected compile error that is really a link error is detected',
         lesson(*program(owner='broken: twice in=tools.cpp at=3 error=twice',
                         cpp=TOOLS_CPP.replace('int twice(int value) {', 'int twice_value(int value) {'))), None,
         'the program failed to link, so every source compiled without errors'),
        ('a broken environment is not taken for the expected compile error of a program in several files',
         lesson(*program(owner=TOOLS_ERROR, cpp=no_semicolon)), None, 'configure failed (an environment problem'),
        ('a different in= in PL and EN is detected',
         lesson(*program(owner=TOOLS_ERROR, cpp=no_semicolon)),
         lesson(*program(owner=TOOLS_ERROR.replace('in=tools.cpp', 'in=main.cpp'), cpp=no_semicolon)), 'differ between'),
        # Programs that read a data file: runs declared with run markers, each in a folder of its own.
        ('a program sees the exact bytes of its data file in each run (a line end, noeol, an empty file, one empty line, '
         'an empty last line, spaces and a tab), and no file when its run has none',
         lesson(('example: bytes', 'cpp', BYTES), *bytes_runs), None, None),
        ('each run has a new folder of its own with only its data file: a file, then none, then the same name with other '
         'content, in a program in several files, and no run folder is left',
         lesson(*listing, *run_parts('listing', 'Folder: run_1\nFiles: steps.txt\nLine: A\n', 'A\n', 'steps.txt'),
                *run_parts('listing', 'Folder: run_2\nFiles:\n'),
                *run_parts('listing', 'Folder: run_3\nFiles: steps.txt\nLine: B\nLine: C\n', 'B\nC\n', 'steps.txt')),
         None, None),
        ('a run without an input block gets an empty standard input, a run may have both, and the blocks of two '
         'programs may alternate',
         lesson(('example: named', 'cpp', NAMED_FILE), ('example: bytes', 'cpp', BYTES),
                ('run: named', None, ''), ('run: bytes', None, ''), ('datafile: named data.txt', 'text', 'Hello\n'),
                ('datafile: bytes data.txt', 'text', 'Hi\n'), ('output: bytes', 'text', bytes_output(b'Hi\n')),
                ('output: named', 'text', 'No standard input\ndata.txt: Hello\n'),
                *run_parts('named', 'other.txt: World\n', 'World\n', 'other.txt', stdin='other.txt\n'),
                *run_parts('named', 'Cannot open missing.txt\n', stdin='missing.txt\n')),
         None, None),
        ('an empty data file in PL and a file of one line end in EN are detected as a difference',
         lesson(('example: bytes', 'cpp', BYTES), *run_parts('bytes', bytes_output(b''), '')),
         lesson(('example: bytes', 'cpp', BYTES), *run_parts('bytes', bytes_output(b''), '\n')), 'differ between'),
        ('every bad data-file name is reported, and nothing is built',
         lesson(*[part for number, bad in enumerate(bad_names, 1)
                  for part in [(f'example: bad_{number}', 'cpp', GOOD), *run_parts(f'bad_{number}', 'Hi!\n', 'x\n', bad)]]),
         None, 'is not a valid data-file name',
         ['Steps.txt is not a valid', '../steps.txt is not a valid', 'con.txt is a reserved name on Windows',
          'steps.csv is not a valid', 'steps is not a valid', 'abcdefghijklmnopqrstu.txt is not a valid',
          "cannot read the datafile marker: <!-- datafile: bad_7 my steps.txt -->"]),
        ('misused run and datafile markers are reported, and nothing is built',
         lesson(*[part for number, (attributes, data, language) in enumerate(misused, 1)
                  for part in [(f'example: m_{number}', 'cpp', GOOD), (f'run: m_{number}', None, ''),
                               (f'datafile: m_{number} {attributes}', language, data), (f'output: m_{number}', 'text', 'Hi!\n')]],
                ('example: m_run', 'cpp', GOOD), ('run: m_run extra', None, ''), ('output: m_run', 'text', 'Hi!\n')),
         None, 'noeol on an empty data file',
         ['noeol after an empty last line', 'cannot read the datafile marker: <!-- datafile: m_3 data.txt noeol noeol -->',
          'cannot read the datafile marker: <!-- datafile: m_4 data.txt eol -->',
          'cannot read the datafile marker: <!-- datafile: m_5 noeol data.txt -->',
          'datafile marker on a ```cpp block, expected ```text', 'cannot read the run marker: <!-- run: m_run extra -->']),
        ('problems in the structure of runs are reported before building, and nothing is built',
         lesson(*structure), None, 'a data file belongs to a run',
         ['output s_2: comes before the first run marker of s_2', 'run 1 of s_3 has no output block',
          'a second output block in run 1 of s_4', 'a second input block in run 1 of s_5',
          'a second data file in run 1 of s_6', 'run s_7: a broken program is never run', 'run s_8: no example s_8 in this lesson',
          'run marker directly followed by a code block']),
        ('lines that look like markers but are not are reported',
         lesson(*good, *[(None, None, f'{line}\n```text\nHi!\n```\n\n') for line in marker_like]),
         None, 'looks like a marker but is not one', marker_like),
        ('control characters in a data file are reported, and nothing is built',
         lesson(('example: bytes', 'cpp', BYTES), *run_parts('bytes', bytes_output(b'a\x01b\n'), 'a\x01b\n'),
                *run_parts('bytes', bytes_output(b'a\x0bb\n'), 'a\x0bb\n')),
         None, 'control characters in the data', ["a control character that splits lines ('\\x0b')"]),
        ('failing runs (a wrong output, an exit code, stderr, one that never finishes, output over the limit) are reported '
         'with their run, and no run folder is left',
         lesson(('example: wrong', 'cpp', GOOD), *run_parts('wrong', 'Hello!\n', 'x\n'),
                ('example: code', 'cpp', RETURN_3), *run_parts('code', 'Hi!\n', 'x\n'),
                ('example: noise', 'cpp', PRINT_X), *run_parts('noise', '\n', 'x\n', stdin='3 1\n'),
                ('example: endless', 'cpp', ENDLESS), *run_parts('endless', 'x\n', 'x\n'),
                ('example: flood', 'cpp', PRINT_X), *run_parts('flood', 'x\n', 'x\n', stdin='70000 0\n')),
         None, 'example wrong (run 1 of 1): output',
         ['example code (run 1 of 1): exit code 3, expected 0', 'example noise (run 1 of 1): printed to stderr',
          'example endless (run 1 of 1): did not finish within', 'example flood (run 1 of 1): stdout exceeded the 65536-byte limit']),
        ('ordinary HTML comments are text, and an example without run markers keeps its runs and the checker\'s working '
         'directory next to one with them: old runs stay where they were',
         lesson((None, None, '<!-- TODO: shorten this section -->\n\n<!-- note: the run below is the main one -->\n\n'
                             '<!-- run the program twice -->\n\n<!-- datafile names are lowercase -->\n\n<!--\nA comment of '
                             'several lines\n-->\n\n'),
                ('example: old', 'cpp', WHERE), ('input: old', 'text', '4\n'),
                ('output: old', 'text', 'Value: 4, course folder here: yes\n'), ('input: old', 'text', '7\n'),
                ('output: old', 'text', 'Value: 7, course folder here: yes\n'),
                ('example: new', 'cpp', WHERE), *run_parts('new', 'Value: 0, course folder here: no\n')),
         None, None),
        # Programs with two targets (target=function_tests), checked before anything is built.
        ('bad target= markers are reported, and nothing is built',
         lesson(('example: s1_a target=tests', 'cpp', GOOD), ('output: s1_a', 'text', 'Hi!\n'),
                ('example: s1_b target=first_program', 'cpp', GOOD), ('output: s1_b', 'text', 'Hi!\n'),
                ('example: s1_c target=function_tests', 'cpp', GOOD), ('output: s1_c', 'text', 'Hi!\n'),
                ('example: s1_d exit=1 target=function_tests', 'cpp', GOOD),
                ('example: s1_e source=main.cpp target=function_tests', 'cpp', GOOD), ('output: s1_e', 'text', 'Hi!\n')),
         None, 'example s1_a: unknown target tests (an example can name only target=function_tests)',
         ['example s1_b: unknown target first_program',
          'example s1_c: target=function_tests is only for a program in several files with two targets',
          'cannot read the example marker (expected target=function_tests [exit=N], in this order): '
          '<!-- example: s1_d exit=1 target=function_tests -->',
          "example s1_e: target= can't be combined with source="]),
        ('target= and the CMakeLists.txt with two targets must agree, and nothing is built',
         lesson(*parking('s2_a', cmake=template.replace('main.cpp)', 'main.cpp rules.cpp)')), *parking('s2_b', marker='')),
         None, 'program s2_a: target=function_tests needs the CMakeLists.txt with two targets',
         ['program s2_b: a CMakeLists.txt with two targets needs target=function_tests on the example']),
        ('the CMakeLists.txt with two targets is checked line for line (C++20 for both, no other command, no third '
         'target), and nothing is built',
         lesson(*parking('s3_a', cmake=cmake_tests.replace('(function_tests PRIVATE cxx_std_20)', '(function_tests PRIVATE cxx_std_17)')),
                *parking('s3_b', cmake=cmake_tests.replace('target_compile_features(function_tests PRIVATE cxx_std_20)\n', '')),
                *parking('s3_c', cmake=cmake_tests + 'enable_testing()\n'),
                *parking('s3_d', cmake=cmake_tests + 'add_executable(more_tests function_tests.cpp rules.cpp)\n'),
                *parking('s3_e', cmake=cmake_tests.replace('OFF)\n\nadd_executable(function_tests', 'OFF)\nadd_executable(function_tests'))),
         None, f'program s3_a: {two_target_form}', [f'program s3_{letter}: {two_target_form}' for letter in 'bcde']),
        ('the source lists of the two targets are checked, and nothing is built',
         lesson(*parking('s4_a', cmake=two_lists(tests='function_tests.cpp rules.cpp main.cpp')),
                *parking('s4_b', cmake=two_lists(program='main.cpp rules.cpp function_tests.cpp')),
                *parking('s4_c', cmake=two_lists(tests='rules.cpp')),
                *parking('s4_d', cmake=two_lists(tests='function_tests.cpp')),
                *parking('s4_e', cpp=None, cmake=two_lists(program='main.cpp', tests='function_tests.cpp')),
                *parking('s4_f', cmake=two_lists(program='rules.cpp'))),
         None, 'program s4_a: function_tests must not list main.cpp',
         ['program s4_b: first_program must not list function_tests.cpp',
          'program s4_c: function_tests must list function_tests.cpp',
          'program s4_d: rules.cpp is listed by first_program but not by function_tests',
          'program s4_e: first_program and function_tests share no .cpp file',
          'program s4_f: add_executable(first_program ...) must list main.cpp']),
        ('the rules of add_executable apply to both lists, and nothing is built',
         lesson(*parking('s5_a', cmake=two_lists(tests='function_tests.cpp rules.cpp rules.hpp')),
                *parking('s5_b', cmake=two_lists(tests='function_tests.cpp rules.cpp rules.cpp')),
                *parking('s5_c', cmake=two_lists(tests='function_tests.cpp rules.cpp Rules.cpp')),
                *parking('s5_d', cmake=two_lists(tests='function_tests.cpp rules.cpp rule.cpp')),
                *parking('s5_e', extra=[('helper.cpp', 'int helper() {\n    return 1;\n}\n')]),
                *parking('s5_f', cmake=two_lists(program='main.cpp rules.cpp main.cpp'))),
         None, 'program s5_a: add_executable(function_tests ...) lists the header rules.hpp',
         ['program s5_b: add_executable(function_tests ...) lists rules.cpp twice',
          'program s5_c: add_executable(function_tests ...) lists Rules.cpp, which differs in case from rules.cpp',
          'program s5_d: add_executable(function_tests ...) lists rule.cpp, which is not a .cpp file of the program',
          'program s5_e: helper.cpp is in neither add_executable',
          'program s5_f: add_executable(first_program ...) lists main.cpp twice']),
        # s6_a would pass if it were built: its tests call their own correct copy, not the faulty rules.cpp.
        ('main.cpp and function_tests.cpp without a header of the program in common are reported (also a commented-out '
         'or miswritten #include), and nothing is built',
         lesson(*parking('s6_a', cpp=RULES_BUG, tests=static_copy),
                *parking('s6_b', main=PARKING_MAIN.replace('#include "rules.hpp"\n', 'int parking_fee(int hours);\n')),
                *parking('s6_c', tests=PARKING_TESTS.replace('"rules.hpp"', '"check.hpp"'), extra=[('check.hpp', CHECK_HPP)]),
                *parking('s6_d', tests=PARKING_TESTS.replace('#include "rules.hpp"', '// #include "rules.hpp"')),
                *parking('s6_e', tests=PARKING_TESTS.replace('"rules.hpp"', '"Rules.hpp"'))),
         None, 'program s6_a: function_tests.cpp includes none of the headers of the program that main.cpp includes '
               '(rules.hpp), so the two targets share no interface',
         ['program s6_b: main.cpp includes no header of the program', 'program s6_c: function_tests.cpp includes none',
          'program s6_d: function_tests.cpp includes none', 'program s6_e: function_tests.cpp includes none',
          'program s6_e: function_tests.cpp:4: #include "Rules.hpp" differs in case from rules.hpp']),
        ('an example with target=function_tests has no input blocks or run markers and one output block, and nothing is '
         'built',
         lesson(*parking('s7_a', output=None), ('input: s7_a', 'text', '2\n'), ('output: s7_a', 'text', PARKING_PASS),
                *parking('s7_b', output=None), *run_parts('s7_b', PARKING_PASS),
                *parking('s7_c'), ('output: s7_c', 'text', PARKING_PASS)),
         None, 'example s7_a: an example with target=function_tests runs once, with an empty standard input',
         ['example s7_b: an example with target=function_tests runs once',
          'example s7_c: an example with target=function_tests has exactly one output block, not 2']),
        ("a broken program can't have two targets or target=, and nothing is built",
         lesson(*parking('s8_a', owner='broken', marker=' stage=link error=main', output=None),
                ('broken: s8_b target=function_tests stage=link error=main', 'cpp', MIAN)),
         None, 'program s8_a: a broken program has one target',
         ['cannot read the broken marker (target= is only for an example: a broken program has one target): '
          '<!-- broken: s8_b']),
        # Programs with two targets, really built: both targets, and only function_tests is run.
        ('a program with two targets builds both targets from the shared rules.cpp, runs function_tests and passes',
         lesson(*parking()), None, None),
        ('a bug in the shared rules.cpp is detected by function_tests, which prints its FAIL lines and exits with 1 (exit=1)',
         lesson(*parking(marker=' target=function_tests exit=1', cpp=RULES_BUG, output=PARKING_FAIL)), None, None),
        ('a one-file example and a program in several files are built as before next to a program with two targets',
         lesson(*good, *twice, *parking()), None, None),
        ('function_tests runs the shared rules.cpp: a bug there fails an example that expects every check to pass',
         lesson(*parking(cpp=RULES_BUG)), None, 'example parking (target function_tests): exit code 1, expected 0',
         ['example parking (target function_tests): output']),
        ('a compile error in main.cpp fails a program with two targets, though only function_tests is run',
         lesson(*parking(main=PARKING_MAIN.replace('<< fee << "\\n";', '<< fee << "\\n"'))), None,
         'example parking (target function_tests): build failed: main.cpp (target first_program) failed to compile'),
        ('a link error of first_program fails a program with two targets, though only function_tests is run',
         lesson(*parking(main=PARKING_MAIN.replace('int main() {', 'int missing_fee();\n\nint main() {')
                         .replace('{parking_fee(hours)}', '{parking_fee(hours) + missing_fee()}'))), None,
         'example parking (target function_tests): build failed: first_program failed to link'),
        ('a compile error in function_tests.cpp is reported with its target',
         lesson(*parking(tests=PARKING_TESTS.replace('int checks{0};', 'int checks{0}'))), None,
         'example parking (target function_tests): build failed: function_tests.cpp (target function_tests) failed to compile'),
        # The copy would pass every check while rules.cpp is faulty; it clashes with rules.cpp in function_tests instead.
        ('a copy of parking_fee in function_tests.cpp fails to link as function_tests, though rules.cpp has a bug it would hide',
         lesson(*parking(cpp=RULES_BUG, tests=with_copy)), None,
         'example parking (target function_tests): build failed: function_tests failed to link'),
        # The tests added to the program's own target: one target with two main functions, checked on the old path.
        ('function_tests.cpp in the list of first_program fails to link with two main functions (stage=link, one target)',
         lesson(*parking(owner='broken', marker=f' stage=link error={DUPLICATE_MAIN}', output=None,
                         cmake=template.replace('main.cpp)', 'main.cpp rules.cpp function_tests.cpp)'))), None, None),
    ]
    project = PROJECT.resolve()
    home = os.getcwd()
    failures = 0
    for title, pl_text, en_text, expected_failure, *also in cases:
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
                # Some cases expect several problems at once: each of them must be reported.
                verdict = verdict and all(any(message in e for e in errors) for message in (also[0] if also else []))
                if 'exact bytes' in title:
                    # The bytes the checker writes, read from the lesson as the checker reads it, before any program runs.
                    found, _ = blocks(pathlib.Path('course/module_99_self_test/lesson.md'))
                    folder_runs = check_lesson(pathlib.Path('lesson.md'), found)[3]
                    written = [data_file[1] if data_file else None for _, data_file, _ in folder_runs.get('bytes', [])]
                    verdict = verdict and written == [content for content, _ in bytes_cases]
                if 'no run folder is left' in title:
                    verdict = (verdict and pathlib.Path('build/lesson-examples/lesson').is_dir()
                               and not any(pathlib.Path('build').rglob('run_*')))
                if 'old runs stay where they were' in title:
                    old = pathlib.Path('build/lesson-examples/lesson/old')
                    verdict = verdict and old.is_dir() and not any(old.glob('run_*'))
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
                if 'builds both targets from the shared' in title:
                    # Both programs exist, and each target compiled rules.cpp into an object file of its own.
                    work = pathlib.Path('build/lesson-examples/lesson/parking/build')
                    verdict = (verdict and executable(work).exists() and executable(work, TEST_TARGET).exists()
                               and all(any((work / 'CMakeFiles' / f'{target}.dir' / f'rules.cpp{suffix}').exists()
                                           for suffix in ('.o', '.obj')) for target in (executable(work).stem, TEST_TARGET)))
                if 'next to a program with two targets' in title:
                    # The program with two targets got its own five files; the others have no second target.
                    work = pathlib.Path('build/lesson-examples/lesson')
                    verdict = (verdict and sorted(p.name for p in (work / 'parking' / 'src').iterdir())
                               == ['CMakeLists.txt', 'function_tests.cpp', 'main.cpp', 'rules.cpp', 'rules.hpp']
                               and executable(work / 'twice' / 'build').exists()
                               and not executable(work / 'twice' / 'build', TEST_TARGET).exists()
                               and not executable(work / 'hi' / 'build', TEST_TARGET).exists())
            finally:
                os.chdir(home)
        print(f'##### {"ok  " if verdict else "FAIL"} self-test: {title}')
        failures += not verdict
    limit_failures, limit_cases = self_test_limits(args)
    failures += limit_failures
    shard_failures, shard_cases = self_test_shards(args)
    failures += shard_failures
    folder_failures, folder_cases = self_test_folders(args)
    failures += folder_failures
    total = len(cases) + limit_cases + shard_cases + folder_cases
    print(f'\n{"PASSED" if not failures else "FAILED"}: self-test, {total} cases, {failures} failed')
    return failures


def self_test_folders(args):
    """Runs run_in_folder() directly, for what a lesson can't arrange: a folder left from before, a data-file name that
    would leave the folder, and a program that can't be started. Returns (failures, number of checks)."""
    project = PROJECT.resolve()
    home = os.getcwd()
    title = ('the run folder: one left from before is emptied first, a data file is never written outside it, '
             'and it is removed even when the program cannot be started')
    print(f'\n##### self-test: {title}')
    with tempfile.TemporaryDirectory() as root:
        os.chdir(root)
        try:
            PROJECT.parent.mkdir(parents=True)
            shutil.copy(project, PROJECT)
            cmake = PROJECT.read_text(encoding='utf-8').replace('main.cpp)', 'main.cpp listing.cpp)')
            built = build('self_test', 'folders', LISTING_MAIN, args,
                          project=({'listing.hpp': LISTING_HPP, 'listing.cpp': LISTING_CPP}, cmake))
            if not built or built[1].returncode != 0:
                print(f'##### FAIL self-test: {title}: the listing program did not build')
                return 1, 1
            exe = executable(built[0]).resolve()
            work = built[0].parent
            stale = work / 'run_1'
            stale.mkdir()
            (stale / 'old.txt').write_text('old\n', encoding='ascii')
            result, removed = run_in_folder(exe, None, ('steps.txt', b'A\n'), stale, args.timeout)
            emptied = (not isinstance(result, str) and result[1].replace(b'\r\n', b'\n')
                       == b'Folder: run_1\nFiles: steps.txt\nLine: A\n' and removed and not stale.exists())
            outside = work / 'run_2'
            result, removed = run_in_folder(exe, None, ('../escaped.txt', b'x\n'), outside, args.timeout)
            kept_inside = (isinstance(result, str) and 'would be written outside' in result and removed
                           and not (work / 'escaped.txt').exists() and not outside.exists())
            missing = work / 'run_3'
            result, removed = run_in_folder(work / 'no-such-program', None, ('steps.txt', b'A\n'), missing, args.timeout)
            not_started = isinstance(result, str) and result.startswith('could not be started') and removed and not missing.exists()
        finally:
            os.chdir(home)
    print(f'##### self-test: emptied first: {emptied}, nothing written outside: {kept_inside}, '
          f'removed after a failed start: {not_started}')
    verdict = emptied and kept_inside and not_started
    print(f'##### {"ok  " if verdict else "FAIL"} self-test: {title}')
    errors.clear()
    return (0 if verdict else 1), 1


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


def self_test_shards(args):
    """Checks --shard on small fixture courses of several lessons: which lessons each part builds, and that every
    lesson is still checked before building. Most lessons have only a fragment, so nothing is built; two cases build
    one program each. Returns (failures, number of cases)."""
    project = PROJECT.resolve()
    home = os.getcwd()
    fragment = lesson(('fragment', 'cpp', 'int twice(int value);\n'))
    template = PROJECT.read_text(encoding='utf-8')
    twice = lesson(('example: twice', 'cpp', TWICE_MAIN), ('file: twice tools.hpp', 'cpp', TOOLS_HPP),
                   ('file: twice tools.cpp', 'cpp', TOOLS_CPP),
                   ('cmake: twice', 'cmake', template.replace('main.cpp)', 'main.cpp tools.cpp)')),
                   ('input: twice', 'text', '4\n'), ('output: twice', 'text', 'Twice: 8\n'),
                   ('input: twice', 'text', '-3\n'), ('output: twice', 'text', 'Twice: -6\n'))

    def run_course(lessons, shard):
        """Checks a fixture course of LESSONS ({file stem: PL text, or (PL text, EN text)}) with --shard SHARD (None:
        without). Returns (problems, output, the lessons built and run here, the lessons with a build folder)."""
        case_args = argparse.Namespace(**vars(args))
        case_args.shard = shard
        with tempfile.TemporaryDirectory() as root:
            os.chdir(root)
            try:
                PROJECT.parent.mkdir(parents=True)
                shutil.copy(project, PROJECT)
                folder = pathlib.Path('course/module_99_self_test')
                folder.mkdir(parents=True)
                # Written in reverse order: the parts must follow the sorted names, not the order of creation.
                for stem in sorted(lessons, reverse=True):
                    pl_text, en_text = lessons[stem] if isinstance(lessons[stem], tuple) else (lessons[stem],) * 2
                    (folder / f'{stem}.md').write_text(pl_text, encoding='utf-8')
                    (folder / f'{stem}.en.md').write_text(en_text, encoding='utf-8')
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    check_course(case_args)
                built_folders = sorted(p.name for p in pathlib.Path('build/lesson-examples').glob('*'))
            finally:
                os.chdir(home)
        text = output.getvalue()
        print(text, end='')
        # The lessons whose header line is followed, before the next lesson, by "built and run here" (any separator).
        here = re.findall(r'^=== course[/\\]module_99_self_test[/\\](\w+)\.md .*\n(?:(?!===).*\n)*?     part \d+ of \d+: built and run here$',
                          text, re.M)
        return list(errors), text, here, built_folders

    def bad_values_refused():
        bad = ['0/2', '3/2', '1/0', '2', '1/2/3', 'a/b', '01/2', ' 1/2', '-1/2', '1/-2', '']
        refused = []
        for value in bad:
            try:
                shard_arg(value)
            except argparse.ArgumentTypeError:
                refused.append(value)
        good = {'1/1': (1, 1), '1/2': (1, 2), '2/2': (2, 2), '3/3': (3, 3), '10/12': (10, 12)}
        return refused == bad and all(shard_arg(value) == parsed for value, parsed in good.items())

    def parts_cover_every_lesson():
        for count in range(1, 6):
            stems = [f'lesson_{chr(ord("a") + i)}' for i in range(count)]
            for parts in range(1, 4):
                seen = []
                for part in range(1, parts + 1):
                    problems, _, here, _ = run_course({stem: fragment for stem in stems}, (part, parts))
                    expected = [stem for i, stem in enumerate(stems) if i % parts + 1 == part]
                    # A part without lessons must fail; any other part must pass and build exactly its lessons.
                    if here != expected or bool(problems) != (not expected):
                        return False
                    seen += here
                if sorted(seen) != stems:
                    return False
        return True

    def odd_count_split():
        lessons = {'lesson_a': fragment, 'lesson_b': fragment, 'lesson_c': fragment}
        first, second = run_course(lessons, (1, 2)), run_course(lessons, (2, 2))
        return (first[2] == ['lesson_a', 'lesson_c'] and second[2] == ['lesson_b'] and not first[0] and not second[0]
                and '3 lesson(s) checked before building, 2 of them built and run in this part' in first[1]
                and '3 lesson(s) checked before building, 1 of them built and run in this part' in second[1])

    def without_shard_as_before():
        problems, text, _, _ = run_course({'lesson_a': fragment, 'lesson_b': fragment, 'lesson_c': fragment}, None)
        return not problems and text.rstrip('\n').endswith('\nPASSED: 3 lesson(s), 0 problem(s)') and ' part ' not in text

    def static_problem_of_other_part():
        lessons = {'lesson_a': fragment, 'lesson_b': fragment + '```cpp\nint main() {}\n```\n'}
        problems, _, here, _ = run_course(lessons, (1, 2))
        return here == ['lesson_a'] and any('lesson_b.md' in e and 'without a marker' in e for e in problems)

    def program_in_several_files_built_whole():
        lessons = {'lesson_a': fragment, 'lesson_b': twice}
        first, second = run_course(lessons, (1, 2)), run_course(lessons, (2, 2))
        return (not first[0] and first[3] == [] and not second[0] and second[3] == ['lesson_b']
                and '(1 example(s), 0 broken program(s), 2 run(s))' in second[1]
                and 'part 2 of 2: 1 lesson(s), 1 example(s), 0 broken program(s), 2 run(s)' in first[1])

    def part_without_lessons():
        problems, _, _, _ = run_course({'lesson_a': fragment, 'lesson_b': fragment, 'lesson_c': fragment}, (4, 4))
        return any('part 4 of 4 has no lessons' in e for e in problems)

    def runs_in_folders_split():
        runs = lesson(('example: bytes', 'cpp', BYTES), *run_parts('bytes', bytes_output(b'A\n'), 'A\n'),
                      *run_parts('bytes', bytes_output(None)), *run_parts('bytes', bytes_output(b''), ''))
        lessons = {'lesson_a': fragment, 'lesson_b': runs}
        whole, first, second = run_course(lessons, None), run_course(lessons, (1, 2)), run_course(lessons, (2, 2))
        verdicts = [[line for line in result[1].splitlines() if line.startswith(('ok   lesson_b', 'FAIL'))]
                    for result in (whole, second)]
        return (not whole[0] and not first[0] and not second[0] and first[3] == [] and second[3] == ['lesson_b']
                and '(1 example(s), 0 broken program(s), 3 run(s))' in second[1] and len(verdicts[0]) == 3
                and verdicts[0] == verdicts[1])

    def failure_stays_in_its_part():
        wrong = lesson(('example: hi', 'cpp', GOOD), ('output: hi', 'text', 'Hello!\n'))
        lessons = {'lesson_a': fragment, 'lesson_b': wrong}
        first, second = run_course(lessons, (1, 2)), run_course(lessons, (2, 2))
        return (not first[0] and '(0 example(s), 0 broken program(s), 0 run(s))' in first[1]
                and any('example hi: output' in e for e in second[0]))

    checks = [
        ('invalid --shard values are refused, and valid ones are read', bad_values_refused),
        ('the parts are disjoint, cover every lesson and follow the sorted names (1 to 5 lessons, 1 to 3 parts)',
         parts_cover_every_lesson),
        ('three lessons in two parts: the first and the third in part 1, the second in part 2', odd_count_split),
        ('without --shard every lesson is built, and the summary is as before', without_shard_as_before),
        ('a problem found before building is reported by a part that does not build that lesson', static_problem_of_other_part),
        ('a program in several files is built whole, by its own part only', program_in_several_files_built_whole),
        ('a part without lessons fails', part_without_lessons),
        ('a failing program fails its own part, and the other part neither builds nor passes it', failure_stays_in_its_part),
        ('an example with run markers is run whole by its own part, with the same verdicts as without --shard',
         runs_in_folders_split),
    ]
    failures = 0
    for title, check in checks:
        print(f'\n##### self-test: {title}')
        verdict = check()
        print(f'##### {"ok  " if verdict else "FAIL"} self-test: {title}')
        failures += not verdict
    errors.clear()
    return failures, len(checks)


def shard_arg(text):
    """K/N for --shard: part K of N, with 1 <= K <= N, written without leading zeros or spaces."""
    match = re.fullmatch(r'([1-9][0-9]*)/([1-9][0-9]*)', text)
    if not match or int(match[1]) > int(match[2]):
        raise argparse.ArgumentTypeError(f'expected K/N with 1 <= K <= N, for example 1/2, not {text!r}')
    return int(match[1]), int(match[2])


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--cxx', required=True, help='full path to the official clang++')
    parser.add_argument('--cmake', default='cmake')
    parser.add_argument('--make-program', help='Ninja to use, if not the one on PATH')
    parser.add_argument('--timeout', type=float, default=10, help='seconds each run of an example may take')
    parser.add_argument('--self-test', action='store_true', help='check the checker on small fixture lessons')
    parser.add_argument('--shard', type=shard_arg, metavar='K/N',
                        help='check every lesson before building, but build and run only part K of N of the lessons')
    args = parser.parse_args()
    if args.self_test and args.shard:
        parser.error('--shard checks a part of the course; --self-test always runs all of its cases')
    if args.self_test:
        return 1 if self_test(args) else 0
    return 1 if check_course(args) else 0


if __name__ == '__main__':
    sys.exit(main())
