<!-- page 70 -->

> **Activity**
>
> ![Book image](../images/p076-01.png)
>
> Write a function that calculates and returns the difference between two students' grades. With your teacher's guidance, explain the code of the program opposite.

### Kinds of functions in Python

**User-Defined Function (functions that the programmer defines)**: the functions you have defined so far are in this category.

**Built-in functions (or Python's internal functions)**: functions that are already defined in Python and that the programmer uses in their programs. They do common and repeated jobs quickly, simply and without writing long code. With the help of built-in functions, programs become more readable, shorter and less error-prone.

You have met some of these functions in earlier sections, and you will learn others below. Math functions: these functions work only or mainly on numbers (Table 4).

*Table 4*

| Function name | Use | Example | Output |
| --- | --- | --- | --- |
| `abs()` | Absolute value of a number | `print(abs(-12))` | 12 |
| `round()` | Round a decimal number | `print(round(3.6))`<br>`print(round(3.1415, 2))` | 4<br>3.14 |
| `pow()` | Power | `print(pow(2, 3))` | 8 |
| `int()` | Convert to an integer | `print(int(4.8))` | 4 |
| `float()` | Convert to a decimal number | `print(float(5))` | 5.0 |
| `max()` | Largest number | `print(max(3, 9, 5))` | 9 |
| `min()` | Smallest number | `print(min(3, 9, 5))` | 3 |
| `sum()` | Sum of several numbers | `print(sum([2, 4, 6]))` | 12 |

<!-- page 71 -->

> **Activity**
>
> Build a calculator with math functions. Parts of the code for this program are written. With your teacher's guidance, complete them and run the program.
>
> ![Book image](../images/p077-01.png)
>
> ![Book image](../images/p077-02.png)

<!-- page 72 -->

> **Activity (continued)**
>
> ![Book image](../images/p078-01.png)

So far you have met functions such as print, len, type, input, and str. Next you will meet some of Python's built-in functions that are not about math.

**The sorted function**: used to sort strings, sets, tuples, and dictionaries; it returns the result as a new list.

### General form of the function

```
sorted(iterable, reverse=false)
```

**iterable**: the data you want to sort (list, string, tuple, set, dictionary, …)

**reverse**: if true, the order is descending. Default: false (ascending)

<!-- page 73 -->

**Example**: in this example sorted sorts the string of characters stored in the data variable in ascending order, by the characters' ASCII codes.

![Figure 149](../images/p079-01.png)
*Figure 149*

> **Activity**
>
> Get city names from the user and store them in a list. Then sort the list in descending order.

## Modules (module)

A module is a file that can contain several functions, variables, and classes, and it is used to organize large programs. With modules you can reuse ready-made code and keep your program shorter and tidier.

![Figure 150](../images/p079-02.png)
*Figure 150*

### Types of modules in Python: the standard module

Python has modules that the programmer just brings into the program without defining them, such as time, date, random, math, and so on. Standard modules can be used in two ways.

### The first way: importing the whole module (import module)

This is the safest way, because it prevents name clashes. In this method you must write the module name before the function.

![Figure 151](../images/p079-03.png)
*Figure 151*

Example: sqrt is a ready-made function in Python's math module, used to calculate the square root of numbers (Figure 151).
