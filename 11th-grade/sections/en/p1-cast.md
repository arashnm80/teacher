<!-- page 13 -->

This statement receives the value typed on the keyboard as a string (**string**), and its output is a string value (even if you typed a "number") (Figure 25).

> **Activity**
>
> Define the variables food, weighe, and avg for your favorite food, your weight, and your grade average. Get a value for each one from the input, then show the values and find the type of each.

![Figure 25](../images/p019-02.png)
*Figure 25*

## Type casting in Python

In Python programming you sometimes need to convert a piece of data from one type to another. This is called **data type conversion**, or **Type Casting**.

![Figure 26](../images/p019-01.png)
*Figure 26*

برای مثال، وقتی ورودی را با تابع `input()` دریافت می‌کنید، مقدار واردشده به‌صورت **رشته (str)** ذخیره می‌شود. اگر بخواهید با آن محاسبات ریاضی انجام دهید، لازم است آن را به عدد تبدیل کنید.

For type conversion, Python gives the programmer ready-made functions, such as:

- Convert to an integer → `int()`

- Convert to a decimal number → `float()`

- Convert to a string → `str()`

- Convert to a boolean (true/false) → `bool()`

<!-- page 14 -->

As in Figure 27, to convert data to a number you can do this:

Example: write a program that gets the user's age and shows it with a suitable message.

![Figure 27](../images/p020-01.png)
*Figure 27*

**Example**: look closely at this example.

When you run it, you will see an error, because the number is attached directly to the text, and that is not allowed (Figure 28).

![Figure 28](../images/p020-02.png)
*Figure 28*

To fix this error, convert the number to a string as shown below. After running it, you will see no error (Figure 29).

![Figure 29](../images/p020-03.png)
*Figure 29*

**مثال**: در خط1 کد مقابل سال تولد کاربر دریافت می‌شود، تابع int آن را به نوع عددی صحیح تبدیل و در متغیر year ذخیره می‌کند. در خط2 تفاضل عدد سال فعلی از سال تولد محاسبه و در متغیر age ذخیره می‌شود. در خط 3 با دستور print سن کاربر با پیغام "your age:" نمایش داده می‌شود (شکل30).

![Figure 30](../images/p020-04.png)
*Figure 30*

<!-- page 15 -->

**Example**: the value of the price variable is an integer. On line 2, the float function is used to convert it to a decimal number (Figure 31).

![Figure 31](../images/p021-01.png)
*Figure 31*

**مثال**: تابع input وزن را به‌صورت یک مقدار عددی دریافت می‌کند و خروجی آن یک مقدار متنی است که تابع float آن را به نوع عدد اعشاری تبدیل و در متغیر weight ذخیره می‌کند. در خط بعد دستور print دو رشته را با عملگر " + " به هم الحاق می‌کند (شکل32).

![Figure 32](../images/p021-02.png)
*Figure 32*

You can see that on this line the str function converts the weight variable back to text.

**Example: the price of an item after adding 9 percent value-added tax** (Figure 33).

![Figure 33](../images/p021-03.png)
*Figure 33*

> **Activity**
>
> Get the user's height as a decimal number and show a message like the one below.
>
> Your height: 1.75 meters.

> **Activity**
>
> To set up a smart shop, do the following steps.
>
> Get the shop manager's name from the input
>
> Get the year the shop started
>
> Convert the data types of the inputs
>
> Show a welcome message
