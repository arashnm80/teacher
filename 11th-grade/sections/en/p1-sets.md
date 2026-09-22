# Working with functions and modules


---

**Page 48**

## Learning unit 2

## Working with functions and modules

### Have you ever thought

If you want to build a set of numbers without duplicates, or keep the order of data and make it unchangeable, what data type do you use?

Suppose you want to store a student’s information such as name, age, and scores and access each item quickly—what data structure is suitable?

If you want to use a specific action several times in a program without repeating the code, what approach is there?

How can you process a large amount of data in a function or perform repeated operations without making the code long?

How can you use ready-made code written by others? What is the difference between a function and a method?

### By the end, the student is expected to

1 Define sets and tuples, add or remove their elements, and know the use of each.

2 Build a dictionary, add keys and values, retrieve data by keys, and know the use of a dictionary for storing information.

3 Be able to write simple functions, use parameters and arguments, and receive and use a function’s return value.

4 Be able to write more complex functions, use loops inside functions, and manage repeated operations in functions.

5 Import modules, use ready-made functions and classes in their program, and identify Python’s standard modules.

6 Create and use local modules.

### Performance standard

The student can create and use functions and modules, manage data and repeated operations with functions, benefit from local modules, and recognize the difference between a function and a method.


---

**Page 49**

In programming, as programs grow larger and more complex, the need to organize and reuse code is felt more. Functions and modules are tools that help the programmer make code tidy, understandable, and reusable. In this learning unit, you become familiar with building functions, using parameters and return values, writing advanced functions with loops, and using ready-made modules and local modules. By learning these concepts, you can create more organized and professional programs.

### Sets (set)

![Book image](../images/p055-01.png)

Sets are used to store several values in one variable. A set is one of Python’s four data types used to store data types such as integers, floating-point numbers, strings, booleans, and tuples (`tuple`) as a collection.

**Figure 97**

Building a `set` :

Using braces {}:

This method is usually used to build a set of specific, predetermined elements.

After each run of the program, you will see that the display order of the set members changes (Figure 98).

That is, a `set` does not guarantee the display order of elements and is `Unordered`.

![Book image](../images/p055-02.png)

1

2

3

**Figure 98**


---

**Page 50**

Using the (`add`) method to add a new element to a `set:`

Run the program. You will see that duplicate elements were not added to the set (Figure 99).

![Book image](../images/p056-01.png)

![Figure 99](../images/p056-02.png)

**Figure 99**

Using the (`remove`) method to remove an element from a `set:`

With the `remove` method, you can remove elements from a `set`.

Example: Using the `remove` method, the element `"banana"` has been removed from the set (Figure 100).

![Book image](../images/p056-03.png)

![Figure 100](../images/p056-04.png)

**Figure 100**

If the member does not exist, an error message is shown at run time (Figure 101).

![Book image](../images/p056-05.png)

![Figure 101](../images/p056-06.png)

**Figure 101**

### Try this

Research the other methods related to `set` on the site `www.w3schools.com` and present them in class.


---

**Page 51**

Using `in` to check whether an element exists in a `set:`

![Figure 102](../images/p057-01.png)

**Figure 102**

Example: In the code in Figure 103, the existence of the element `"grape"` in the `fruits` set is checked. The output of the code shows that this element does not exist in the set.

![Book image](../images/p057-02.png)

![Figure 103](../images/p057-03.png)

**Figure 103**

### Activity

Write a program that has a `set` of numbers and checks whether the number 10 exists in the `set` or not.

### Activity

There is a set of fruits:

```
}"fruits = {"apple", "banana", "orange", "grape
```

Write a program in which the user enters a fruit name and, if it is in the `set`, displays a message that the fruit exists in the set, and print the final `set`.


---
