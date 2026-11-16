<!-- page 40 -->

![Figure 87](../images/p046-01.png)
*Figure 87*

### The while loop

This loop runs a set of statements as long as the loop condition is True; as soon as the condition becomes False, the loop stops running and ends. This kind of loop is usually used when **the number of repetitions is not known in advance**.

```
while یا      : شرط حلقه     while condition :
```

statements → the statements in the body of the loop

**Example**: a person at the entrance of a dining hall welcomes the guests of a wedding. They have been told to stand there, ask each guest's name as they come in, and welcome them, and no end has been set for the job. The program below does this with a while loop (Figure 88).

![Figure 88](../images/p046-02.png)
*Figure 88*

**About the program's code**: in front of the while statement, instead of a particular condition, the logical value True is used for now. This makes the loop repeat endlessly, with no way to stop it, because the condition in front of while is always True and never becomes False.

On the next two lines the guest's name is asked and the welcome message is printed.

Since there is no end to the program, to stop it you must either press the key combination Ctrl + C or close the window of the running program.

**Example**: can the program above be written so that the welcoming stops after the groom (damad) arrives?

<!-- page 41 -->

**About the code**: as you can see in the output of the code in Figure 89, the program ends after the groom's name is entered.

![Figure 89](../images/p047-02.png)
*Figure 89*

Inside the loop, after the guest's name is read, an if condition checks whether the name entered equals damad; if it does, break ends the loop and the program continues after the while loop.

**Example**: besides the guests, staff (Employee) are also coming and going in this hall. If you do not want the staff to be welcomed, you can use a condition and the continue statement.

**About the code**: as you can see in the output of the code in Figure 90, after the name Employee is entered the program asks the user for another name, and the staff member is not welcomed. Look at the program's output carefully.

![Figure 90](../images/p047-01.png)
*Figure 90*

When the program reaches continue, it skips the rest of the statements in the loop and goes back to the start of the loop.

Although this program works well, this structure is not very good programming because of the True in front of while, and the loop can be changed as in the next example.

**Example**: the person welcoming the guests has been told to keep doing it as long as the groom has not arrived; the code changes as below.

Notice that in this example the condition for continuing the loop is written in front of the while statement, and there is no need to check anything inside the loop.

<!-- page 42 -->

**About the code**: as you can see in the output of the code in Figure 91, the program ends after the groom's name is entered and he is welcomed.

![Figure 91](../images/p048-01.png)
*Figure 91*

On the first line a variable named name is created with an empty value, so that the loop condition holds at the start.

The second line means: as long as the name entered, that is, the value of the variable (name), is not the word damad, the statements in the loop body keep running.

When the user enters the word damad, after the message is printed the program goes back to the start of the loop; but this time the loop condition is False and the loop ends. Here the code is better and more logical than the previous program.

**Example**: the person welcoming the guests has been told to stand there, ask each guest's name as they come in, and welcome them, and to stop as soon as the groom arrives; but the groom himself does not need to be welcomed. The code above changes a little.

**About the code**: in Figure 92, on the first line, instead of putting an empty string in the name variable, a real name is read from the user with input. So if the name damad is entered on the first line, the loop condition is False, the loop body never runs, and the program ends.

![Figure 92](../images/p048-02.png)
*Figure 92*

Inside the loop the welcome is printed first, and on the next line another name is read, so that on the next pass this name is checked in the loop condition.

> **Note**
>
> All the examples above help the programmer learn how to use the while loop in different situations. By writing the code again and thinking through how each program works, the programmer learns it more thoroughly. For better learning, look at the examples on the next page.

<!-- page 43 -->

**Example**: write a program that gets a whole number from the user and prints its square, and keeps doing this as long as the user enters a number greater than zero (Figure 93).

![Figure 93](../images/p049-01.png)
*Figure 93*

**About the code**: on the first line a whole number is read from the user and put in the number variable.

The meaning of the while condition: the loop statements repeat as long as the value of number is greater than zero.

Inside the loop, the number entered and its square (that is, its second power) are printed with a suitable message first, and then another number is read from the user.

If a value less than or equal to zero is entered on the first line, the loop condition is False, the loop body does not run, and the program ends. Note that in this example the square of zero or of a negative number is not printed.

> **Activity**
>
> Change the program above so that it also prints the cube (Cube) of the number (that is, its third power) as well as its square.

**Example**: write a program that gets the names of some foods from the user and adds (append) them to an empty list. This continues until the user enters the word exit. When the loop finishes, the contents of the list are printed all at once (Figure 94).

![Figure 94](../images/p049-02.png)
*Figure 94*

<!-- page 44 -->

**About the code**: on the first line an empty list is created.

As in the previous examples, first get the name of a food and store it in the food variable.

The meaning of the while condition: the loop statements repeat as long as the value of food is not the string "exit".

Inside the loop, the food name that was read is added to the end of the list with the append method, and then the name of another food is read from the user.

On the last line, outside the loop body, the full contents of the food list are printed.

![Figure 95](../images/p050-01.png)
*Figure 95*

Note that the last line must not be indented by a tab; it must be written exactly in line with while.

**Example**: look at the code below. It prints the numbers one to five, one under another, with a for loop (Figure 95).

If you want to do the same thing with a while loop, the code can be like the code in Figure 96.

**About the code**: on the first line the variable i is given the starting value one.

As in the previous examples, first get the name of a food and store it in the food variable.

![Figure 96](../images/p050-02.png)
*Figure 96*

The meaning of the while condition: the loop statements repeat as long as the value of i is less than 6. Inside the loop, the value of i is printed first. On the last line inside the loop, one is added to the variable.

As you can see, a while loop is more complicated for loops with a known number of repetitions and needs more care. So programmers are advised to think, before they start coding, about which kind of loop suits the problem better.

### Important points about the while loop

In this kind of loop you do not know in advance how many repetitions are needed; the loop goes on as long as the condition holds.

The repetition depends on a condition, which can be a comparison, user input, or the state of the program.

The end is decided by the user or by a certain event, so the loop goes on until the end condition is reached. To control the loop and prevent it from running forever, the loop variable must be given a starting value before the loop begins.

<!-- page 45 -->

Inside the loop, break can be used to end the loop.

Inside the loop, continue can be used to go back to the start of the loop and run it again.

The break and continue statements must be used with an if condition inside loops.

while loops can also be used for loops with a known number of repetitions, but this is not recommended, because such programs are simpler and more logical with a for loop.

> **Activity**
>
> In the previous example, at the end of the program above, print each food in the list on its own line using a for loop.

> **Activity**
>
> Write a program that lets the user order food again and again until they enter "done".
>
> Each time a new food is entered, show the message "`Your order for <food> has been added`." and add (append) the new food to the order list. When the user enters "done", the program shows all the orders.
