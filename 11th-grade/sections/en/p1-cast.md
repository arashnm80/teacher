**Page 13**

This statement receives the value entered through the keyboard as a string (`string`), and its output is a string value (even if you entered a "number") (Figure 25).

### Activity

Define the variables `food`, `weighe`, and `avg` in order for your favorite food, your weight, and your grade average. Receive a value from input for each one, then display the values and determine the type of each one.

![Book image](../images/p019-02.png)

![Figure 25](../images/p019-03.png)

**Figure 25**

### Type casting in Python

In Python programming, sometimes you need to convert one data type to another. This is called type casting or `Type` `Casting`.

![Figure 26](../images/p019-01.png)

**Figure 26**

For example, when you receive input with the ()`input` function, the entered value is stored as a string (`str`). If you want to perform mathematical calculations with it, you need to convert it to a number.

Python provides the programmer with ready-made functions for type casting, such as:

Convert to integer → )(`int` Convert to floating-point number → )(`float` Convert to string → )(`str` Convert to a logical value (true/false `bool`() → )


---

**Page 14**

According to Figure 27, to convert a data type to a numeric type you can do it like this:

Example: Write a program that receives the user's age and displays it with a suitable message.

![Figure 27](../images/p020-02.png)

**Figure 27**

Example: Pay attention to this example.

After running, you will see an error, because a number has been directly joined to text, and that is not possible (Figure 28).

![Book image](../images/p020-01.png)

![Figure 28](../images/p020-03.png)

**Figure 28**

To fix this error, you need to convert the numeric data type to the string data type as follows. After running, you will not see an error code (Figure 29).

![Figure 29](../images/p020-04.png)

**Figure 29**

Example: On line 1 of the code opposite, the user's year of birth is received; the `int` function converts it to an integer type and stores it in the `year` variable. On line 2 the difference between the current year and the year of birth is calculated and stored in the `age` variable. On line 3, with the `print` statement, the user's age is displayed with the message "`your` `age` :" (Figure 30).

![Book image](../images/p020-05.png)

![Figure 30](../images/p020-06.png)

**Figure 30**


---

**Page 15**

Example: The value of the `price` variable is an integer. On line 2, the `float` function is used to convert it to a floating-point number (Figure 31).

![Figure 31](../images/p021-01.png)

**Figure 31**

Example: The `input` function receives weight as a numeric value, and its output is a text value that the `float` function converts to a floating-point number and stores in the `weight` variable. On the next line the `print` statement concatenates two strings with the "+" operator (Figure 32).

![Book image](../images/p021-03.png)

![Figure 32](../images/p021-02.png)

**Figure 32**

You can see that on this line the `str` function converts the `weight` variable to a text type again.

Example: Calculating the price of a product after applying 9 percent value-added tax (Figure 33).

![Book image](../images/p021-05.png)

![Figure 33](../images/p021-04.png)

**Figure 33**

### Activity

Get the user's height as a floating-point number and display a message similar to the one below.

```
.Your height: 1.75 meters
```

### Activity

To set up a smart store, carry out the following steps.

Receive the store manager's name from input Receive the year the store started operating Convert the type of the inputs Display a welcome message


---
