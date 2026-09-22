**Page 62**

### Function (Function)

A function is a block or piece of code that you define once and can call many times in several places in the program.

![Figure 129](../images/p068-01.png)

**Figure 129**

Advantages of using a function:

By defining a function, the programmer writes the desired code only once and then, at any point in the program or even in other projects where it is needed, calls and uses it.

Dividing code into small, specific functions greatly increases understanding of the code.

Finding and fixing bugs and making changes in the code become much simpler.

Organizing the code logically and neatly, and the overall structure of the program, becomes easier.

Defining a function: A function is defined using the keyword `def`, followed by the function name and parentheses.

The general form of defining a function with an input parameter is as follows:

![Book image](../images/p068-02.png)

`def` function name (function parameters):

return value

statement or statements of the function body

function

inputs

`return` value or values

**Figure 130**


---

**Page 63**

Example: In this program a function named `show_store_name` is defined and a `print` (`"Digital` `Online` `Store"`) statement is written in it (Figure 131).

![Figure 131](../images/p069-01.png)

**Figure 131**

Example: In this program also a function named `greet` is defined and the statement `print`(`"Hello`! ") is written in it (Figure 132).

![Figure 132](../images/p069-02.png)

**Figure 132**

Example: In this program the function `greet`() is defined without a parameter, so when calling it there is no need to send an argument (Figure 133).

![Book image](../images/p069-03.png)

Output

**Figure 133**

Example: In this program also the function is defined without a parameter. When calling it there is no need to send an argument (Figure 134).

![Book image](../images/p069-04.png)

![Figure 134](../images/p069-05.png)

**Figure 134**


---

**Page 64**

Parameter and argument (`Parameters` & `Arguments`) What is a parameter? A function can receive inputs. The inputs of a function at the time the function is defined are called a parameter (`parameter`).

What is an argument? The inputs of a function that are given to it when the function is called.

After definition, the function must be called to run. If you only define the function but it is not called, nothing happens. It is as if it was never defined.

To call a function, write its name and send it as many arguments as there are parameters (this is called passing). You can call a function many times.

The way to call a function is as follows:

function name (function arguments)

Example: In the example in Figure 135, the function `show_product`(`name`, `price`) is defined with two parameters `name` , `price`. When calling it, two values must also be sent as arguments.

![Book image](../images/p070-01.png)

Output

![Figure 135](../images/p070-02.png)

**Figure 135**

Example: In the example in Figure 136, the function `print_age`(`age`) has one parameter named `age`. When calling it, one argument should also be sent to it. As you can see, the function `print_age`(`age`) is called twice with two different arguments.

![Book image](../images/p070-03.png)

Output

![Figure 136](../images/p070-04.png)

**Figure 136**


---

**Page 65**

### Note

The order, number, and type of parameters (at the time the function is defined) must match the order, number, and type of arguments (at the time the function is called).

If the order and type of sending arguments are not observed, incorrect output is produced. It does not give an error at run time;

but the program logic is wrong.

The solution is to use keyword arguments (`keyword` `arguments`), or named arguments; that is, when calling the function, you can write the parameter name together with the assignment operator.

Example: Look carefully at the code in Figure 137. Check the outputs. Calling without observing the order of the arguments has caused the price to be printed first and then the product name, and this is incorrect logic.

![Book image](../images/p071-01.png)

Output

Calling without observing order Calling with observing order

![Figure 137](../images/p071-02.png)

**Figure 137**

Example: In the example in Figure 138, to prevent incorrect output when sending arguments out of order, keyword arguments are used. Write the program and compare the result with the previous example.

![Figure 138](../images/p071-03.png)

**Figure 138**

### Note

When arguments are given to the function without the parameter name, the order in which they are sent is important, because each argument is assigned in turn to the function’s parameters. These arguments are called positional arguments

```
(positional arguments) گفته می‌شود.
```

### Activity

Write a function named `square` that takes a number and prints its square.


---

**Page 66**

### Note

Write a function that receives two numbers as parameters and shows their sum.

### Note

Write a function that receives the names of 3 users from input as parameters and prints them.

Example: The number of arguments sent to a function must equal the number of its parameters at the time the function is defined. Otherwise, an error message is displayed at run time (Figure 139).

![Book image](../images/p072-01.png)

The number of arguments sent is less than the number of function parameters

![Book image](../images/p072-02.png)

The error message displayed after running the program

**Figure 139**

### Note

You can set a default value for a parameter. If an argument is not given, the default value is used.

Example: In the first line of the code in Figure 140, the function is defined with one parameter. On line 4, when calling, its argument is not sent, so its default value `"Tehran"` is used. On line 5 the function is called with an argument. Write the program and check the result. Change the default value and run the program.

![Book image](../images/p072-03.png)

![Figure 140](../images/p072-04.png)

**Figure 140**


---

**Page 67**

Example: In this example the function is defined with two parameters that have default values. Each time it is called, the arguments are sent in different ways. Write the program, check the result. Change the default value and run the program again (Figure 141).

![Book image](../images/p073-01.png)

![Figure 141](../images/p073-02.png)

**Figure 141**

Function return value (`Return` `Value`) A function can calculate a value and return it to the program so that it can be used later; that is called a return value (`Return` `Value`). Without `return`, the function does its own work (for example, it prints) but returns no value outward, and if you want to store the function’s result in a variable, its value becomes `None` (Figure 142).

![Figure 142](../images/p073-03.png)

**Figure 142**

Example: By running the program in Figure 143, the value 8 is displayed. But the number 8 is not stored and also cannot be used elsewhere.

![Book image](../images/p073-04.png)

Now change the program using `return` and observe the result.

This time: the function returns the number 8 and the return value is stored in the variable `result` and can be used again.

**Figure 143**

Example: Without using `return`, only (`price` * `count`) is calculated and no value is returned to the program, so by calling the function `total_` `price`(200000, 2) in the variable `x` the value `None` is stored and by running the program the value `None` is also printed

![Book image](../images/p073-05.png)

(Figure 144).

**Figure 144**


---

**Page 68**

Example: Using `return`, the calculated value is returned to the program and you can store it in the variable `x`, and by printing the variable `x` the stored value is displayed (Figure 145).

![Figure 145](../images/p074-01.png)

**Figure 145**

### Activity

Build a function named `avg_numbers` that receives three numbers and returns their average.

Example: Write a function that calculates the total purchase price and, if the purchase quantity is more than 5, gives a 10% discount.

Inside the function, `if` is used so that a condition is checked.

If the condition (`count` > 5) is true, the value with the discount is returned.

If the condition is not true, the value without the discount is returned.

`return` is used so that the calculated result returns outside the function and you can print or store it (Figure 146).

![Figure 146](../images/p074-02.png)

**Figure 146**

Using a loop inside a function:

Using a loop inside a function is so that you can run specific statements several times automatically, for as long as the set condition is true or for a specific number of times. This reduces code repetition, increases readability, and optimizes the function’s performance.

![Book image](../images/p074-03.png)

Example: In this example, the defined function prints the natural numbers smaller than 6. Run the program and observe the result (Figure 147).

**Figure 147**


---

**Page 69**

Example: First, the defined function has a parameter named `names`, which is expected to receive arguments that are a list of names (Figure 148).

With a `for` loop it receives the list elements one by one and assigns them to the variable `name`.

The `print` statement also runs inside the loop and prints the names separately.

Before calling the function, on the first line of the program, the list `students` that includes the students’ names is created.

Then the function is called with the argument `students`. The loop inside the function prints the names inside the list one by one.

![Figure 148](../images/p075-01.png)

**Figure 148**

### Activity

![Book image](../images/p075-04.png)

The written function calculates the sum of all numbers in a list. Write the program and run it. With guidance from your teacher, explain the lines of code written in it. Change the function so that the user enters the list elements from the keyboard.

### Activity

![Book image](../images/p075-02.png)

The written function that calculates and displays the length of the user’s input string. Run the program and examine it, and also with guidance from your teacher explain the code of the program opposite.

### Activity

![Book image](../images/p075-03.png)

The code opposite calculates and displays the largest value among the numbers in a list. Run the code and explain its lines.


---
