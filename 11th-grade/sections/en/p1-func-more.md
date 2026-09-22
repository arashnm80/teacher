**Page 70**

### Activity

![Book image](../images/p076-01.png)

Write a function that calculates the difference between two students’ scores and returns that value. With guidance from your teacher, explain the code of the program opposite.

Types of functions in Python `User-Defined` `Function` (functions that the programmer defines): The functions you have defined so far belong in this category.

`Built-in` `functions` (or Python’s internal functions): Functions that are already defined in Python and that the programmer uses in their programs. They perform common and repeated tasks quickly, simply, and without writing long code. With built-in functions, programs become more readable, shorter, and less error-prone.

In earlier sections you became familiar with some of these functions; below you will also learn the use of some others.

Math functions: These functions work only or mainly on numeric values (Table 4).

**Table 4**

Function name

### Use

### Example

Output

`abs`()calculates the absolute value of a number`print`(`abs`(-12))

12

```
print(round(3.6))
```

4

```
round()گرد کردن عدد اعشاریprint(round(3.1415, 2))
```

3.14

```
pow()محاسبه توانprint(pow(2, 3))
```

8

`int`()converts to an integer`print`(`int`(4.8))

4

`float`()converts to a floating-point number`print`(`float`(5))

50

```
max()بزرگ‌ترین عددPrint(max(3, 9, 5))
```

9

```
min()کوچک‌ترین عددPrint(min(3, 9, 5))
```

3

```
sum()جمع چند عددPrint(sum([2, 4, 6]))
```

12


---

**Page 71**

### Activity

Create a calculator using math functions. Parts of the code related to this program have been written. With guidance from your teacher, complete them and run the program.

![Book image](../images/p077-01.png)

![Book image](../images/p077-02.png)


---

**Page 72**

![Book image](../images/p078-03.png)

![Book image](../images/p078-01.png)

![Book image](../images/p078-02.png)

Up to this section you have become familiar with functions such as `print` ,`len` ,`type` , `input` ,`str`. Below you will become familiar with some of Python’s non-math built-in functions.

The `sorted` function: This function is used to sort a string, set, tuple, and dictionary and returns the result as a new list.

General structure of the function:

```
sorted(iterable, reverse=false)
```

`iterable:` the data you want to sort (list, string, tuple, set, dictionary, and so on) `reverse:` if `true`, the order becomes descending. Default (`false` ascending)


---

**Page 73**

Example: In this example the `sorted` function sorts a string of characters stored in the variable `data` in ascending order based on the ASCII codes of the characters.

![Book image](../images/p079-01.png)

![Figure 149](../images/p079-02.png)

**Figure 149**

### Activity

Receive the names of cities from the user and store them in a list. Then sort this list in descending order.

### Module (module)

A module is a file that can include several functions, variables, and classes and is used to organize large programs. Using a module, you can reuse ready-made code and make your program shorter and tidier.

![Figure 150](../images/p079-03.png)

**Figure 150**

Types of modules in Python:

Standard module (`standard`) There are modules in Python that the programmer only imports into their own program and does not need to define. Such as `time`, `date`, `random`, `math`, and so on. There are two ways to use standard modules.

First method: importing the whole module (`import` `mojvle`):

This is the safest way, because it prevents name conflicts. In this method you must put the module name before the function.

![Book image](../images/p079-04.png)

Example: `Sqrt` is a ready-made function in Python’s `math` module, which is used to calculate the square root of numbers (Figure 151).

**Figure 151**


---
