**Page 213**

Loop statements in programming languages are used to repeat the execution of a section of a program. Repetition loops reduce program size, improve code readability, optimize the program algorithm, and increase program efficiency.

There are different types of repetition loops. In JavaScript, these loops include `for`, `while`, `do` `while`, `for`…`of`, and `for`…`in`.

The `for` loop is used when the number of times a task should be repeated is known. The general form of the `for` loop is as follows:

```
    10|{ )Initialization; Condition; Increment/Decrement( for
```

The code that should be repeated

}

The `for` loop needs a counter to count how many times the loop runs. The loop counter is a variable that has an initial value and a final value. The expression `Initiliazation` refers to initializing the loop counter. In the `Condition` part, the loop’s repetition condition is checked. To exit the loop, the loop condition must be violated.

![Book image](../images/p219-01.png)

For this purpose, the loop counter must be increased or decreased on each repetition of the loop so that the counter’s value passes the final value. The expressions `Increment` and `Decrement` mean increasing and decreasing the counter’s value. If braces are not used to define the loop block’s scope, only the first statement is considered part of the loop.

**Figure 11**

Using the `for` loop

### Workshop

![Book image](../images/p219-02.png)

Create a new file named `workshop7.html` and write the script shown opposite to print the numbers 0 through 4.

### Note

If the loop counter is defined with the keyword `let`, access to the counter variable’s value will be possible only inside the `for` block.

Based on these explanations, if after the closing brace the statement `console.log`(`i`) is written, an error message is issued.


---

**Page 214**

### Learn more

**Table 21**

```
حلقه while و do while
```

`while`

These loops repeat a set of statements

```
do while
```

until a condition is violated.

{ `do`

```
{(condition) while
```

Their general form

The code that should be executed repeatedly

The code that should be repeated

```
;(condition) while }
```

}

is as shown opposite:

In the `while` loop, first the condition inside the parentheses is checked; if the condition is true, the statements inside the loop are executed. If the loop condition is false from the start, the loop body is not executed at all.

The body of the `do` `while` loop is executed once, then the loop condition is checked. If the condition is not true, the loop is exited.

If the loop condition is never violated, the loop statements repeat continuously. This situation is known as an infinite loop (`Infinite` `loop`). An infinite loop can consume system resources (such as `CPU` and `RAM`) excessively, which will disrupt the browser’s performance.

Using the `while` and `do` `while` loops: In the file `workshop7.html`, write the script below to print the elements of the `colors` array using a `while` loop.

![Book image](../images/p220-02.png)

![Book image](../images/p220-01.png)

Save the file and display its output in the browser.

Calculate the sum of the elements of the `numbers` array using a `do` `while` loop and display the result in the console.

![Book image](../images/p220-03.png)

![Book image](../images/p220-04.png)


---

**Page 215**

The `for`…`of` loop: This loop is used to iterate over the elements of an iterable collection such as an array, a string, a set, and so on.

The `for`…`of` loop provides access to the values of array elements.

The `for` … `in` loop: This loop is used to iterate over the keys of objects (`Objects`) and the indices of arrays.

The general form of the `for` … `of` and `for` … `in` structures is as follows:

**Table 22**

```
for … in
for … of
{ (const key in object) for
{ (const element of iterable) for
```

...…

..…

}

}

The variable `element` refers to the elements of an array, a set, or the characters of a string, and `iterable` refers to an iterable object.

The variable `key` refers to the keys of object elements and the indices of array elements.

Working with the `for` … `of` and `for` … `in` loop structures

### Workshop

1 In the file `workshop7.html`, write the script below and observe the result in the browser console.

![Book image](../images/p221-02.png)

![Book image](../images/p221-01.png)

The variable `name` refers to the elements of the `firstName` array; on each execution of the loop, the variable `name` refers to a new element of the array.

### Try this

In the expression ( `const` `name` `of` `firstNames`( `for`, why is the keyword `const` used?

2 To examine how the `for` … `in` loop works when iterating over object elements, write the script below and check the result in the browser console.

![Book image](../images/p221-03.png)


---

**Page 216**

In the code above, the variable `languages` is an object containing the names of languages. In this object, abbreviations (such as `en`, `fa`, and so on) are specified as element keys, and the corresponding Persian phrase (such as English, Persian, and so on) is specified as the element value.

In this code, the `for`…`in` loop iterates over the elements of the `languages` object one by one and places the key of each element in the variable `lang`. Then the `console.log`() statement displays the key name and its corresponding value in the console.

The `break` statement: This statement is used to exit a loop or a `Switch` structure. If the `break` statement is used inside a loop, execution of all statements after it stops and the loop is exited.

### Note

If this statement is used inside a `switch` structure, the later `Case`s will not be checked and program control moves to after the closing brace.

Using the `Break` statement

### Workshop

Write a script that displays the two-digit numbers of the array below in the browser console.

```
;]let data = [10,21,37,43,76,83,98,356,200,353,444,1000
```

To do this, at the end of the file `workshop7.html`, enter the script below. Then save the file and display its output in the console.

![Book image](../images/p222-02.png)

![Book image](../images/p222-01.png)

```
دستور continue
```

Using the `continue` statement in a loop causes the current execution of the loop to stop and the next iteration of the loop to run. That means after the `continue` statement runs, program control moves to the beginning of the loop and the next iteration of the loop (if possible) is executed.


---

**Page 217**

Using the `Continue` statement

### Workshop

Display the even numbers between 20 and 35 next to each other with a hyphen (-) as the separator.

At the end of the script in the file `workshop7.html`, write the script below and check the result in the console.

![Book image](../images/p223-01.png)

![Book image](../images/p223-02.png)

To remove the final hyphen (-), write the statement below before the `console.log` statement:

```
;)0, -3(evenNumbers = evenNumbers.slice
```

### Learn more

Nested loops: The loops introduced so far make it possible to iterate over one-dimensional elements. To iterate over elements such as a two-dimensional array, you need to use nested loops. This type of loop is created when another loop is placed inside a loop. In a nested loop, the inner loop repeats as many times as the outer loop runs.

### Learn more

Using a nested loop

١ Display a 5×5 multiplication table using a nested loop.

٢ Write the script below at the end of the script in the file `workshop7.html` and check the result in the console.

![Book image](../images/p223-03.png)

![Book image](../images/p223-04.png)

The `\t` symbol means `tab` and is used to set the spacing between values.


---

**Page 218**

### Activity

Instead of the `console.log` statement, use the `document.write` statement to display the values on the browser page.

Iterating over a two-dimensional array using a `for` loop

### Workshop

Open the file `product.html` and add the JavaScript code below to it.

![Book image](../images/p224-02.png)

![Book image](../images/p224-01.png)

```
توابع(Functions)
```

In programming languages, blocks of code that perform a specific task are called functions.

A programmer can group a set of instructions in the form of a function and then use it as a separate unit. These separate units can be used many times.

Using functions in programming not only increases development speed but also increases the readability and maintainability of the code. The set of statements written to create a function can be called under a specific name. A function can receive values as input and, after executing the statements inside the function, return a value as output.

In JavaScript, the following general form is used to create a function:

![Book image](../images/p224-03.png)

![Figure 12](../images/p224-04.png)

**Figure 12**
