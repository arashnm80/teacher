**Page 33**

In the Python programming language, there are two main structures for implementing repetition loops:

1 The `for` loop

2 The `while` loop

The `for` loop: is used to repeat the execution of statements over a sequence (such as a list, string, tuple, set, and dictionary) and is usually used when the number of repetitions is known or can be determined in advance.

The overall structure of the `for` loop in Python is as follows:

```
:for variable in sequence
statements
```

In this structure:

`variable` is a variable that, in each repetition, receives the value of one of the elements of the sequence.

The variable name can be chosen freely; for example (`i`, `count`, `num`, `student`…) `sequence` is a sequence such as a list, string, tuple, set, or dictionary.

`statements` are the set of statements in the loop body that are executed on each repetition. These statements are called the loop block and must have one `tab` of indentation.

Traversing lists Example 1: The code below prints the elements of a list that includes three colors (`red`, `blue`, `green`) (Figure 73).

![Figure 73](../images/p039-01.png)

**Figure 73**

Code explanation: In the first line, a list containing the names of three colors as strings is defined.

In the second line, the `for` statement traverses the list elements in order and places each element in the variable `item`.

Example 2: Displaying a shopping cart. In this program, first a list named `shopping_cart` is created and the purchased items are stored in it. Then the elements in the list are printed using a `for` loop.

Run the program and observe the result (Figure 74).

![Book image](../images/p039-02.png)

![Figure 74](../images/p039-03.png)

**Figure 74**


---

**Page 34**

Code explanation: In the first line, a list containing the names of the purchased items as strings is defined.

The second line prints an appropriate message before entering the loop.

In the third line, the `for` statement traverses the list elements in order and places each element in the variable `item`.

In the final line, a message containing the name of each list element is printed.

![Book image](../images/p040-02.png)

Traversing strings Example: printing the letters of the word `python` (Figure 75)

![Figure 75](../images/p040-01.png)

**Figure 75**

Code explanation: On each execution of the loop, one of the letters of the string `python` is placed in the variable `ch` and that same value is printed inside the loop.

Examples of using the `for` loop Example 1: The program below is written to count the number of elements in a list using a `for` loop (Figure 76).

![Figure 76](../images/p040-03.png)

**Figure 76**

Code explanation: In the first line, a list containing the names of several fruits as strings is defined.

In the second line, the variable `count` is created with the initial value zero.

In the third line, the `for` loop traverses the list elements in order and places each element in the variable `fruit`.

In the fourth line, for each execution of the loop, one is added to the variable `count`. The two statements below are equivalent.

```
count + = 1
count = count + 1
```

In the final line, the final value of `count` is printed. Note that this line is outside the loop.


---

**Page 35**

### Activity

In Python there is a built-in function for doing the code on the previous page; research it.

Example 2: If the goal is to count the number of a specific element (for example, the number of `apple`) inside the loop, you can change the program as follows using the conditional statement `if` (Figure 77).

![Figure 77](../images/p041-01.png)

**Figure 77**

Code explanation: In the fourth line, the `if` statement checks whether the value of `fruit` equals the value `apple` or not.

If the above condition is met, one is added to the variable `count`.

### Activity

Lists have a method for doing the code above; research it.

Using the `range`() function: So far, the `for` loop has been used to traverse the elements in lists and strings.

In some cases, a statement needs to be repeated a specific number of times, without a list of values being available in advance.

In such situations, the `range` function is used.

The `range`() function produces a sequence of numbers that starts from the value `start` and, with steps specified in `step`, continues up to but not including the value `stop`.

`Start:` (optional and default)

```
:)start, stop, step( for counter in range
```

`Stop:` (required) and that value itself is not included.

Loop body statements

`Step:` (optional) its default is one.

**Figure 78**


---

**Page 36**

First form: In the simplest form, the `range`() function receives only one number, written as `range`(`stop`). Consider the example below:

![Book image](../images/p042-04.png)

Example: A loop to print the numbers 0 through 4 (Figure 79).

![Figure 79](../images/p042-03.png)

**Figure 79**

Code explanation: The start value (`start`) is zero by default, and the step (`step`) also has the default value one. The end value (`stop`) is considered the number 5, and this number itself is not produced in the output.

The function `range`(5) produces a sequence of numbers from 0 to 4. The `for` loop runs 5 times. The variable `i` receives the value of one of these numbers in each repetition. In the second line, on each run the value of the variable `i` is printed.

Second form: Using the function as `range`(`start`, `stop`).

Example: A loop to print the numbers from 1 to 6 (Figure 80).

![Book image](../images/p042-06.png)

![Figure 80](../images/p042-05.png)

**Figure 80**

Code explanation: The start value (`start`) inside the `range` statement is one.

The loop end value (`stop`) is the number 7; but the number 7 itself will not be included. The `range` function produces the sequence of numbers from 1 to 6.

The step (`step`) is also one by default.

In the third form, the `range` function receives three numbers, written as `range`(`start`, `stop`, `step`). Consider the example below:

Example: A loop to print even numbers less than 10 (Figure 81).

![Book image](../images/p042-02.png)

![Figure 81](../images/p042-01.png)

**Figure 81**


---

**Page 37**

Code explanation: The start value (`start`) in the `range` statement is equal to zero.

The end value (`stop`) is considered the number 10, but this number itself is not produced in the output. The step value (`step`) is equal to 2.

The `range` function produces a sequence of even numbers from 0 to 8.

### Activity

Change the previous program so that it prints the sequence of even numbers from large to small. For this purpose, the value of `step` must become negative, and the start (`start`) and end (`stop`) values must also be changed accordingly.

### Activity

Write a program that receives the waiting time to get food as a number (in minutes) from the user and displays a countdown.

At each step, the message below is printed:

```
Time remaining: X minutes
```

in which, instead of `X`, the remaining time value is displayed.

After the count reaches zero, the message below is displayed.

```
!Your food is ready
```

### Activity

Write a program that receives the heights of 5 people from input and calculates and displays their average height.

Using the underscore character (_ ) in variable names is allowed; therefore you can also use it alone as a variable name.

![Book image](../images/p043-01.png)

Observe the code in Figure 82.

**Figure 82**

In this example, the loop counter variable is not used in the loop body; therefore you can use the underscore character (_) instead. Using _ shows that the value of the variable in question will not be used later in the program.

### Try this

Investigate what advantages using _ instead of using a variable name has.


---

**Page 38**

Introducing control statements (`break` and `continue`) in loops In Python, the control statements `break` and `continue` are used to control the flow of loop execution.

`continue:` is used to skip a particular part of the loop and go to the next repetition.

`break:` completely stops the loop's execution and exits it.

Example: Write and run the program below. In this program, the names of all foods in a list are each printed on one line. (Figure 83)

![Book image](../images/p044-03.png)

![Figure 83](../images/p044-02.png)

**Figure 83**

Now if you want, when printing, the name of a particular food (for example, `soup`) not to be displayed, you can use the `continue` statement inside the loop. Write the code below carefully and run it, and when writing the program pay attention to indentation (`Indentation`) (Figure 84).

![Figure 84](../images/p044-01.png)

**Figure 84**

Code explanation: In the line `"soup"` == `if` `item`, it is checked whether the value of the variable `item` equals the value `soup` or not.

If the `if` condition is met, the `continue` statement is executed and causes the loop to immediately go to the next element, which is `"ash"`. For that reason, the name `soup` is not printed in the program output.

In general, using the `continue` statement, the loop skips executing part of the code inside the loop for particular repetitions and goes directly to the beginning of the next repetition.


---

**Page 39**

Now if you want, when printing, upon reaching the name of a particular food (for example, `soup`), a specific message to be printed and the loop's execution to end, you can use the `break` statement inside the loop. Write the code below and run it. When writing the program pay attention to indentation (`Indentation`) (Figure 85).

![Book image](../images/p045-01.png)

![Figure 85](../images/p045-02.png)

**Figure 85**

Code explanation: In the third line, it is checked whether the value of the variable `item` equals the value `soup` or not.

If the `if` condition is met, first the message "Soup is not a food!" is printed and then the `break` statement is executed and control of the program's execution is moved to after the loop. In this case, the loop's execution is completely stopped and later repetitions will not be performed (Figure 86).

Now write and run the two programs below.

![Book image](../images/p045-04.png)

![Book image](../images/p045-03.png)

![Book image](../images/p045-05.png)

![Figure 86](../images/p045-06.png)

**Figure 86**

### Try this

Given the output of the programs above, state the use of the words `break` and `continue` for each of the programs.


---
