<!-- page 198 -->

Defining variables can also be done automatically. Automatic variable definition happens when a variable is given a value.

> **Example**
>
> In the following example the two variables x and z are defined automatically:
>
> ```
> x = 10;
> z = x + 10;
> ```

> **Learn more**
>
> **Constants**: constants (const) have a fixed value during the running of the program. Constants are defined and given a value once and cannot be given a value again after that.

> **Example**
>
> In the following example the constant PI is defined with the value 3.141592. Changing the value of PI in the second and third lines causes an error.
>
> ```
> const PI = 3.141592;
> PI = 3.14;
> PI = PI + 10;
> ```

### Principles of naming variables

- The name of a variable can contain English letters, numbers, the $ sign and the underscore (\_), but numbers must not be used at the start of the variable name.

- JavaScript is case-sensitive, so the names price, Price and PRICE are three different variables.

- JavaScript's reserved words (which have a special meaning) must not be used as variable names, such as let and var, if, for and so on.

JavaScript also makes it possible to define variables in one line, but at the end of each variable definition a comma must be used to separate them.

```
let firstName = "Sara", lastName = "Jones", studentId = "1234567";
```

Giving values to variables is done with the assignment operator (`=`). If a variable is not given a value, its value will be undefined (Undefined).

> **Activity**
>
> Specify whether the definitions of the following variables are correct or not.
>
> ```
> myVar = 2 ;           …...……..
> 2x = 10;             …………..
> user-name ="Safa";     …………..
> var = 20;             …………..
> ```

<!-- page 199 -->

### Showing the value of variables and strings

To show the value of a variable in the browser console, the console statement is used as in form 5:

![Figure 5](../images/p205-01.png)
*Figure 5*

Considering that JavaScript is case-sensitive, writing the statement `console.log(X)` causes the following error message to be shown:

![Figure 6](../images/p205-02.png)
*Figure 6*

To show a text string in the console or on the web page, quotation marks are used around the text, but variables do not need these marks. In the following example a text phrase together with the value of the variable x is shown in the console.

![Figure 7](../images/p205-03.png)
*Figure 7*

Here the + operator is used to stick two phrases to each other. Depending on the type of the data, this operator can act as the arithmetic addition operator or as string concatenation.

> **Workshop**
>
> **Defining a variable and showing it in JavaScript**
>
> In the rest of the script of the file `workshop1.html`, define the variables x and y with the values 5 and 10 and then show their values in the browser console:
>
> ![Book image](../images/p205-04.png)
>
> ![Book image](../images/p205-05.png)
>
> Create a variable as follows and then show its value in the console.
>
> ```
> let test;
> ```
>
> Considering that the variable test has not been given a value, if the statement `console.log(test)` is used, the message ……………… appears.

<!-- page 200 -->

### Data types

In a programming language, variables can store different data types inside them. Storing each data type needs a different amount of memory; data types let programming languages use memory more effectively. Programmers can also organise data in a more logical and coherent way. Table 15 shows the data types that can be used in JavaScript.

*Table 15: Data types in JavaScript*

![Table 15: Data types in JavaScript](../images/p206-01.png)

> **Workshop**
>
> **Working with data types**
>
> 1. Create an HTML document named `workshop2.html` and in the `<body>` section write the tag `<script>`. Define the variables x, Family, d and names inside the `<script>` tag according to the examples of the table above and then show their values in the console like the following statement:
>
> ```
> console.log("The value of x is: "+ x);
> ```

<!-- page 201 -->

> **Workshop (continued)**
>
> 2. The **typeof** operator in JavaScript specifies the data type of a variable. This operator can be used with or without parentheses. At the end of the script of the file `workshop2.html` use this operator, as in the following example, to check the data type of the variables x, Family, d and names, and write the results in the blank.
>
> ```
> console.log("x: "+ typeof(x));         x: number   Family: …….   d: …….    names: ……
> ```
>
> 3. Check the behaviour of the browser in interpreting the following code and complete the blank based on your conclusion. `let a = 10 + 20 + "Blue";`
>
> ```
> let b = "Blue" + 10 + 20;
> ```
>
> In the first line, the operands 10 and 20 are at the start of the arithmetic expression, so JavaScript regards the numbers 10 and 20 as the data type number, and as a result the value ........................ is stored in the variable a. In the second line, because the string Blue is at the start of the arithmetic expression, the next operands are regarded as the data type .......................... and so the value .......................... is stored in the variable b.
>
> 4. The data type of a variable can change during the program. In the following script, the variable x is first created as undefined (Undefined). The data type of the variable x changes in line 2 to the type ............................ when it receives the value 10, and in line 3 to the type ....................... when it receives the value sara1980.
>
> ```
> 1  let x;
> 2  x = 10;
> 3  x = "sara1980";
> ```

### Converting data types

JavaScript makes converting the data type of variables possible in two ways: implicit and explicit conversion. When the data type of a variable is converted automatically, an implicit conversion has happened.

> **Example**
>
> The following example shows a case of implicit type conversion:
>
> ![Book image](../images/p207-02.png)
>
> ![Book image](../images/p207-01.png)
>
> In the first line, the variable s is defined as numeric. In the fourth line, the result of adding the variable w and the string 100 is the phrase 10100, which is put in the variable s. As a result the data type of the variable s becomes string. Using the operator `typeof()` in lines 2 and 6 shows the data type of the variable s.

<!-- page 202 -->

Explicit conversion of the data type is done by JavaScript's built-in functions. The conversion functions include `parseInt()`, `parseFloat()`, `Number()`, `String()` and `Boolean()`, which convert the data type of the input argument to integer, decimal, numeric, string and logical types.

> **Workshop**
>
> **Working with the type conversion functions**
>
> Create the following variables at the end of the script of the file `workshop2.html`.
>
> ```
> x = "15.25" , y = 123 , z = 1;
> 1 let num1 = parseInt(x);            …15...     …number...
> 2 let num2 = parseFloat(y)         ……...     …………....
> 3 let num3 = Number(x);            ……...     …………....
> 4 let num4 = Number(true);        ……...     …………....
> 5 str = String(y);                          ……...     …………....
> 6 let bool = Boolean(z);               ……...     …………...
> ```
>
> Then check the value and data type of the variables created in lines 2 to 7 with the function `typeof()` and write the result in the blank as in the example. To check the values and types of the variables, act as in the following pattern:
>
> ```
> console.log(num1 +": "+ typeof(num1));
> ```

> **Note**
>
> The reason for not using the keyword let for the variables x, y, z and str is that these variables were created in the earlier workshops. So using the keyword let again causes an error.

### Operators

![Figure 8](../images/p208-01.png)
*Figure 8*

In programming languages, operators are used to do operations on variables and values; the values an operator works on are called **operands**. In the expression `z = x + y` the signs + and `=` are **operators** and the letters x, y and z are operands. In this section the JavaScript operators are described.
