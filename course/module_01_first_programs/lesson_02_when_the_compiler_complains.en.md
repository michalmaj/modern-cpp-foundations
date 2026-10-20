# probe

<!-- example: start -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

<!-- output: start -->
```text
Good morning!
Time to write some C++.
```

<!-- broken: no_semicolon at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n"
    std::cout << "Time to write some C++.\n";
}
```

<!-- broken: no_include at=2 error=. -->
```cpp
int main() {
    std::cout << "Good morning!\n";
    std::cout << "Time to write some C++.\n";
}
```

<!-- broken: no_std at=5 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n";
    cout << "Time to write some C++.\n";
}
```

<!-- broken: shopping_list at=2 error=. -->
```cpp
int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n"
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

<!-- broken: shopping_list_include at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "SHOPPING LIST\n";
    std::cout << "- bread\n"
    cout << "- milk\n";
    std::cout << "- apples";
    std::cout << "TOTAL: 3 items\n";
}
```

<!-- broken: last_semicolon at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Good morning!\n"
}
```
