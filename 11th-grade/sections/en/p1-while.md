**Page 40**

The `while` loop This loop executes a set of statements as long as the loop condition is `True`, and whenever the loop condition becomes `False`, the loop is no longer executed and the loop's execution ends. This type of loop is usually used when the number of loop repetitions is not known and determined in advance.

![Figure 87](../images/p046-01.png)

**Figure 87**

```
: while condition یا : شرط حلقه while
```

`statements` → loop body statements

Example: A person at the entrance of a dining hall welcomes the guests of a wedding ceremony. They have been told to stand there and, after asking their names, welcome each guest who enters, and no limit has been set for when their work ends. The program below does this with the help of a `while` loop (Figure 88).

![Book image](../images/p046-03.png)

![Figure 88](../images/p046-02.png)

**Figure 88**

Explanation of the program code: In front of the `while` statement, instead of putting a particular condition, for now the logical expression `True` is used. With this, the loop repeats without stopping and no end has been defined for stopping it;

because the condition in front of `while` is always `True` and never becomes `False`.

In the next two lines the guest's name is asked and the welcome message will be printed.

Given that there is no end for the program's execution, to stop the program you must either use the key combination `Ctrl` + `C` or close the window of the running program.

Example: Can the program above be written so that after the groom enters, the welcoming task ends?


---

**Page 41**

Code explanation: As you can see in the output of the code in Figure 89, after the groom's name is entered, the program ends.

![Figure 89](../images/p047-03.png)

**Figure 89**

Inside the loop, after receiving the guest's name, with the help of an `if` condition it is checked whether the entered name equals `damad` or not, and if it equals, with the help of the `break` statement the loop's execution ends and the program's execution is moved to after the `while` loop.

Example: In this hall, besides guests, employees (`Employee`) are also coming and going; now if you do not want employees to be welcomed, you can use a conditional statement and the `continue` statement.

Code explanation: As you can see in the output of the code in Figure 90, after the name `Employee` is entered, the program again receives another name from the user and the employee will not be welcomed. Look carefully at the program output.

![Book image](../images/p047-02.png)

![Figure 90](../images/p047-01.png)

**Figure 90**

When the program reaches the `continue` statement, it abandons executing the rest of the loop statements and moves the program's execution to the beginning of the loop.

Although this program works well, this structure, because of the presence of `True` in front of `while`, is not very suitable for programming, and the loop structure can be changed as in the next example.

Example: The welcoming attendant has been told to continue this work until the groom has not arrived; the code changes as follows.

Note that in this example the condition for continuing the loop is in front of the `while` statement and you do not need to control anything inside the loop.


---

**Page 42**

Code explanation: As you can see in the output of the code in Figure 91, after the groom's name is entered and he is welcomed, the program ends.

![Book image](../images/p048-01.png)

![Figure 91](../images/p048-02.png)

**Figure 91**

In the first line a variable named `name` is created and its value is empty so that the loop condition is initially met.

The meaning of the second line is that as long as the entered name, that is the value of the variable (`name`), is not equal to the word `damad`, the loop body statements continue.

When the user enters the word `damad`, after printing the message, the program returns to the beginning of the loop; but this time the loop condition is `False` and the loop's execution ends. Here, compared with the previous program, the code has become better and more logical.

Example: The welcoming attendant has been told to stand there and, after asking their names, welcome each guest who enters, and as soon as the groom enters the welcoming task ends; but there is no longer a need to welcome the groom. The code above will change a little.

Code explanation: In Figure 92, in the first line, instead of placing an empty string in the variable `name`, with the help of the `input` statement a real name is taken from the user. In this way, if in the first line of the program the name `damad` is entered, the loop condition becomes `False` and the loop body statements will no longer be executed and the program ends.

![Book image](../images/p048-03.png)

![Figure 92](../images/p048-04.png)

**Figure 92**

Inside the loop first the welcome is printed and in the next line another name will be received so that in the next round this name is checked in the loop condition.

### Note

The examples above all help the programmer learn how to use the `while` loop in different situations. By rewriting the code and thinking about the process of each of the programs above, the programmer learns the material more precisely. For better learning, pay attention to the examples on the next page.


---

**Page 43**

Example: Write a program that receives an integer from the user and prints the square of that number; this continues as long as the user enters a number greater than zero (Figure 93).

![Book image](../images/p049-01.png)

![Figure 93](../images/p049-02.png)

**Figure 93**

Code explanation: In the first line an integer is received from the user and placed in the variable `number`.

The meaning of the `while` condition: that is, as long as the value of the variable `number` is greater than zero, the loop statements will be repeated.

Inside the loop first, with an appropriate message, the number taken and its square (that is, to the power of two) will be printed, and then another number is taken from the user.

If in the first line of the program a value less than or equal to zero is entered, the loop condition becomes `False` and the loop body statements will no longer be executed and the program ends. Note that in this example, the square of the number zero or a negative number is not printed.

### Activity

Change the program above so that in addition to the square of the number, the cube (`Cube`) of the number (that is, the number to the power of 3) is also printed.

Example: Write a program that takes the names of several foods from the user and adds (`append`) them to an empty list.

This continues as long as the user enters the word `exit`. After the loop ends, the contents of the list will be printed all at once (Figure 94).

![Book image](../images/p049-03.png)

![Figure 94](../images/p049-04.png)

**Figure 94**


---

**Page 44**

Code explanation: In the first line, an empty list is created.

As in the previous examples, first take the name of a food and store it in the variable `food`.

The meaning of the `while` condition: that is, as long as the value of the variable `food` is not equal to the string `"exit"`, the loop statements will be repeated.

Inside the loop first the name of the food taken is added to the end of the list with the help of the `append` method, and then the name of another food is taken from the user.

In the last line and outside the loop body, the complete contents of the food list are printed.

![Book image](../images/p050-02.png)

Note that the last line must not be moved forward by one `tab` and must be written exactly under the `while` column.

![Book image](../images/p050-01.png)

Example: Pay attention to the code below. This code prints the numbers one through five one under another with the help of a `for` loop (Figure 95).

**Figure 95**

Now if you want to do the same thing with the help of a `while` loop, its code can be like the code in Figure 96.

Code explanation: In the first line, the variable `i` is assigned the default value one.

As in the previous examples, first take the name of a food and store it in the variable `food`.

![Book image](../images/p050-04.png)

![Book image](../images/p050-03.png)

The meaning of the `while` condition: that is, as long as the value of the variable `i` is less than

6, the loop statements will be repeated. Inside the loop first the value of the variable `i` has been printed. In the last line and inside the loop, one has been added to the variable.

**Figure 96**

As you can see, the `while` loop structure for loops with a known number of repetitions is more complex and requires more care. Therefore programmers are advised, before starting to code, to think about, according to the given problem, which type of loop is better to use.

Important points you learn from the `while` loop:

In this type of loop you do not know in advance how many repetitions are needed; that is, the loop continues as long as the condition is met.

Repetition depends on a condition, and the condition can be a comparison, user input, or the state of the program.

The end of the work is determined by the user or a specific event. So the loop continues until the end condition is reached.

To control the loop and prevent infinite execution, before the loop starts, the loop variable must be initialized.


---

**Page 45**

Inside the loop you can use `break` to end the loop's execution.

Inside the loop you can use `continue` to return to the beginning of the loop and run it again.

The `break` and `continue` statements must be used together with an `if` condition inside loops.

To implement loops with a known count you can also use `while` loops; but this is not recommended, because writing such programs with a `for` loop is simpler and more logical.

### Activity

In the previous example and at the end of the program above, with the help of a `for` loop print each of the foods in the list one under another.

### Activity

Write a program so that the user can repeatedly order food, until they enter `"done"`.

Each time a new food is taken from the user, the message `".Your` `order` `for` `<food>` `has` `been` `added"` should be displayed and the new food should be added (`append`) to the food order list. When the user enters `"done"`, the program should display all the orders.


---
