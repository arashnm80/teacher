<!-- page 8 -->

## Variables and data types

A variable is a place in RAM used to store data temporarily. In Python you do not need to declare a variable first and then initialize it; the data type is detected automatically (Figure 14). Just write the variable name on the left of the assignment operator " `=` " and its value on the right. `name="baran" , num = 55` Python supports several kinds of variables (Figure 15).

![Figure 15](../images/p014-03.png)
*Figure 15*

![Figure 14](../images/p014-04.png)
*Figure 14*

Python works out the type of a variable from the value assigned to it.

**Example**: `num1=15` in this example Python makes the variable an integer, and you do not have to state its type.

### Common data types in Python

![Figure 16](../images/p014-01.png)
*Figure 16*

**نوع داده رشته‌ای (str)**: هر چیزی که **متن باشد**، مثل اسم، پیام، ایمیل، رمز عبور، شماره تلفن، توضیح، نوع داده رشته‌ای (**str**) است.

The **str** type, short for **string**, can be defined with single, double, or triple quotation marks (Figure 16).

- **نوع داده عدد صحیح (int)**: عددهایی که با آنها محاسبه انجام می‌دهید و اعشار ندارند همان عددهای صحیح (**int**) یا همان **integer**، هستند (شکل17).

![Figure 17](../images/p014-02.png)
*Figure 17*

<!-- page 9 -->

- **نوع داده عدد اعشاری (float)**: این داده‌ها عددی هستند و در محاسبات ریاضی به کار گرفته می‌شوند و دارای مقدار اعشاری هستند. مثل:

```
  height = 1.75
```

- **The `type()` function**: the output of the **`type()`** function is the **data type** of a variable (Figure 18).

![Figure 18](../images/p015-01.png)
*Figure 18*

از این مرحله به بعد کدها را در محیط VS Code بنویسید. برای انجام این کار برنامه VS Code را اجرا کرده و سپس از منوی فایل دستور new folder یک‌پوشه جدید به نام PyProg ایجاد کنید و سپس در آن پوشه از منو فایل با انتخاب گزینه New File، کادر EXPLORER انتخاب دکمه New File و یا کلید‌های ترکیبی Ctrl+ N فایل جدیدی به نام `prog01.py` در این پوشه ایجاد کنید (شکل 19). حالا صفحه ویرایشگر کد باز شده و می‌توانید دستورات خود را در آن بنویسید.

![Figure 19](../images/p015-02.png)
*Figure 19*

To run the statements, use the button at the top right of the program window or the Run menu. The result is shown at the bottom of the window (Figure 20).

![Figure 20](../images/p015-03.png)
*Figure 20*

**Python style guide** (PEP)

نحوه نگارش کدهای پایتون و قراردادهای کدنویسی را ارائه می‌دهد و باعث خوانایی بیشتر و تمیز (clean) شدن کدها می‌شود. برای مشاهده می‌توانید به `pep8.ir` مراجعه کنید.

<!-- page 10 -->

> **Curiosity**
>
> After reading the pep8 principles, answer these questions:
>
> 1. At most, how many characters can you write on one line?
>
> 2. How many characters should an indent be?
>
> 3. Can a line start with a space character?

در VSCode پس از کدنویسی با فشار کلیدهای Alt+Shift+F به طور خودکار بیشتر مشکلات فرمت کد را بر اساس pep8 اصلاح می‌کند. به‌شرط آنکه یکی از افزونه‌های autopep8، Black formatter، Ruff یا yapf نصب شده باشد.

### Rules for naming variables in Python

- A variable name cannot contain a space. For example, you cannot define a variable named is valid.

- نام‌گذاری متغیرها در پایتون باید با یک حرف یا زیر خط آغاز شود. مثل (`num`، `_personal`)

- A variable name can contain letters, digits, and underscores.

- نام متغیرها به حروف کوچک و بزرگ حساس است Age، age و AGE سه متغیر متفاوت هستند.

- A variable name must not be one of Python's keywords. The names var, import, const, if, and for are wrong as variable names, because these words are Python keywords.

> **Note**
>
> In Python, a keyword is a word that the language itself reserves for its statements and structures. These words have a predefined meaning, so they cannot be used as names of variables, functions, or classes.

> **Curiosity**
>
> Python has several ways to name variables made of more than one word. Research them and present them in class.

**عملگر (operator)**: نمادهای ویژه‌ای هستند که عملیات خاصی را روی مقادیر یا متغیرها انجام می‌دهند. در این عبارات a + b یا c \* d یا 4/2 به +، \* و / عملگر (operator) گفته می‌شود.

**عملوند (operand)**: مقدار یا مقدارهایی هستند که عملگرها روی آن کار می‌کنند. مثلاً در عبارت a + b علامت "+" عملگر و a, b عملوند هستند.

<!-- page 11 -->

The operands of the " +" operator in Python can both be numbers or both be strings. In the first case you get mathematical addition, and in the second case concatenation (**concatenation**) (Figure 21).

![Figure 21](../images/p017-03.png)
*Figure 21*

> **Curiosity**
>
> What happens if, with the + operator, one operand is a number and the other is a string?

> **Project**
>
> ### The cook project
>
> Write a program that picks one food at random from a list of foods.
>
> ![Book image](../images/p017-01.png)
>
> On the first line, bring (**import**) the **random** library into the program so that on line 3 it can use the **choice** method to pick at random.
>
> On the second line you can add your favorite foods to the list, and help your mother choose a meal at home.
>
> On the third line, one food is picked at random from the **foods** list and stored in the **item** variable. On the fourth line, the **item** variable, which now holds the name of a random food, is printed.
>
> - What change could you make to the code so that one food has a better chance of being picked?
>
> Answer: in the code below, repeating the name «ash» gives ash a better chance of being picked.
>
> ![Book image](../images/p017-02.png)

<!-- page 12 -->

### Some kinds of operators in Python

Table 1 shows some arithmetic operators you can use for math calculations.

*Table 1*

**Arithmetic operators**

| Operator | Use |
| --- | --- |
| + | Addition |
| - | Subtraction |
| \* | Multiplication |
| / | Division |
| % | Remainder of division |

![Figure 22](../images/p018-01.png)
*Figure 22*

> **Curiosity**
>
> Research other kinds of operators and present them in class.

### Input and output statements

- **The `print()` statement**: you learned earlier that **print** is used to show output, and you have seen some of its uses.

The **`len()`** function: sometimes you need to know how many characters a text has. This function counts the characters of a text (Figure 23).

![Figure 23](../images/p018-02.png)
*Figure 23*

- **دستور `input()`** : برای دریافت داده از کاربر و ذخیره در متغیر از دستور input استفاده می‌شود (شکل24).

![Figure 24](../images/p018-03.png)
*Figure 24*
