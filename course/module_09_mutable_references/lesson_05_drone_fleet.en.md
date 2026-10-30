# Lesson 9.5: A delivery drone fleet (the Module 9 test)

[Polski](lesson_05_drone_fleet.md) · **English** · [Course overview](../../README.en.md)

> **Module 9, lesson 5: the test** · about 105–125 minutes, in two sessions
> **You need:** your `cpp-workspace` folder and the original `lesson_05_first_program` project.
> **Pilot version.** The reference solutions in this lesson are checked automatically on Windows, Ubuntu and macOS. Nothing grades your own work automatically: you check it yourself, against the criteria. Your program asks for no data: all the values are written in the code. Only the check program in Part B reads data from the input.

## How this test works

This lesson introduces nothing new. You check whether you can design, on your own, a program in which **several functions change existing records on purpose**: each operation keeps the agreed conditions of correctness, and a refusal never leaves partly changed data. It isn't about counting summaries or choosing the best record, but about a controlled change of state.

The lesson has two parts:

- **Part A: the test.** Task 1: requirements, data, the report and the criteria. No hints and no solution code. Everything you need is from Modules 1–9.
- **Part B: checking and discussion.** Hints, the full list of check cases, task 2 (diagnostics) and task 3 (explanations), which you do after task 1, and then the reference solution, fixes, answers and the self-assessment. Go there only after doing Part A, or when you consciously decide to stop trying on your own.

Looking at Part B, at earlier lessons or at your notes isn't a failure. What matters is that you **honestly note what you did on your own and what with help**. A suggested split into two sessions:

- **first:** analysing the rules, designing the type and the three functions, writing them, and the report for the data in the requirements;
- **second:** the boundary cases, the empty-vector variant, tasks 2 and 3, comparing with the solution, and the self-assessment.

**You may use:** CLion or the terminal, CMake and Ninja, as before; a `CMakeLists.txt` copied from the original `lesson_05_first_program`; case and trace tables, and temporary test printouts. You won't need the debugger.

---

# Part A: the test

## Task 1: A delivery drone fleet

The program manages a simplified fleet of delivery drones. It isn't a simulator of real devices: the battery and the cost of a flight are points by convention, and the program doesn't model time, distance, routes or weather. All the operations change the drones stored in one collection.

**Preparation:** in `cpp-workspace`, create a folder `drone_fleet`, copy `CMakeLists.txt` into it from the original `lesson_05_first_program`, create an **empty** `main.cpp`, and write the whole program yourself.

### The fleet's data

| Drone | Battery | Flights | Grounded |
|---|---:|---:|---|
| A-01 | 65 | 2 | no |
| B-02 | 35 | 0 | no |
| C-03 | 90 | 4 | yes |
| D-04 | 100 | 1 | no |

### Rules

- The identifiers are non-empty, unique, and made of plain ASCII text. The battery has from 0 to 100 points, and the number of flights is non-negative. All the numbers are small. The data meet these assumptions, so the program doesn't check them.
- **A flight** is allowed only when **all three** conditions are met:
  1. the cost of the flight is positive;
  2. the drone isn't grounded;
  3. the battery **after** the flight would be at least 20 points. That's the reserve: a battery of exactly 20 after the flight is allowed, and 19 isn't.
- A cost of 0 and a negative cost are invalid requests.
- **An accepted flight:** the battery falls by the cost, the number of flights grows by 1, and the other fields don't change. **A refused flight:** no field changes. There's no partial flight.
- **A flight by identifier** concerns only the drone with that identifier. An unknown identifier is a refusal, after which nothing changes. The result "the flight didn't happen" doesn't tell whether the drone wasn't found or the flight was refused, as in lesson 9.4.
- **Charging the fleet:** every drone with a battery below 100 gets a battery of 100. Charging doesn't change the number of flights or the identifiers. A drone that already has 100 isn't counted as charged.
- **A grounded drone can be charged, but charging doesn't lift the grounding.** After charging, it still can't fly.
- The number of drones in the vector and their order never change.

### The type and the functions

- The program defines **one type of your own** for a drone, with four fields: an identifier (`std::string`), the battery (`int`), the number of flights (`int`) and whether it's grounded (`bool`). No additional fields. You choose the names of the type and the fields.
- **The function for one drone's flight** gets an existing record through a modifiable reference, and the cost (`int`) by value. It checks all the conditions of the flight before changing anything. It returns `bool`: `true` when it performed the flight, `false` when it refused it.
- **The function for a flight by identifier** gets the existing vector through a modifiable reference, the identifier through `const std::string&` and the cost by value. It finds the drone with that identifier, performs its flight **with the function for one drone's flight**, and returns that function's result. When the identifier isn't there, it returns `false`.
- **The function for charging the fleet** gets the existing vector through a modifiable reference, charges the drones according to the rules, and returns the number of drones whose battery really changed. That's a number of elements, as in lesson 8.4.
- None of these functions prints anything or reads anything from the input. You write the names of the functions and parameters, and their headers, yourself. A fourth function isn't needed. You may add a function that only prints the fleet, as long as it gets it through `const&`.
- **`main`** stores the drones in one vector, initialised in the code in the order of the table. No separate variables for the drones, and no `push_back`. `main` performs the operations from the list below, each **exactly once, on the same vector**. It stores the result of each flight and prints `accepted` or `refused` based on it, without calling the operation again. It doesn't repeat the rules of flying or charging. The program uses no variables declared outside functions.

### Operations

Perform exactly these operations, in this order:

1. a flight of `B-02`, cost 15;
2. a flight of `B-02`, cost 1;
3. a flight of `C-03`, cost 10;
4. a flight of `BAD-99`, cost 10;
5. charging the whole fleet;
6. a flight of `B-02`, cost 80;
7. a flight of `B-02`, cost 1.

### The report

For the data in the requirements, the standard output must be:

<!-- output: drone_fleet -->
```text
Drones: 4
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (15): accepted
Fly B-02 (1): refused
Fly C-03 (10): refused
Fly BAD-99 (10): refused
Charged: 3
Fly B-02 (80): accepted
Fly B-02 (1): refused
After:
A-01: battery 100, flights 2, grounded no
B-02: battery 20, flights 2, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
```

- `Drones` comes from `size()`, and `Before` and `After` show all the drones in the vector's order.
- In the flight lines, the cost stands in brackets.
- `Charged` is the result of the function for charging the fleet.
- The program prints no other messages and no blank lines.

**The empty-vector variant:** the same functions, an empty vector, one flight of `A-01` with cost 10, and charging the fleet. `main` then prints only:

<!-- output: drone_fleet_empty -->
```text
Drones: 0
Fly A-01 (10): refused
Charged: 0
```

### How to work

1. **Design the type and the three functions before you start writing `main`.** For each function, write down in one sentence its job, its parameters and its result type.
2. **Prepare a table of cases:** the data from the requirements; an empty vector; one drone; a cost of 0 and a negative cost; a flight that leaves exactly 20, and one that would leave 19; a cost larger than the battery; a grounded drone with a full and with a partly charged battery; an unknown identifier; a drone at the first, the middle and the last position; two flights of the same drone with a charge between them; charging when all the batteries are full, and when none is, twice in a row. For each operation, write down the result and the state of the drone it concerns. **Check the state after a refusal right after it**, not only at the end: a later charge can hide a battery changed by a refused flight.
3. **Run the program** for the data from the requirements and for the empty-vector variant. Analyse the other cases on paper. All the cases of the full check list are checked automatically.

When the result matches, you can save the project in Git, as in lesson 1.5. Before committing, check `git status`: only `main.cpp` and `CMakeLists.txt` go into the history.

## Success criteria

You pass the test when you meet **all** the criteria. You may use Part B while doing so, as long as you note it honestly in the self-assessment.

- `drone_fleet/main.cpp` was written from an empty file, in valid C++20. The program builds without errors.
- There's one drone type with four fields of the required types, and the drones stand in one vector, in the order of the table.
- The function for one drone's flight gets the record through `&` and the cost by value. It checks all three conditions before changing anything. On a refusal it changes no field, and on success it changes exactly the battery and the number of flights.
- The function for a flight by identifier gets the vector through `&` and the identifier through `const std::string&`, changes the real element, uses the function for one drone's flight, and returns `false` only after checking all the drones.
- The function for charging the fleet changes only the battery, doesn't lift the grounding, and counts only the drones whose battery really changed.
- None of the three functions prints or reads anything. The rules of flying and charging stand in one place in the program.
- The standard output for the data from the requirements and for the empty-vector variant matches the requirements. The other cases match your analysis on paper and the full list of check cases.
- The bug from diagnostic A was fixed and checked, and the fragment from diagnostic B was analysed without running it (task 2 in Part B).
- You can explain every line of your program and answer the questions of task 3.

The names of the type, the fields, the functions and the variables, and the layout of `main`, may differ from the reference solution, as long as they're readable and meet the requirements. A correct result is a necessary condition, but **not proof of understanding**. That's why tasks 2 and 3 are part of the test.

---

# Part B: checking and discussion

Come here **only after doing Part A**, or when you consciously decide to stop trying on your own. This part contains code very close to the solution of task 1.

## How to check your work

- **Standard output:** compare the program's lines with the expected ones, character by character, including the costs in brackets and the order of the drones.
- **The state after a refusal:** for each refused flight, check that all four fields of the drone are the same as before it. The full list of check cases shows the state of the fleet after each operation.
- **Functions:** does each one have a job that can be described in one sentence? Does the reserve or charging condition also stand in `main`?
- **The result and the effect:** `accepted` says that the function reported a flight. Whether the real record changed is shown only by `After`.

## Hints

<details>
<summary>Hint 1</summary>

Which operations concern one drone, and which the whole fleet? Which of them must search for a record by identifier?

</details>

<details>
<summary>Hint 2</summary>

Check the flight's conditions before changing the battery and the counter. The function that searches for a drone should use the function that performs the flight.

</details>

<details>
<summary>Hint 3</summary>

When charging, go through the real records through a reference, and count only the batteries whose value went up. When a flight is refused, don't change any field.

</details>

## The full list of check cases

<details>
<summary>Open it after preparing your own table</summary>

Each drone is written as its identifier, its battery, its number of flights and whether it's grounded.

| | Fleet | Operations | Results | What it checks |
|---|---|---|---|---|
| A | A-01 65 2 no, B-02 35 0 no, C-03 90 4 yes, D-04 100 1 no | fly B-02 15, B-02 1, C-03 10, BAD-99 10, charge, B-02 80, B-02 1 | accepted, refused, refused, refused, 3, accepted, refused | the data from the requirements |
| B | empty | fly A-01 10, charge | refused, 0 | an empty vector |
| C | S-01 50 0 no | fly S-01 30 | accepted | one drone; exactly 20 is left |
| D | S-01 50 0 no | fly S-01 31 | refused | 19 would be left |
| E | Z-01 80 3 no | fly Z-01 0, Z-01 -5 | refused, refused | a cost of 0 and a negative cost; two refusals in a row |
| F | X-01 30 1 no | fly X-01 40 | refused | a cost larger than the battery |
| G | G-01 100 2 yes | fly G-01 10, charge | refused, 0 | a grounded drone with a full battery |
| H | G-02 40 5 yes, N-01 70 1 no | fly G-02 10, charge, G-02 10 | refused, 2, refused | a grounded drone with a partly charged battery: charging doesn't lift the grounding |
| I | A-01 60 0 no, B-02 60 0 no | fly ZZ-99 10 | refused | an unknown identifier in a non-empty vector |
| J | P-01 80 0 no, P-02 80 0 no, P-03 80 0 no | fly P-03 10, P-02 20, P-01 30 | accepted, accepted, accepted | a match at the last, the middle and the first position |
| K | R-01 60 0 no | fly R-01 30, R-01 20, charge, R-01 20 | accepted, refused, 1, accepted | two flights of one drone; a refusal, then acceptance after charging |
| L | F-01 100 0 no, F-02 100 3 yes | charge, charge | 0, 0 | all the batteries full |
| M | L-01 10 0 no, L-02 99 1 yes, L-03 0 2 no | charge, charge | 3, 0 | no battery full; charging again |

In every case the identifiers, the number of drones and their order don't change. A refused flight changes no field, and charging changes only the battery.

**Automatic tests and your own tries.** All the cases are checked automatically by a check program. It has the same type and the same three functions as the reference solution, but it reads the fleet and the operations from the input, and **prints the state of the whole fleet after each operation**. It's only a checking tool, not part of the test. The check program and its results are with the reference solution.

</details>

## Task 2: Diagnostics

Do this task **after task 1**, before looking at the reference solution. Both problems concern functions similar to yours.

<details>
<summary>Diagnostic A: a copy of the drone changes (open only after task 1)</summary>

In `cpp-workspace`, create a folder `diagnosis_9`, copy `main.cpp` and `CMakeLists.txt` into it from the original `lesson_05_first_program`, and put the program below into `main.cpp`: you can type it or copy it. The rules are the same as in task 1. The fleet is printed by the function `print_fleet`, which only reads the vector. The bug isn't in it.

<!-- example: fleet_copy_bug -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false}
    };
    const std::string id{"B-02"};
    const int cost{0};

    std::cout << "Before:\n";
    print_fleet(drones);

    const bool flown{fly_by_id(drones, id, cost)};

    if (flown) {
        std::cout << "Fly " << id << " (" << cost << "): accepted\n";
    } else {
        std::cout << "Fly " << id << " (" << cost << "): refused\n";
    }

    std::cout << "After:\n";
    print_fleet(drones);
}
```

1. **Predict** the result for the data in the program: a cost of 0, a request that should be refused. Then run the program. Does the result look correct?
2. Change the data so that the bug becomes visible. Write down the correct result and the state of both drones for your data.
3. **Predict** what this program prints for your data: the flight's result and the state of both drones. Then run the program.
4. Point to the place where the copy is made.
5. Explain why the function for one drone's flight works correctly, while the function for a flight by identifier doesn't keep its agreement.
6. Fix the program and run it again for your data.

</details>

<details>
<summary>Diagnostic B: the battery changes before the reserve check (open only after task 1)</summary>

Analyse this fragment **on paper**, without running it. It's another version of the function for one drone's flight:

<!-- fragment -->
```cpp
bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    drone.battery -= cost;

    if (drone.battery < 20) {
        return false;
    }

    ++drone.flights;
    return true;
}
```

The drone has a battery of 25, isn't grounded, and has 3 flights. The requested flight costs 10.

1. What's the correct result, and the drone's state after this request?
2. What does this version return, and what state of the drone does it leave?
3. Which check comes too late? Why does that break the "all or nothing" rule?
4. Why doesn't `return false;` undo the earlier change?
5. How do you change the order so that a refusal changes nothing?

</details>

The results, example data and fixes are in [Diagnostics: results and fixes](#diagnostics-results-and-fixes).

## Task 3: Explain your design

Answer briefly, in writing, referring to your own program from task 1, before you open the reference solution:

1. Why does the function for one drone's flight get the record through `&`, and both fleet functions get the vector through `&`? Why do the loop variables in those functions also have `&`?
2. What does `false` returned by the function for a flight by identifier mean? Does it tell you whether the drone exists?
3. Why is a battery of 20 after the flight allowed, but not 19? Point to these cases in your table.
4. Why must a refused flight not change any field? What would happen to this drone's later flights if a refusal changed the battery?
5. Why doesn't charging change the grounding or the number of flights, and why isn't a drone with a battery of 100 counted?
6. Why must all seven operations work on the same vector? What do the two flights of `B-02` with a charge between them show?
7. Does an `accepted` result prove that the right record changed? How do you check it?
8. Why does only one function know the rules of a flight? What jobs do the other two have?

## The reference solution

Look here **after doing tasks 1–3**. Your names and the layout of `main` may differ, as long as the program meets the requirements.

<details>
<summary>Task 1: a delivery drone fleet</summary>

<!-- example: drone_fleet -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

std::size_t charge_fleet(std::vector<Drone>& drones) {
    std::size_t charged{0};

    for (Drone& drone : drones) {
        if (drone.battery < 100) {
            drone.battery = 100;
            ++charged;
        }
    }

    return charged;
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false},
        {"C-03", 90, 4, true},
        {"D-04", 100, 1, false}
    };

    std::cout << "Drones: " << drones.size() << "\n";
    std::cout << "Before:\n";

    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }

    const bool first_flight{fly_by_id(drones, "B-02", 15)};

    if (first_flight) {
        std::cout << "Fly B-02 (15): accepted\n";
    } else {
        std::cout << "Fly B-02 (15): refused\n";
    }

    const bool second_flight{fly_by_id(drones, "B-02", 1)};

    if (second_flight) {
        std::cout << "Fly B-02 (1): accepted\n";
    } else {
        std::cout << "Fly B-02 (1): refused\n";
    }

    const bool third_flight{fly_by_id(drones, "C-03", 10)};

    if (third_flight) {
        std::cout << "Fly C-03 (10): accepted\n";
    } else {
        std::cout << "Fly C-03 (10): refused\n";
    }

    const bool fourth_flight{fly_by_id(drones, "BAD-99", 10)};

    if (fourth_flight) {
        std::cout << "Fly BAD-99 (10): accepted\n";
    } else {
        std::cout << "Fly BAD-99 (10): refused\n";
    }

    const std::size_t charged{charge_fleet(drones)};

    std::cout << "Charged: " << charged << "\n";

    const bool fifth_flight{fly_by_id(drones, "B-02", 80)};

    if (fifth_flight) {
        std::cout << "Fly B-02 (80): accepted\n";
    } else {
        std::cout << "Fly B-02 (80): refused\n";
    }

    const bool sixth_flight{fly_by_id(drones, "B-02", 1)};

    if (sixth_flight) {
        std::cout << "Fly B-02 (1): accepted\n";
    } else {
        std::cout << "Fly B-02 (1): refused\n";
    }

    std::cout << "After:\n";

    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}
```

1. **One type is enough,** because every operation changes drones, and the results are a single `bool` answer or one number. A separate summary type isn't needed.
2. **`fly` gets `Drone&`,** because a flight must change the existing record, not a copy of it.
3. **`fly_by_id` gets `std::vector<Drone>&`** and goes through it with a `Drone&` loop, because the drone found must change in the vector from `main`.
4. **The identifier through `const std::string&`,** because the function only reads and compares it.
5. **`charge_fleet` uses a `Drone&` loop,** because it changes the batteries of the real elements. A loop without `&` would change copies.
6. **`bool` means the flight's success, not finding the drone:** `false` means "the flight didn't happen", because the drone is missing or because of a refusal.
7. **A cost of 0 and a negative cost are refused,** because a flight for 0 would add a flight without using the battery, and a negative cost would raise the battery. The check stands first, so the reserve is computed only for a positive cost.
8. **A grounded drone is refused** whatever its battery: that's the second condition of the same clause.
9. **A battery of 20 after the flight is allowed,** because the reserve is "at least 20". The refusal condition is `drone.battery - cost < 20`, and 20 isn't less than 20.
10. **19 means a refusal,** because 19 is less than 20.
11. **On a refusal nothing changes,** because both guard clauses stand before the changes. The expression in the condition computes the planned battery, and the field changes only after the check.
12. **Charging doesn't change `grounded`,** because grounding is a separate decision, not a battery state. C-03 still can't fly after charging.
13. **Charging doesn't increase `flights`,** because no flight happened.
14. **A drone with a battery of 100 isn't counted,** because its battery doesn't change, and the result must tell about real changes.
15. **Later calls use the state left by the earlier ones,** because all of them concern the same vector: the second flight of `B-02` sees a battery of 20, and the flight for 80 is possible only after charging.
16. **A new collection isn't needed,** because the fleet represents the current state, and the state before the operations isn't needed in the report.
17. **`accepted` doesn't prove that the original changed:** a function can correctly change a copy and report a flight (diagnostic A). Only the state in `After` proves it.
18. **Three responsibilities:** `fly` knows the rules of one flight and protects the state of one drone; `fly_by_id` finds the right record and passes it to `fly`; `charge_fleet` changes all the records that need it.

**Other correct solutions:**

- one guard clause with three conditions joined by `||`, as long as the cost is checked first;
- the reserve condition written as `cost > drone.battery - 20`;
- a local constant, for example `const int reserve{20};`, in the flight function;
- your own function that prints the fleet, gets the vector through `const&`, and is called for `Before` and `After`;
- a separate function that charges one drone, called by the function for charging the fleet.

This isn't the only correct solution.

**The empty-vector variant:**

<!-- example: drone_fleet_empty -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

std::size_t charge_fleet(std::vector<Drone>& drones) {
    std::size_t charged{0};

    for (Drone& drone : drones) {
        if (drone.battery < 100) {
            drone.battery = 100;
            ++charged;
        }
    }

    return charged;
}

int main() {
    std::vector<Drone> drones{};

    std::cout << "Drones: " << drones.size() << "\n";

    const bool flown{fly_by_id(drones, "A-01", 10)};

    if (flown) {
        std::cout << "Fly A-01 (10): accepted\n";
    } else {
        std::cout << "Fly A-01 (10): refused\n";
    }

    const std::size_t charged{charge_fleet(drones)};

    std::cout << "Charged: " << charged << "\n";
}
```

For an empty vector both loops make zero passes: `fly_by_id` reaches the `return false;` after the loop, and `charge_fleet` returns 0. No element is read.

**The check program** checks all the cases of the check list. The type and the three functions are the same as above. The difference is in `main`: the program reads the number of drones, then each drone (its identifier, battery, number of flights, and `yes` or `no` for grounding), and then the number of operations. Each drone goes to the end of the vector with `push_back`, as in the check programs of lessons 8.4–9.4. It reads each operation, `fly` with an identifier and a cost, or `charge`, one at a time, only in the loop over the operations, and performs it at once. **After each operation it prints the state of the whole fleet**, so that the state after a refusal is visible at once. The printing is done by the function `print_fleet`, which only reads the vector.

<!-- example: drone_fleet_check -->
```cpp
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

std::size_t charge_fleet(std::vector<Drone>& drones) {
    std::size_t charged{0};

    for (Drone& drone : drones) {
        if (drone.battery < 100) {
            drone.battery = 100;
            ++charged;
        }
    }

    return charged;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{};
    int count{0};

    std::cin >> count;

    for (int number{1}; number <= count; ++number) {
        std::string id{};
        int battery{0};
        int flights{0};
        std::string grounded_answer{};

        std::cin >> id;
        std::cin >> battery;
        std::cin >> flights;
        std::cin >> grounded_answer;

        const Drone drone{id, battery, flights, grounded_answer == "yes"};
        drones.push_back(drone);
    }

    int operation_count{0};
    std::cin >> operation_count;

    if (std::cin.fail()) {
        std::cout << "Input could not be read\n";
    } else {
        std::cout << "Drones: " << drones.size() << "\n";
        std::cout << "Before:\n";
        print_fleet(drones);

        for (int number{1}; number <= operation_count; ++number) {
            std::string operation{};
            std::cin >> operation;

            if (operation == "fly") {
                std::string id{};
                int cost{0};

                std::cin >> id;
                std::cin >> cost;

                const bool flown{fly_by_id(drones, id, cost)};

                if (flown) {
                    std::cout << "Fly " << id << " (" << cost << "): accepted\n";
                } else {
                    std::cout << "Fly " << id << " (" << cost << "): refused\n";
                }
            } else {
                const std::size_t charged{charge_fleet(drones)};

                std::cout << "Charged: " << charged << "\n";
            }

            print_fleet(drones);
        }
    }
}
```

Each case starts with the number of drones. Then each drone takes one line: its identifier, battery, number of flights and grounding. Next come the number of operations and the operations, one per line. The cases are in the order of the check list, from A to M.

<!-- input: drone_fleet_check -->
```text
4
A-01 65 2 no
B-02 35 0 no
C-03 90 4 yes
D-04 100 1 no
7
fly B-02 15
fly B-02 1
fly C-03 10
fly BAD-99 10
charge
fly B-02 80
fly B-02 1
```

<!-- output: drone_fleet_check -->
```text
Drones: 4
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (15): accepted
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (1): refused
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly C-03 (10): refused
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly BAD-99 (10): refused
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
C-03: battery 90, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Charged: 3
A-01: battery 100, flights 2, grounded no
B-02: battery 100, flights 1, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (80): accepted
A-01: battery 100, flights 2, grounded no
B-02: battery 20, flights 2, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
Fly B-02 (1): refused
A-01: battery 100, flights 2, grounded no
B-02: battery 20, flights 2, grounded no
C-03: battery 100, flights 4, grounded yes
D-04: battery 100, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
0
2
fly A-01 10
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 0
Before:
Fly A-01 (10): refused
Charged: 0
```

<!-- input: drone_fleet_check -->
```text
1
S-01 50 0 no
1
fly S-01 30
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
S-01: battery 50, flights 0, grounded no
Fly S-01 (30): accepted
S-01: battery 20, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
S-01 50 0 no
1
fly S-01 31
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
S-01: battery 50, flights 0, grounded no
Fly S-01 (31): refused
S-01: battery 50, flights 0, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
Z-01 80 3 no
2
fly Z-01 0
fly Z-01 -5
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
Z-01: battery 80, flights 3, grounded no
Fly Z-01 (0): refused
Z-01: battery 80, flights 3, grounded no
Fly Z-01 (-5): refused
Z-01: battery 80, flights 3, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
X-01 30 1 no
1
fly X-01 40
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
X-01: battery 30, flights 1, grounded no
Fly X-01 (40): refused
X-01: battery 30, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
G-01 100 2 yes
2
fly G-01 10
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
G-01: battery 100, flights 2, grounded yes
Fly G-01 (10): refused
G-01: battery 100, flights 2, grounded yes
Charged: 0
G-01: battery 100, flights 2, grounded yes
```

<!-- input: drone_fleet_check -->
```text
2
G-02 40 5 yes
N-01 70 1 no
3
fly G-02 10
charge
fly G-02 10
```

<!-- output: drone_fleet_check -->
```text
Drones: 2
Before:
G-02: battery 40, flights 5, grounded yes
N-01: battery 70, flights 1, grounded no
Fly G-02 (10): refused
G-02: battery 40, flights 5, grounded yes
N-01: battery 70, flights 1, grounded no
Charged: 2
G-02: battery 100, flights 5, grounded yes
N-01: battery 100, flights 1, grounded no
Fly G-02 (10): refused
G-02: battery 100, flights 5, grounded yes
N-01: battery 100, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
2
A-01 60 0 no
B-02 60 0 no
1
fly ZZ-99 10
```

<!-- output: drone_fleet_check -->
```text
Drones: 2
Before:
A-01: battery 60, flights 0, grounded no
B-02: battery 60, flights 0, grounded no
Fly ZZ-99 (10): refused
A-01: battery 60, flights 0, grounded no
B-02: battery 60, flights 0, grounded no
```

<!-- input: drone_fleet_check -->
```text
3
P-01 80 0 no
P-02 80 0 no
P-03 80 0 no
3
fly P-03 10
fly P-02 20
fly P-01 30
```

<!-- output: drone_fleet_check -->
```text
Drones: 3
Before:
P-01: battery 80, flights 0, grounded no
P-02: battery 80, flights 0, grounded no
P-03: battery 80, flights 0, grounded no
Fly P-03 (10): accepted
P-01: battery 80, flights 0, grounded no
P-02: battery 80, flights 0, grounded no
P-03: battery 70, flights 1, grounded no
Fly P-02 (20): accepted
P-01: battery 80, flights 0, grounded no
P-02: battery 60, flights 1, grounded no
P-03: battery 70, flights 1, grounded no
Fly P-01 (30): accepted
P-01: battery 50, flights 1, grounded no
P-02: battery 60, flights 1, grounded no
P-03: battery 70, flights 1, grounded no
```

<!-- input: drone_fleet_check -->
```text
1
R-01 60 0 no
4
fly R-01 30
fly R-01 20
charge
fly R-01 20
```

<!-- output: drone_fleet_check -->
```text
Drones: 1
Before:
R-01: battery 60, flights 0, grounded no
Fly R-01 (30): accepted
R-01: battery 30, flights 1, grounded no
Fly R-01 (20): refused
R-01: battery 30, flights 1, grounded no
Charged: 1
R-01: battery 100, flights 1, grounded no
Fly R-01 (20): accepted
R-01: battery 80, flights 2, grounded no
```

<!-- input: drone_fleet_check -->
```text
2
F-01 100 0 no
F-02 100 3 yes
2
charge
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 2
Before:
F-01: battery 100, flights 0, grounded no
F-02: battery 100, flights 3, grounded yes
Charged: 0
F-01: battery 100, flights 0, grounded no
F-02: battery 100, flights 3, grounded yes
Charged: 0
F-01: battery 100, flights 0, grounded no
F-02: battery 100, flights 3, grounded yes
```

<!-- input: drone_fleet_check -->
```text
3
L-01 10 0 no
L-02 99 1 yes
L-03 0 2 no
2
charge
charge
```

<!-- output: drone_fleet_check -->
```text
Drones: 3
Before:
L-01: battery 10, flights 0, grounded no
L-02: battery 99, flights 1, grounded yes
L-03: battery 0, flights 2, grounded no
Charged: 3
L-01: battery 100, flights 0, grounded no
L-02: battery 100, flights 1, grounded yes
L-03: battery 100, flights 2, grounded no
Charged: 0
L-01: battery 100, flights 0, grounded no
L-02: battery 100, flights 1, grounded yes
L-03: battery 100, flights 2, grounded no
```

</details>

## Diagnostics: results and fixes

<details>
<summary>Diagnostic A: a copy of the drone changes</summary>

Before the fix, for a cost of 0:

<!-- output: fleet_copy_bug -->
```text
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
Fly B-02 (0): refused
After:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
```

- **For a cost of 0 the result is correct,** because the function for one drone's flight refuses such a request before changing anything. The correct version also returns `false` and changes nothing.
- **Data that reveal the bug:** any flight that should be accepted. For example `B-02` with a cost of 15. The correct result is `accepted` and `B-02: battery 20, flights 1`. The buggy program prints:

<!-- example: fleet_copy_revealed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false}
    };
    const std::string id{"B-02"};
    const int cost{15};

    std::cout << "Before:\n";
    print_fleet(drones);

    const bool flown{fly_by_id(drones, id, cost)};

    if (flown) {
        std::cout << "Fly " << id << " (" << cost << "): accepted\n";
    } else {
        std::cout << "Fly " << id << " (" << cost << "): refused\n";
    }

    std::cout << "After:\n";
    print_fleet(drones);
}
```

<!-- output: fleet_copy_revealed -->
```text
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
Fly B-02 (15): accepted
After:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
```

| Moment | `drone` in the loop (a copy) | `B-02` in the vector |
|---|---|---|
| before the call | doesn't exist | battery 35, flights 0 |
| the second pass: `drone.id == id` | a copy of `B-02`: battery 35, flights 0 | battery 35, flights 0 |
| after `fly(drone, cost)` | battery 20, flights 1; the result `true` | battery 35, flights 0 |
| after returning to `main` | doesn't exist | battery 35, flights 0 |

- **Where the copy is made:** in the loop `for (Drone drone : drones)`. In each pass, `drone` is a new object with the values of the current element.
- **`fly` works correctly:** it checks the conditions, changes the object it gets, and reports the flight. But it gets a copy. `fly_by_id` breaks its agreement: it reports a performed flight, while the drone in the vector doesn't change.
- **The result doesn't replace checking the effect.** `accepted` is printed, and the state in `After` is old. If the report showed only the results, the bug would go unnoticed.
- **The fix:** the loop variable `Drone& drone`. The compiler reports no error in the version with a copy, because it's valid C++: changing a copy is allowed, it just doesn't fit the function's job.

<!-- example: fleet_copy_fixed -->
```cpp
#include <iostream>
#include <string>
#include <vector>

struct Drone {
    std::string id;
    int battery;
    int flights;
    bool grounded;
};

bool fly(Drone& drone, int cost) {
    if (cost <= 0 || drone.grounded) {
        return false;
    }

    if (drone.battery - cost < 20) {
        return false;
    }

    drone.battery -= cost;
    ++drone.flights;
    return true;
}

bool fly_by_id(std::vector<Drone>& drones, const std::string& id, int cost) {
    for (Drone& drone : drones) {
        if (drone.id == id) {
            return fly(drone, cost);
        }
    }

    return false;
}

void print_fleet(const std::vector<Drone>& drones) {
    for (const Drone& drone : drones) {
        std::cout << drone.id << ": battery " << drone.battery << ", flights " << drone.flights << ", grounded ";

        if (drone.grounded) {
            std::cout << "yes\n";
        } else {
            std::cout << "no\n";
        }
    }
}

int main() {
    std::vector<Drone> drones{
        {"A-01", 65, 2, false},
        {"B-02", 35, 0, false}
    };
    const std::string id{"B-02"};
    const int cost{15};

    std::cout << "Before:\n";
    print_fleet(drones);

    const bool flown{fly_by_id(drones, id, cost)};

    if (flown) {
        std::cout << "Fly " << id << " (" << cost << "): accepted\n";
    } else {
        std::cout << "Fly " << id << " (" << cost << "): refused\n";
    }

    std::cout << "After:\n";
    print_fleet(drones);
}
```

<!-- output: fleet_copy_fixed -->
```text
Before:
A-01: battery 65, flights 2, grounded no
B-02: battery 35, flights 0, grounded no
Fly B-02 (15): accepted
After:
A-01: battery 65, flights 2, grounded no
B-02: battery 20, flights 1, grounded no
```

For a cost of 0 the fixed program prints the same as before the fix. That's why a refused request isn't enough to check whether the function changes the real element.

</details>

<details>
<summary>Diagnostic B: the battery changes before the reserve check</summary>

1. **Correctly:** a refusal, because 25 − 10 = 15, which is less than the reserve 20. The drone stays unchanged: battery 25, 3 flights.
2. **This version** returns `false`, but leaves a battery of 15. The number of flights stays 3, because `++drone.flights;` stands after the second check. The record is partly changed.
3. **The reserve check comes too late.** The function changes the battery before it knows whether the flight is allowed. A refusal should leave all the fields unchanged, and here one field has already changed: that breaks the "all or nothing" rule from lesson 9.2.
4. **`return false;` only ends the function** and passes on the result. It doesn't restore the earlier values of the fields: the change of the battery has already happened on the real record.
5. **The fix:** check the reserve on the planned battery before you change the field, for example `if (drone.battery - cost < 20) { return false; }`, and make both changes only after all the checks, as in the reference solution.

Such a bug is easy to miss in the whole sequence: a later charge sets the battery to 100 and hides the change made by the refused flight. That's why the state after a refusal is checked right after it.

</details>

## Answers to task 3

<details>
<summary>Sample answers</summary>

1. Because all three functions must change the existing data from `main`. The record through `&` gives access to the real drone, the vector through `&` to the real fleet, and the `&` loop variable to its real elements. Without any of them, a copy would change.
2. That the flight didn't happen and nothing changed. You can't tell whether the drone was missing or the flight was refused: the result tells only about the operation's success, as in lesson 9.4.
3. Because the reserve is "at least 20 after the flight", and the refusal condition is a battery after the flight less than 20. In the check list, case C leaves exactly 20 and is accepted, and case D would leave 19 and is refused.
4. Because the agreement says that a refusal changes nothing. If a refusal lowered the battery, this drone's later flights would see a battery that's too low and could be refused for no reason, and the report would show a state that doesn't exist.
5. Because charging concerns only the battery: the grounding and the flights are different information, and no flight happened. A drone with a battery of 100 doesn't change, so it isn't counted: the result must tell about real changes.
6. Because each operation must start from the state left by the earlier ones. The second flight of `B-02` for 1 is refused, because 20 is left; the flight for 80 is possible only after charging, and the last flight for 1 runs into the reserve again.
7. No. A function can change a copy and report a flight, as in diagnostic A. I check it with the state of the fleet in `After`, and with the check cases, which show the state after each operation.
8. Because the rule should be in one place, and changing it should require fixing one function. The function for a flight by identifier only finds the drone and passes it to the flight function. The charging function has its own, different rule, and doesn't need the rules of a flight.

</details>

## Self-assessment

For each criterion, mark one answer:

| Criterion | On my own | With a hint | After looking at the solution | To revise |
|---|---|---|---|---|
| Designing the drone type | | | | |
| The vector of drones initialised in the code | | | | |
| The flight function: `&`, all the conditions before the change, two fields | | | | |
| The reserve: the boundary of 20 and 19 | | | | |
| A cost of 0 and a negative cost, grounding | | | | |
| The function for a flight by identifier, and `return false;` after the loop | | | | |
| Charging: only the battery, counting real changes | | | | |
| A grounded drone and charging | | | | |
| Seven operations on the same vector | | | | |
| The empty-vector variant | | | | |
| The case table and the state after a refusal | | | | |
| Diagnostic A (a copy of the drone changes) | | | | |
| Diagnostic B (the battery before the reserve check) | | | | |
| The explanations of task 3 | | | | |

If anything is marked in the "To revise" column, go back to the matching lesson:

| Topic | Lesson |
|---|---|
| a function changes a record through `T&` | [9.1](lesson_01_a_function_changes_a_record.en.md) |
| checking before the change, a `bool` result, all or nothing | [9.2](lesson_02_a_change_only_when_allowed.en.md) |
| changing the elements of a vector, two levels of `&`, a counter of real changes | [9.3](lesson_03_changing_vector_elements.en.md) |
| finding a record, `return` in the loop and after it | [9.4](lesson_04_find_a_record_and_change_it.en.md) |
| guard clauses | [5.4](../module_05_functions/lesson_04_several_returns.en.md) |
| joining conditions and short-circuit evaluation | [3.4](../module_03_decisions_and_conditions/lesson_04_combining_conditions.en.md) |
| a vector of records and `std::size_t` | [8.4](../module_08_structs/lesson_04_many_records_in_a_vector.en.md) |

Then try the task again, for example for a scooter rental where a ride needs a battery reserve, and blocked scooters can be charged but not rented.

---

## Module 9 summary

After five lessons, you can:

- pass an existing record through `T&` when the function's job is to change it, and tell that from passing it by value and through `const&`;
- write functions that check all the conditions before the change, change nothing on a refusal, and return `bool`;
- change the elements of an existing vector in a function with a `std::vector<T>&` parameter and a `T&` loop, counting only real changes;
- find a record by a unique identifier and change only that one, with `return` in the loop and `return false;` after it;
- tell a function's result from its effect, and check the state of the data, not just the message;
- choose data that reveal a change to a copy, a partial change, and a `return` that comes too early.

## What's next

This is the last lesson of Module 9. The next modules of the course are in preparation.

**Previous lesson:** [Lesson 9.4: Find a record and change the right object](lesson_04_find_a_record_and_change_it.en.md) · **Next lesson:** in preparation · [Course overview](../../README.en.md)
