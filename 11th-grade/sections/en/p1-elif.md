<!-- page 27 -->

> **Activity**
>
> Write a program that lets a user log in only if:
>
> a username has been entered **and** (the password is correct or the verification code is active).

**Example**: making sure a value is not allowed: in this example the program uses the comparison operator `!=`, meaning «not equal», and if the username entered is not equal to "guest"… the entry is blocked with a suitable message. Run the program and check the result with different data (Figure 60).

![Figure 60](../images/p033-01.png)
*Figure 60*

![Book image](../images/p033-02.png)

**مثال**: در این برنامه عملگر `>` برای بررسی شرط بیشتر بودن نمره هنرجو در دروس پودمانی از عدد 12 استفاده شده است. برنامه را اجرا و نتیجه را با داده‌های مختلف بررسی کنید (شکل61).

![Figure 61](../images/p033-03.png)
*Figure 61*

**مثال**: در این برنامه عملگر `<` برای بررسی محدودیت سنی زیر ۱۸ سال برای ورود به سایت استفاده شده است. برنامه را اجرا و نتیجه را با داده‌های مختلف بررسی کنید (شکل62).

![Figure 62](../images/p033-04.png)
*Figure 62*

<!-- page 28 -->

**مثال**: در این برنامه محدودیت تعداد سفارش کالا با عملگر `<=` مورد بررسی قرار گرفته است که تنها به تعداد ۵ یا کمتر از ۵ را شامل می‌شود. برنامه را اجرا و نتیجه را با داده‌های مختلف بررسی کنید (شکل63).

![Figure 63](../images/p034-03.png)
*Figure 63*

**مثال**: در این برنامه محدودیت پایه تحصیلی 11 برای ورود به سیستم پیشرفته با عملگر `>=` برقرار شده است. برنامه را اجرا و نتیجه را با داده‌های مختلف بررسی کنید (شکل64).

![Figure 64](../images/p034-04.png)
*Figure 64*

**مثال**: در این برنامه شرط ورود به مرحله دوم مسابقه سن حداقل ۱۸ و امتیاز حداقل 70 در نظر گرفته شده است. برنامه با عملگرهای مقایسه `>=` به معنی بزرگ‌تر مساوی و عملگر منطقی and به معنی " و " نوشته شده است. نتیجه عملگر and زمانی True است که هر دو عبارت و هر دو True باشند. برنامه را اجرا و نتیجه را با داده‌های مختلف بررسی کنید (شکل65).

![Book image](../images/p034-01.png)

![Book image](../images/p034-02.png)

![Figure 65](../images/p034-05.png)
*Figure 65*

<!-- page 29 -->

**Example**: in this program the logical operator or is placed between two expressions and checks whether either of them holds. Its result is true when one of the expressions on either side of or is true. Run the program and check the result with different data (Figure 66).

![Figure 66](../images/p035-01.png)
*Figure 66*

> **Activity**
>
> Write a program that gets the user's age and country and, if the age is greater than or equal to 18 and the country is Iran, shows the message "You are allowed to register".

### The third form of the conditional structure: if – elif – else

This structure is used when there are **several different conditions** and the program must **choose one of them**. elif checks a new condition when the previous conditions did not hold; that is, once one of the if or elif conditions holds and its statements run, the remaining elif conditions are not checked. elif is short for else if and is used to check further conditions. The difference between else and elif is that no condition is written after else.

### The general form of if – elif – else

```
if condition1:
     statements1
elif condition2:
     statements2
else:
     statements_else
```

<!-- page 30 -->

**Example**: write a program that reads the game level from the input and shows a suitable message based on it. Write and run the program and check the result with different data (Figure 67).

![Figure 67](../images/p036-01.png)
*Figure 67*

**Example**: write a program that, after getting the food and the drink from the user, checks the following:

If pizza with a drink is chosen ← price 140000

If pizza without a drink ← price 120000

Otherwise ← print the message «Other option». This example uses the logical operator and in the condition. Write and run the program (Figure 68).

![Figure 68](../images/p036-02.png)
*Figure 68*

**Example**: the statements below get the status of a device from the user and show a suitable message based on it. Run the program below and check the result (Figure 69).

![Figure 69](../images/p036-03.png)
*Figure 69*

<!-- page 31 -->

The advantage of if-elif-else over several separate if statements is that once a condition holds, the program does not check the later conditions. This makes the program run faster and work more efficiently.

> **Activity**
>
> A seller is giving a discount to people who buy apples. Write a program that gets the fruit name and the quantity from the user: if the fruit is apple and the quantity is at least 5, show the message "Discount applied".
>
> Otherwise show the message "No discount".

> **Activity**
>
> Write a program in which the user enters their age. The program must check the following:
>
> If the user's age is between 18 and 25, show the message "Welcome, young adult".
>
> If the user's age is greater than or equal to 26, show the message "Welcome, adult".
>
> If the user's age is less than 18, show the message "You are underage".

> **Activity**
>
> Write a program that uses if and elif with an order status entered by the seller and, based on the order status in an online shop (Delivered /Sent /Registered), announces how the goods will be shipped with suitable messages:
>
> Your order has been successfully delivered - Your order is on the way - Your order is being processed - Status unknown.

> **Activity**
>
> Write a program that gets a student's score as a whole number between 1 and 100.
>
> If the score is ≥ 90 ← message "exelent"
>
> If the score is between 69 and 90 ← message "good"
>
> If the score is between 50 and 69 ← message "pass"
>
> If the score is `<` 50 ← show the message "fail".

**Example**: write a program that prints a suitable message if the value of choice is one of the options below, and otherwise shows the message Food not available (Figure 70).

A) The food menu has the two options below

![Figure 70](../images/p037-01.png)
*Figure 70*

:

- Pizza

- burger

<!-- page 32 -->

B) Extend the program for a food menu with the three options below: (Figure 71)

- pizza

- burger

- pasta

![Figure 71](../images/p038-01.png)
*Figure 71*

In the example above, what happens if the menu has 20 foods? Or if a new food is added tomorrow? The first solution that comes to mind is to use more if statements. But that makes the code longer and harder. The real solution is to use lists and loop statements properly.

### حلقه‌های تکرار (Loop)

When coding, if a statement or a group of statements must run several times, **loop structures** are used. They make code shorter, more readable, and easier to manage. For example, if you need a program that prints the word python 10 times, instead of writing the statement `print('python')` ten separate times, you can put it once inside a loop so that it runs ten times automatically.

![Figure 72](../images/p038-02.png)
*Figure 72*
