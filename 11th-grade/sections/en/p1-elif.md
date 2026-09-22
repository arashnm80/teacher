**Page 27**

### Activity

Write a program so that a user is allowed to log in only if:

a username has been entered and (the password is correct or the verification code is active).

Example: Making sure a value is invalid: in this example the program is written with the comparison operator != meaning inequality, and if the entered username is not equal to `"guest"`, the user is prevented from entering with an appropriate message. Run the program and check the result with different data (Figure 60).

![Book image](../images/p033-01.png)

![Book image](../images/p033-02.png)

![Figure 60](../images/p033-03.png)

**Figure 60**

Example: In this program the operator < is used to check the condition that the student's grade in modular courses is greater than the number 12. Run the program and check the result with different data (Figure 61).

![Figure 61](../images/p033-04.png)

**Figure 61**

Example: In this program the operator > is used to check the age limit under 18 for entering the site. Run the program and check the result with different data (Figure 62).

![Figure 62](../images/p033-05.png)

**Figure 62**


---

**Page 28**

Example: In this program the limit on the number of product orders is checked with the operator >=, which includes only a quantity of 5 or less than 5. Run the program and check the result with different data (Figure 63).

![Figure 63](../images/p034-01.png)

**Figure 63**

Example: In this program the grade-11 limit for entering the advanced system is set with the operator <=.

Run the program and check the result with different data (Figure 64).

![Figure 64](../images/p034-02.png)

**Figure 64**

Example: In this program the condition for entering the second stage of the contest is a minimum age of 18 and a minimum score of 70. The program is written with the comparison operators >= meaning greater than or equal and the logical operator `and` meaning "and". The result of the operator `and` is `True` when both expressions

and

both

are `True`. Run the program and check the result with different data (Figure 65).

![Figure 65](../images/p034-03.png)

**Figure 65**


---

**Page 29**

Example: In this program the logical operator `or` is placed between two expressions and checks the condition for one of the expressions to be true. Its result is `true` when one of the expressions on either side of `or` is true. Run the program and check the result with different data (Figure 66).

![Figure 66](../images/p035-01.png)

**Figure 66**

### Activity

Write a program that receives the user's age and country name and, if the age is greater than or equal to 18 and the country name is Iran, displays the message "You are allowed to register".

Third type of the conditional structure `if` – `elif`– `else`:

This structure is used when there are several different conditions and the program must choose one of them. `elif` checks a new condition if the previous conditions were not met; that is, if one of the `if` or `elif` conditions is met and its statement is executed, the other `elif` conditions will not be checked. `elif` is short for `else` `if` and is used to check later conditions. The difference between `else` and `elif` is that after `else` no condition is written.

Overall structure of `if` – `elif` – `else:`

```
:if condition1
statements1
:elif condition2
statements2
```

`:else`

```
statements_else
```


---

**Page 30**

Example: Write a program that receives the game level from input and then displays an appropriate message based on it.

Write the program, run it, and check the result with different data (Figure 67).

![Figure 67](../images/p036-01.png)

**Figure 67**

Example: Write a program that, after receiving the type of food and drink from the user, checks the following:

If pizza and a drink are selected → price 140000 If pizza without a drink → price 120000 otherwise → print the message «`Other` `option`». In this example the logical operator `and` is used in the condition. Write and run the program (Figure 68).

![Figure 68](../images/p036-02.png)

**Figure 68**

Example: The statements below receive the device status from the user and display an appropriate message based on it.

Run the program below and check the result (Figure 69).

![Book image](../images/p036-03.png)

![Book image](../images/p036-04.png)

Output

**Figure 69**


---

**Page 31**

The advantage of using the `if-elif-else` structure instead of several separate `if` statements is that if a condition is met, the later conditions are not checked by the program. This feature increases the program's execution speed and makes its performance more efficient.

### Activity

The seller has put a discount on apple fruit for buyers. Write a program that gets the fruit name and the purchase quantity from the user: if the fruit is `apple` and the quantity is at least 5, display the message `"Discount` `applied"`.

Otherwise display the message `"No` `discount"`.

### Activity

Write a program in which the user enters their age. The program must check the following:

If the user's age is between 18 and 25 years, display the message `"Welcome`, `young` `adult"`.

If the user's age is greater than or equal to 26, display the message `"Welcome`, `adult"`.

If the user's age is less than 18, display the message `"You` `are` `underage"`.

### Activity

Write a program that uses the `if` , `elif` statements by receiving the order status from the seller and, based on the order status (`Delivered` `/Sent` `/Registered`) in an online store, announces how the product is shipped with appropriate messages:

```
Your order has been successfully delivered - Your order is on the way - Your order
.is being processed - Status unknown
```

### Activity

Write a program that receives a student's score as an integer between 1 and 100.

If score ≥ 90 → message `"exelent"` If score between 69 and 90 → message `"good"` If score between 50 and 69 → message `"pass"` If score < 50 → display the message `"fail"`.

Example: Write a program that if the value of `choice` is one of the options below, prints an appropriate message and otherwise displays the message `Food` `not` `available` (Figure 70).

a) The food menu includes the two options below:

![Book image](../images/p037-01.png)

`Pizza`

```
burger
```

![Figure 70](../images/p037-02.png)

**Figure 70**


---

**Page 32**

b) Extend the program so that if the food menu includes the three options below: (Figure 71)

`pizza`

```
burger
```

`pasta`

![Book image](../images/p038-01.png)

![Figure 71](../images/p038-02.png)

**Figure 71**

In the example above, what happens if the menu has 20 foods? Or if a new food is added tomorrow? The first solution that comes to mind is to use more `if` statements. But that makes the code longer and harder. The solution is to use lists correctly and repetition-loop statements.

Repetition loops (`Loop`):

When coding, if a statement or a set of statements needs to be executed several times, repetition-loop structures are used. These structures make the code more readable, shorter and more readable, and easier to manage.

![Book image](../images/p038-03.png)

For example, if you need to write a program that prints the word `python` 10 times, instead of writing the statement print('python') ten times separately, you can put this statement only once inside a loop so that its execution is automatically repeated ten times.

**Figure 72**


---
