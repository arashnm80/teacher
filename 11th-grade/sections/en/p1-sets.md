<!-- page 48 -->

## Learning unit 2

## Have you ever thought about this

- If you want to build a collection of numbers with no repeats, or keep the order of the data and make it unchangeable, which data type do you use?

- Suppose you want to store a student's information, such as name, age, and grades, and get to each item quickly. Which data structure is suitable?

- If you want to use a certain operation several times in a program without repeating the code, what can you do?

- How can you process a lot of data or do repeated operations in a function without making the code long?

- How can you use code that others have already written? What is the difference between a function and a method?

## By the end, the student is expected to

1. Define sets and tuples, add or remove their elements, and know what each is used for.

2. Build a dictionary, add keys and values, retrieve data by key, and know how dictionaries are used to store information.

3. The student can write simple functions, use parameters and arguments, and receive and use a function's return value.

4. The student can write more complex functions, use loops in functions, and handle repeated operations in functions.

5. Import modules, use ready-made functions and classes in their program, and recognize Python's standard modules.

6. Create and use local modules.

## Performance standard

The student can create and use functions and modules, handle data and repeated operations with functions, make use of local modules, and tell the difference between a function and a method.

<!-- page 49 -->

In programming, the bigger and more complex programs get, the more you need to organize and reuse code. Functions and modules are tools that help programmers keep their code tidy, understandable, and reusable. In this learning unit you will learn to build functions, use parameters and return values, write advanced functions with loops, and use ready-made and local modules. With these concepts you can build more organized and professional programs.

## Sets (set)

![Figure 97](../images/p055-01.png)
*Figure 97*

Sets are used to store several values in one variable. A set is one of Python's four collection data types and is used to store data such as integers, decimal numbers, strings, booleans, and tuples (tuple) as a collection.

### Creating a set

**Using curly braces** {}:

This method is usually used to build a set of specific, predefined elements.

Each time you run the program you will see that the members of the set are shown in a different order (Figure 98). That is, a set does not guarantee the order of its elements; it is unordered (Unorder).

![Figure 98](../images/p055-02.png)
*Figure 98*

<!-- page 50 -->

### Using the add method to add a new element to a set

Run the program. You will see that duplicate elements are not added to the set (Figure 99).

![Figure 99](../images/p056-01.png)
*Figure 99*

### Using the remove method to remove an element from a set

With the remove method you can remove elements of a set.

**Example**: the element "banana" is removed from the set with the remove method (Figure 100).

![Figure 100](../images/p056-02.png)
*Figure 100*

If the member does not exist, an error message is shown when the program runs (Figure 101).

![Figure 101](../images/p056-03.png)
*Figure 101*

> **Curiosity**
>
> Research the other set methods on www.w3schools.com and present them in class.

<!-- page 51 -->

### Using in to check whether an element is in a set

![Figure 102](../images/p057-01.png)
*Figure 102*

**Example**: in the code of Figure 103, the existence of the element "**grape**" in the set **fruits** is checked. The output of the code shows that this element does not exist in the set.

![Figure 103](../images/p057-02.png)
*Figure 103*

> **Activity**
>
> Write a program that has a **set** of numbers and checks whether the number 10 is in the **set**.

> **Activity**
>
> There is a set of fruits:
>
> ```
> fruits = {"apple", "banana", "orange", "grape"}
> ```
>
> Write a program in which the user enters the name of a fruit; if it is in the **set**, show a message saying the fruit is in the set, and print the final **set**.
