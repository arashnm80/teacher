<!-- page 213 -->

### Loop statements

In programming languages, loop statements are used to repeat the running of a part of the program. Loops reduce the size of the program, improve the readability of the code, optimise the algorithm of the program and increase the efficiency of the program. Loops have different types. In JavaScript these loops include for, while, do while, for…of and for…in.

### The for loop

When the number of repeats of a job is known, the for loop is used. The general form of the for loop is as follows:

```
for (Initialization; Condition; Increment/Decrement) {
```

The code that must be repeated

```
}
```

The for loop needs a counter to count the number of times the loop runs. The loop counter is a variable that has a starting and an ending value. The phrase Initialization points to giving the loop counter its initial value. In the Condition part, the repeat condition of the loop is checked. To leave the loop, the loop condition must be violated. For this purpose the loop counter must be increased or decreased on every repeat of the loop so that the value of the counter passes the ending value. The phrases Increment and Decrement mean increasing and decreasing the value of the counter. If curly braces are not used to mark the range of the loop block, only the first statement counts as part of the loop.

![Figure 11](../images/p219-01.png)
*Figure 11*

> **Workshop**
>
> **Using the for loop**
>
> ![Book image](../images/p219-02.png)
>
> Create a new file named `workshop7.html` and write the script opposite to print the numbers 0 to 4.
>
> > **Note**
> >
> > If the loop counter is defined with the keyword let, the value of the counter variable can be reached only inside the for block.
>
> Considering these explanations, if the statement `console.log(i)` is written after the closing brace, an error message is given.

<!-- page 214 -->

> **Learn more**
>
> *Table 21*
>
> | do while | `while` |
> | --- | --- |
> | `do {`<br>`} while (condition);` | `while (condition){`<br>The code that must be repeated<br>`}` |
>
> **The while and do while loops** These loops repeat a set of statements until a condition is violated. The general form of these loops, with the code that must be repeated, is as opposite:
>
> In the while loop, first the condition inside the parentheses is checked; if the condition holds, the statements inside the loop run; if the loop condition is false from the start, the content of the loop does not run at all.
>
> The content of the do while loop runs once, then the loop condition is checked. If the condition does not hold, the loop is left.
>
> If the loop condition is never violated, the statements of the loop are repeated continuously. This state is known as an infinite loop. An infinite loop can use up the system's resources (such as CPU and RAM) without limit, which disturbs the browser's performance.
>
> **Using the while and do while loops**
>
> In the file `workshop7.html` write the following script to print the elements of the array colors using the while loop.
>
> ![Book image](../images/p220-01.png)
>
> ![Book image](../images/p220-02.png)
>
> Save the file and show its output in the browser.
>
> Calculate the sum of the elements of the array numbers with a do while loop and show the result in the console.
>
> ![Book image](../images/p220-03.png)
>
> ![Book image](../images/p220-04.png)

<!-- page 215 -->

**The for…of loop**: this loop is used to go over the elements of an iterable collection such as an array, a string, a set and so on. The for…of loop makes it possible to reach the values of the elements of an array.

**The for … in loop**: this loop is used to go over the keys of objects and the indexes of arrays. The general form of the for … of and for … in structures is as follows:

*Table 22*

| `for … in` | `for … of` |
| --- | --- |
| `for (const key in object) {`<br>…...<br>`}` | `for (const element of iterable) {`<br>…..<br>`}` |

The variable element points to the elements of the array, the set or the characters of a string, and iterable points to the iterable object. The variable key points to the key of the elements of the object and the index of the elements of the array.

> **Workshop**
>
> **Working with the for … of and for … in loop structures**
>
> 1. In the file `workshop7.html` write the following script and see the result in the browser console.
>
> ![Book image](../images/p221-01.png)
>
> ![Book image](../images/p221-02.png)
>
> The variable name points to the elements of the array firstName; each time the loop runs, the variable name points to a new element of the array.
>
> > **Curiosity**
> >
> > In the expression `for (const name of firstNames)`, why is the keyword const used?
>
> 2. To check how the for … in loop works in going over the elements of objects, write the following script and check the result in the browser console.
>
> ![Book image](../images/p221-03.png)
>
> ![Book image](../images/p221-04.png)

<!-- page 216 -->

> **Workshop (continued)**
>
> In the code above, the variable languages is an object containing the names of languages. In this object the abbreviations (such as en, fa and so on) are given as the keys of the elements and the matching phrases (such as English, Persian and so on) as the values of the elements.
>
> In this code, the for…in loop goes over the elements of the object languages one by one and puts the key of each element in the variable lang. Then the statement `console.log()` shows the name of the key and its matching value in the console.

### The break statement

This statement is used to leave a loop or a Switch structure. If the break statement is used inside a loop, the running of all the statements after it stops and the loop is left.

> **Note**
>
> If this statement is used inside a switch structure, the next cases will not be checked and the control of the program moves to after the closing brace.

> **Workshop**
>
> **Using the Break statement**
>
> Write a script that shows the two-digit numbers of the following array in the browser console.
>
> ```
> let data = [10,21,37,43,76,83,98,356,200,353,444,1000];
> ```
>
> For this, at the end of the file `workshop7.html`, enter the following script. Then save the file and show its output in the console.
>
> ![Book image](../images/p222-02.png)
>
> ![Book image](../images/p222-01.png)

### The continue statement

Using the continue statement in a loop makes the current run of the loop stop and the next round of the loop run. This means that after the continue statement runs, the control of the program moves to the start of the loop and the next round of the loop is run (if possible).

<!-- page 217 -->

> **Workshop**
>
> **Using the Continue statement**
>
> Show the even numbers between 20 and 35 side by side with the dash (-) as the separator.
>
> At the end of the script of the file `workshop7.html`, write the following script and check the result in the console.
>
> ![Book image](../images/p223-01.png)
>
> ![Book image](../images/p223-02.png)
>
> To remove the last dash (-), write the following statement before the `console.log` statement:
>
> ```
> evenNumbers = evenNumbers.slice(0, -3);
> ```

> **Learn more**
>
> **Nested loops**
>
> The loops introduced so far make it possible to go over one-dimensional elements. To go over elements such as a two-dimensional array, nested loops must be used. This kind of loop is created when another loop is placed inside a loop. In a nested loop, the inner loop is repeated as many times as the outer loop runs.

> **Learn more**
>
> **Using a nested loop**
>
> 1- Show the 5\*5 multiplication table using a nested loop.
>
> 2- Write the following script at the end of the script of the file `workshop7.html` and check the result in the console.
>
> ![Book image](../images/p223-03.png)
>
> ![Book image](../images/p223-04.png)
>
> The sign \\t means tab and is used to adjust the space between the values used.

<!-- page 218 -->

> **Activity**
>
> Instead of the `console.log` statement, use the `document.write` statement to show the values in the browser page.

> **Workshop**
>
> **Going over a two-dimensional array with the for loop**
>
> Open the file `product.html` and add the following JavaScript code to it.
>
> ![Book image](../images/p224-02.png)
>
> ![Book image](../images/p224-01.png)

**Functions**: in programming languages, blocks of code that do one specific job are called functions. The programmer can group a set of instructions in the form of a function and then use it as a separate unit. These separate units can be used many times. Using functions in programming not only increases the speed of development, but also increases the readability and maintainability of the code. The set of statements written to create a function can be called under a specific name. A function can receive values as input and, after the statements inside the function run, return a value as output.

In JavaScript the following general form is used to create a function:

![Figure 12](../images/p224-03.png)
*Figure 12*
