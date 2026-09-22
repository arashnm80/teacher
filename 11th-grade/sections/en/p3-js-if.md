**Page 211**

The word `Condition` means the condition, and the word `statement` refers to the statement or statements that run when the condition is met. A condition being met means that the value of the `Condition` expression equals `True`. The word `else` means “otherwise.” The content of `else` runs when the `if` condition is not met—that is, when the value of the `condition` expression equals `False`.

Working with `if` conditional structures

### Workshop

Using an `if` conditional structure, check whether the number `n` is even or odd.

For this purpose, create a new file named `workshop6.html` and write the following script in it:

Save the file and view the result in the browser console. In this script, the remainder of dividing the number `n` by 2 is stored in the variable `r`. If the remainder is zero (that is, `n` is divisible by 2), the phrase `"Even` `number"` appears on the page; otherwise the phrase `"Odd` `number"` appears.

![Book image](../images/p217-03.png)

The word `Even` means even and the word `Odd` means odd.

The script that detects whether a number is even or odd can also be written with an `if-else` structure. Change the previous script according to the figure below and check the result in the browser console.

![Book image](../images/p217-02.png)

![Book image](../images/p217-01.png)

![Book image](../images/p217-04.png)

The `else-if` structure: Makes it possible to check several conditions one after another. In this step, a student’s rank is determined based on the score earned. At the end of the previous script, write the code on the right.

In this script, the variable `score` with the value 70 is defined to hold the student’s score. First the condition `score>=90` and then the condition `score>=80` are checked. Given that

**Figure 10**


---

**Page 212**

the value of both conditions is false, the `console.log`() statement on lines 3 and 5 is not executed. Then the condition `score>=70` is checked. Because the condition is met, statement number 7 runs and the phrase `Grade:` `C` is printed on the page. After statement 7 runs, the later conditions are not checked and program control moves to line 13.

### Learn more

The `Switch` structure The `switch` structure is used to choose among several blocks of code based on the value of a variable. If the problem conditions are limited only to comparing one variable with specific values, you can use a `switch` structure instead of many `else-if`s.

Using the `switch` conditional structure

### Workshop

![Book image](../images/p218-01.png)

Write a script that receives a student’s rank from the variable `grade` and, based on the rank value, displays an appropriate message for the user.

For this purpose, place the existing script in the `workshop6.html` file inside comment marks and then write the code on the right to check the rank.

In this example, the `switch` conditional structure checks the value of the variable `grade` with different `case`s; as soon as the value next to a `case` matches the value of the variable `grade`, the statement after the : mark runs, and then exiting the `switch` structure is done with the `break` statement. If the value of the variable `grade` does not match any of the values written next to the `case`s, the statement for the `default` case runs.

### Note

If a `case` condition is met but there is no `break` statement in it, the next `case` is also checked by the program.

### Activity

In `case` `A`, remove the `break` statement and check the program output in the browser. Then remove the `break` statement from the later `case`s and analyze the result.


---
