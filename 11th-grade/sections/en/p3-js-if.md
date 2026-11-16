<!-- page 211 -->

The word Condition means the condition and the word statement points to the statement or statements that run when the condition holds. The condition holding means that the value of the Condition expression is True. The word else means "otherwise". The content of else runs when the condition of the if does not hold, that is, the value of the condition expression is False.

> **Workshop**
>
> **Working with the if conditional structures**
>
> With the **if** conditional structure, check whether the number n is even or odd.
>
> For this purpose create a new file named `workshop6.html` and write the following script in it: save the file and see the result in the browser console. In this script, the remainder of dividing the number n by 2 is stored in the variable r. If the value of the remainder is zero (that is, n is divisible by 2), the phrase "Even number" appears on the page, and otherwise the phrase "Odd number". The word Even means even (zugh) and the word Odd means odd.
>
> ![Book image](../images/p217-03.png)
>
> The script for finding out whether a number is even or odd can also be written with the **if-else** structure. Change the previous script as in the following figure and check the result in the browser console.
>
> ![Book image](../images/p217-01.png)
>
> ![Book image](../images/p217-02.png)

![Figure 10](../images/p217-04.png)
*Figure 10*

**The else-if structure**: makes it possible to check several conditions one after another. In this step the grade of a student is decided based on the score obtained. At the end of the previous script, write the code opposite.

In this script, the variable score is defined with the value 70 to hold the student's score. First the condition `score>=90` and then the condition `score>=80` are checked. Since both conditions are false, the `console.log()` statements in lines 3 and 5 do not run. Then the condition `score>=70` is checked. Since this condition holds, statement number 7 runs and the phrase Grade: C is printed on the page. After statement 7 runs, the next conditions are not checked and the control of the program moves to line 13.

<!-- page 212 -->

> **Learn more**
>
> **The Switch structure**
>
> The switch structure is used to choose among several blocks of code, based on the value of one variable. If the conditions of the problem are limited only to comparing one variable with certain values, the switch structure can be used instead of several else-ifs.

> **Workshop**
>
> **Using the switch conditional structure**
>
> ![Book image](../images/p218-01.png)
>
> Write a script that receives the grade of a student from the variable grade and, based on the value of the grade, shows a suitable message to the user.
>
> For this purpose, put the script in the file `workshop6.html` inside comment signs and then write the code opposite to check the grade.
>
> In this example the switch conditional structure checks the value of the variable grade with different cases; as soon as the value opposite a case is the same as the value of the variable grade, the statement after the : sign runs and then the exit from the switch structure is done by the break statement. If the value of the variable grade is not the same as any of the values written opposite the cases, the statement for the default case runs.

> **Note**
>
> If the condition of a case holds but the break statement is not in it, the next case is checked by the program too.

> **Activity**
>
> Remove the break statement in case A and check the output of the program in the browser. Then remove the break statement from opposite the next cases and analyse the result.
