# Toolchain checks

`cpp20_smoke/` is a tiny C++20 project that checks whether the official course toolchain can compile, link, run and test a program. The toolchain is upstream LLVM/Clang 22 or newer, used through `clang++`, together with CMake, Ninja and CTest.

This is a check for course maintainers. It is **not** an installation guide for learners.

## Three levels of verification

These are different things. A green run of this check proves only the first.

1. **The toolchain works on a CI runner.** `.github/workflows/toolchains.yml` runs this project on GitHub-hosted Windows, Ubuntu 24.04 and macOS runners. Those runners come with many tools preinstalled, for example full Visual Studio on Windows.
2. **A clean installation works on a learner's computer.** This needs a fresh machine or virtual machine and the exact steps a learner will follow. It is not covered here.
3. **CLion is set up correctly.** This includes toolchain selection, Debug/Release profiles and the debugger. It is a separate, manual check.

## What the project checks

- **Configuration fails** unless the compiler is upstream Clang 22 or newer, with the `clang++` (GNU-style) driver, and on Windows targets the MSVC ABI. AppleClang, GCC, MSVC `cl`, `clang-cl` and MinGW are rejected, so a green run can't come from a silent fallback.
- **It builds** a static library, a program and a test program. This uses the compiler, the archiver and the linker. It uses C++20: concepts, ranges, `std::span`, `std::format`, `operator<=>` and designated initializers.
- **CTest runs two real tests:**
  - `smoke_test` checks the library's results and fails with a message for each wrong one;
  - `program_output` checks the program's output, including whether assertions are compiled in. That proves whether Debug or Release was actually built.
- **The program prints** the compiler version, the C++ standard library it was built against, and `__cplusplus`.

The same workflow also builds the learner project of lesson 0.5 (`course/module_00_tooling/lesson_05_first_program`) in Debug, runs it, and checks the behaviour the lesson describes: after editing `main.cpp` without building, the existing executable still prints the old message; after building it prints the new one; a second build without changes does no work. It works on a copy in `build/`, so the tracked lesson files are never changed.

`lesson_06.ps1` (Windows PowerShell 5.1 and PowerShell 7) and `lesson_06.sh` (bash on Ubuntu, zsh on macOS) run the **exact terminal commands of lesson 0.6** on a temporary copy of that project: CMake configure, build and run; a direct `clang++` compile; and the edit-and-rebuild experiment with three executables. They can be run locally from the repository root, for example `zsh tests/toolchains/lesson_06.sh` or `powershell -NoProfile -ExecutionPolicy Bypass -File tests\toolchains\lesson_06.ps1`.

## Running it locally

From the repository root, with the official toolchain installed. Use the full path to upstream `clang++`, so that CMake can't pick another compiler:

| System | `CXX_COMPILER` used in CI |
|---|---|
| Windows (PowerShell) | `C:\Program Files\LLVM\bin\clang++.exe` (LLVM from Chocolatey) |
| Ubuntu 24.04 | `/usr/bin/clang++-22` (apt.llvm.org) |
| macOS | `$(brew --prefix llvm@22)/bin/clang++` (Homebrew), **not** `/usr/bin/clang++`, which is AppleClang |

Then, for each configuration (`Debug` and `Release`):

```sh
cmake -S tests/toolchains/cpp20_smoke -B build/toolchain-smoke/Debug -G Ninja -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=<CXX_COMPILER>
cmake --build build/toolchain-smoke/Debug
ctest --test-dir build/toolchain-smoke/Debug --output-on-failure
```

`build/` is ignored by Git. The workflow file shows exactly how CI installs the tools and identifies the environment. That is a CI recipe, not a verified procedure for a clean computer.
