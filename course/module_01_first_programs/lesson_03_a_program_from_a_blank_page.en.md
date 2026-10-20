# probe

<!-- broken: quote_udl at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Say "cheese"!\n";
}
```

<!-- broken: quote_space at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Say "cheese" please\n";
}
```

<!-- broken: quote_end at=4 error=. -->
```cpp
#include <iostream>

int main() {
    std::cout << "Folder: C:\";
}
```

<!-- example: path -->
```cpp
#include <iostream>

int main() {
    std::cout << "C:\new\notes.txt\n";
}
```

<!-- output: path -->
```text
C:
ew
otes.txt
```

<!-- example: ret3 exit=3 -->
```cpp
#include <iostream>

int main() {
    std::cout << "Done.\n";
    return 3;
}
```

<!-- output: ret3 -->
```text
Done.
```

<!-- example: comment -->
```cpp
#include <iostream>

int main() {
    // A comment.
    std::cout << "Comments start with // in C++\n";
    // std::cout << "Hidden\n";
}
```

<!-- output: comment -->
```text
Comments start with // in C++
```
