# Draft (replaced by the real lesson in the next commit)

<!-- example: original source=../module_00_tooling/lesson_05_first_program/main.cpp -->
```cpp
#include <iostream>

int main() {
    std::cout << "Hello! My first C++20 program works.\n";
}
```

<!-- output: original -->
```text
Hello! My first C++20 program works.
```

<!-- broken: mian stage=link error=undefined reference to .main'|undefined symbol: main\b|"_main", referenced from -->
```cpp
#include <iostream>

int mian() {
    std::cout << "Hello! My first C++20 program works.\n";
    return 0;
}
```

<!-- example: mission -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK\n";
    std::cout << "Run: OK\n";
    return 0;
}
```

<!-- output: mission -->
```text
Build: OK
Run: OK
```

<!-- broken: mission_quote at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK\n;
    std::cout << "Run: OK\n";
    return 0;
}
```

<!-- broken: mission_main stage=link error=undefined reference to .main'|undefined symbol: main\b|"_main", referenced from -->
```cpp
#include <iostream>

int Main() {
    std::cout << "Build: OK\n";
    std::cout << "Run: OK\n";
    return 0;
}
```

<!-- example: mission_newline -->
```cpp
#include <iostream>

int main() {
    std::cout << "Build: OK";
    std::cout << "Run: OK\n";
    return 0;
}
```

<!-- output: mission_newline -->
```text
Build: OKRun: OK
```

