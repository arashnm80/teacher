<!-- page 33 -->

In Python there are two main structures for loops:

1. The for loop

2. The while loop

**The for loop**: used to run statements for each item of a sequence (such as a list, string, tuple, set, or dictionary), usually when the number of repetitions is known in advance or can be worked out.

The general form of the for loop in Python is:

```
for variable in sequence:
      statements
```

In this structure:

- variable is a variable that receives one element of the sequence on each pass.

- The variable name can be anything; for example (i, count, num, student…)

- sequence is a sequence such as a list, string, tuple, set, or dictionary.

- statements are the statements in the body of the loop that run on each pass. They are called the loop block, and they must be indented by one tab.

### Going through lists

**Example 1**: the code below prints the elements of a list of three colors (red, blue, green) (Figure 73).

![Figure 73](../images/p039-01.png)
*Figure 73*

**About the code**: on the first line, a list holding the names of three colors as strings is defined.

On the second line, the for statement goes through the list elements in order and puts each element in the item variable.

**Example 2**: showing a shopping cart. In this program a list named `shopping_cart` is created first and the purchased items are stored in it. Then the elements of the list are printed with a for loop. Run the program and see the result (Figure 74).

![Figure 74](../images/p039-02.png)
*Figure 74*

<!-- page 34 -->

**About the code**: on the first line, a list holding the names of the purchased items as strings is defined. The second line prints a suitable message before the loop starts.

On the third line, the for statement goes through the list elements in order and puts each element in the item variable. On the last line, a message with the name of each element of the list is printed.

![Figure 75](../images/p040-01.png)
*Figure 75*

### Going through strings

Example: printing the letters of the word python (Figure 75)

**About the code**: on each pass of the loop, one letter of the string python is put in the ch variable, and that value is printed inside the loop.

### Some uses of the for loop

**Example 1**: the program below counts the elements of a list with a for loop (Figure 76).

![Figure 76](../images/p040-02.png)
*Figure 76*

**About the code**: on the first line, a list holding the names of some fruits as strings is defined.

On the second line, the variable count is created with the starting value zero.

On the third line, the for loop goes through the list elements in order and puts each element in the fruit variable. On the fourth line, one is added to count on each pass of the loop. The two statements below are equivalent.

```
count + = 1
count = count + 1
```

On the last line, the final value of count is printed. Note that this line is outside the loop.

<!-- page 35 -->

> **Activity**
>
> Python has a ready-made function that does what the code on the previous page does; research it.

**Example 2**: if the goal is to count one particular element inside the loop (for example, the number of apples), you can change the program with an if statement as below (Figure 77).

![Figure 77](../images/p041-01.png)
*Figure 77*

**About the code**: on the fourth line, the if statement checks whether the value of fruit equals apple. If it does, one is added to count.

> **Activity**
>
> Lists have a method that does what the code above does; research it.

**Using the `range()` function**: so far the for loop has been used to go through the elements of lists and strings.

Sometimes a statement must be repeated a certain number of times without a ready list of values.

In such cases the range function is used.

The `range()` function produces a sequence of numbers that starts at start and goes on, in steps of step, until just before stop.

Start: (optional, with a default)

![Figure 78](../images/p041-02.png)
*Figure 78*

Stop: (required), and it is not itself included. Step: (optional), default one.

<!-- page 36 -->

**اولین حالت**: در ساده‌ترین حالت، تابع `range()` تنها یک عدد دریافت می‌کند که به‌صورت `range(stop)` نوشته می‌شود. به مثال زیر توجه کنید:

![Figure 79](../images/p042-02.png)
*Figure 79*

**Example**: a loop that prints the numbers 0 to 4 (Figure 79).

**About the code**: the start value (start) is zero by default, and the step (step) is one by default. The end value (stop) is 5, and 5 itself is not produced. range(5) produces the numbers 0 to 4. The for loop runs 5 times. On each pass the variable i gets one of these numbers. On the second line, the value of i is printed on each pass.

**The second form: using the function as `range(start, stop)`**.

Example: a loop that prints the numbers 1 to 6 (Figure 80).

![Figure 80](../images/p042-03.png)
*Figure 80*

**About the code**: the start value (start) in the range statement is one.

The end value of the loop (stop) is 7, but 7 itself is not included. The range function produces the numbers 1 to 6.

The step (step) is one by default.

**در حالت سوم، ** تابع range سه عدد دریافت می‌کند که به‌صورت `range(start, stop, step)` نوشته می‌شود. به مثال زیر توجه کنید:

Example: a loop that prints the even numbers less than 10 (Figure 81).

![Figure 81](../images/p042-01.png)
*Figure 81*

<!-- page 37 -->

**About the code**: the start value (start) in the range statement is zero.

The end value (stop) is 10, but 10 itself is not produced. The step (step) is 2.

The range function produces the even numbers from 0 to 8.

> **Activity**
>
> Change the previous program so that it prints the even numbers from largest to smallest. For this, step must be negative, and start and stop must be changed to match.

> **Activity**
>
> Write a program that gets from the user the waiting time for food (in minutes) as a number and shows a countdown.
>
> At each step, print the message below:
>
> Time remaining: X minutes, where X is replaced by the time left.
>
> When the count reaches zero, show the message below.
>
> Your food is ready!

> **Activity**
>
> Write a program that gets the heights of 5 people from the input and calculates and shows their average height.

The underscore character (\_ ) is allowed in variable names, so it can also be used on its own as the name of a variable.

![Figure 82](../images/p043-01.png)
*Figure 82*

Look at the code in Figure 82.

In this example the loop counter variable is not used in the body of the loop, so the underscore character (\_) can be used instead. Using \_ shows that the value of that variable will not be used later in the program.

> **Curiosity**
>
> Find out what the advantages are of using \_ instead of a variable name.

<!-- page 38 -->

### The control statements break and continue in loops

In Python, the control statements break and continue are used to control how loops run.

**continue**: used to skip a certain part of the loop and go on to the next pass.

**break**: stops the loop completely and **exits** it.

**Example**: write and run the program below. In this program the names of all the foods in a list are printed, each on its own line. (Figure 83)

![Figure 83](../images/p044-02.png)
*Figure 83*

Now, if you want a certain food (for example, soup) not to be shown when printing, you can use the continue statement inside the loop. Write and run the code below carefully, and pay attention to the indentation (Indentation) as you write it (Figure 84).

![Figure 84](../images/p044-01.png)
*Figure 84*

**About the code**: the line `if item == " soup"` checks whether the value of the item variable equals soup.

If the if condition holds, the continue statement runs and makes the loop go straight to the next element, which is "ash". That is why soup is not printed in the output.

In general, with continue the loop skips part of the code inside it for certain passes and goes straight to the start of the next pass.

<!-- page 39 -->

Now, if you want a certain message to be printed and the loop to **end** when a certain food (for example, soup) is reached, you can use the break statement inside the loop. Write and run the code below. Pay attention to the indentation (Indentation) as you write it (Figure 85).

![Figure 85](../images/p045-01.png)
*Figure 85*

**About the code**: the third line checks whether the value of the item variable equals soup.

If the if condition holds, the message "Soup is not a meal!" is printed first, then break runs and the program continues after the loop. In this case the loop stops completely and no more passes are made (Figure 86).

Now write and run the two programs below.

![Figure 86](../images/p045-02.png)
*Figure 86*

> **Curiosity**
>
> Based on the output of the programs above, explain what break and continue do in each program.
