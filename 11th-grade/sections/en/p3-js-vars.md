**Page 198**

Variables can also be defined automatically. Automatic definition of a variable happens when a variable is assigned a value.

### Example

In the following example, the two variables `x` and `z` have been defined automatically:

;`x` = 10

;`z` = `x` + 10

### Learn more

Constants (`constants`): Constants (`const`) have a fixed value throughout the program’s run. Constants are defined and assigned a value once, and after that they cannot be assigned a new value.

### Example

In the following example, the constant `PI` is defined with the value 3.141592. Changing the value of `PI` on the second and third lines causes an error.

```
;const PI = 3.141592
```

;`PI` = 3.14

```
;PI = PI + 10
```

Rules for naming variables A variable name can contain English letters, digits, the $ sign, and the underscore (_), but digits must not be used at the beginning of the variable name.

JavaScript is case-sensitive, so the names `price`, `Price`, and `PRICE` are three different variables.

JavaScript reserved words (which have a special meaning) must not be used as variable names, such as

```
let و var، if، for و...
```

JavaScript also lets you define variables on one line, but at the end of each variable definition you must use a comma to separate them.

```
;"let firstName = "Sara", lastName = "Jones", studentId = "1234567
```

Assigning values to variables is done with the assignment operator (=). If a variable is not assigned a value, its value will be undefined (`Undefined`).

### Activity

Determine whether the following variable definitions are done correctly or not.

..……...… ; `myVar` = 2 ..………… ;`2x` = 10

```
..………… ;"user-name ="Safa
```

..………… ;`var` = 20


---

**Page 199**

Displaying the values of variables and strings To display the value of a variable in the browser console, the `console` statement is used as in Figure 5:

![Book image](../images/p205-02.png)

![Figure 5](../images/p205-01.png)

**Figure 5**

Because JavaScript is case-sensitive, writing the statement `console.log`(`X`) causes the following error message to be displayed:

![Figure 6](../images/p205-03.png)

**Figure 6**

To display a text string in the console or on a web page, quotation marks are used around the text, but variables do not need these marks. In the following example, a text phrase together with the value of the variable `x` is displayed in the console.

![Book image](../images/p205-04.png)

![Figure 7](../images/p205-05.png)

**Figure 7**

Here the + operator is used to join two phrases together. Depending on the data types, this operator can act as an arithmetic addition operator or as a string concatenation operator.

Defining a variable and displaying it in JavaScript

### Workshop

Continuing the script in the `workshop1.html` file, define the variables `x` and `y` with the values 5 and 10 and then display their values in the browser console:

![Book image](../images/p205-06.png)

![Book image](../images/p205-07.png)

Create a variable as follows and then display its value in the console.

```
;let test
```

Because the variable `test` has not been assigned a value, if the statement `console.log`(`test`) is used, the message ……………… appears.


---

**Page 200**

Data types In a programming language, variables can store different types of data. Storing each data type requires a different amount of memory; data types allow programming languages to use memory more effectively. Programmers can also organize data in a more logical and coherent way. Table 15 shows the data types that can be used in JavaScript.

Table 15 Data types in JavaScript

Row

Data type

Explanation

### Example

Includes integer and decimal numeric values;`let` `x` = 20 , `y` = 10.75

1

```
عددی (Number)
```

Phrases that are placed inside single

```
;"let family = "Smith
```

2

String (`String`)

or double quotation marks are treated

```
;"let color = "Orange
```

as strings.

```
;let a = true , b = false
```

3

Boolean (`Boolean`)Includes the values `true` and `false`

```
;"let c = x>y , d = "amin" < "Amin
;]let numbers = [10,20,30,40,50
,"let names = ["sara", "mahdi
```

Variables of array type can hold

```
;]"amir"
```

4

Arrays (`Array`)

different data types inside them.

```
,"let data = [100, 5.75, "javascript
```

```
;]true
```

JavaScript objects are specified as

```
, "let obj = {username: "Alfred
Object (object)
```

5

property: value pairs inside braces.

```
;} "password: "admin
```

```
-2022-03"(const date = new Date
```

A date object is created using the `Date`

6Date object (`Date`)

;)"25

class.

Working with data types

### Workshop

1 Create an `HTML` document named `workshop2.html` and write the `<script>` tag in the `<body>` section. Define the variables `x`, `Family`, `d`, and `names` inside the `<script>` tag according to the examples in the table above, and then display their values in the console as in the statement below:

```
;)The value of x is: "+ x"(console.log
```


---

**Page 201**

2 The `typeof` operator in JavaScript determines the data type of a variable. This operator can be used with or without parentheses. At the end of the script in the `workshop2.html` file, use this operator as in the example below to check the data type of the variables `x`, `Family`, `d`, and `names`, and write the results in the blanks.

```
…… :x: number Family: ……. d: ……. names ;)(x)x: "+ typeof"(console.log
```

3 Examine how the browser interprets the following code and complete the blanks based on your conclusion.

```
;"let a = 10 + 20 + "Blue
;let b = "Blue" + 10 + 20
```

In the first line, the operands 10 and 20 are at the beginning of the expression, so JavaScript treats

10 and 20 as the `number` data type; as a result, the value ........................ is stored in the variable `a`. In the second line, because the string `Blue` is at the beginning of the expression, the following operands are treated as the .......................... data type, and therefore the value .......................... is stored in the variable `b`.

4 A variable’s data type can change during the program. In the script below, the variable `x` is first created as undefined (`Undefined`). The data type of the variable `x` changes on line 2, when it receives the value 10, to the ............................ type, and on line 3, when it receives the value `sara1980`, to the ....................... type.

```
;1 let x
```

;2 `x` = 10

```
;"3 x = "sara1980
```

Type conversion JavaScript makes it possible to convert the data type of variables in two ways: implicit (`Implicit`) and explicit (`Explicit`). When the conversion of a variable’s data type is done automatically, an implicit conversion has taken place.

### Example

The following example shows a sample of implicit type conversion:

![Book image](../images/p207-02.png)

![Book image](../images/p207-01.png)

On the first line, the variable `s` is defined as a numeric type. On the fourth line, the result of adding the variable `w` and the string 100 is the phrase 10100, which is placed in the variable `s`. As a result, the data type of the variable `s` is converted to string. Using the `typeof`() operator on lines 2 and 6 causes the data type of the variable `s` to be displayed.


---

**Page 202**

Explicit type conversion is done by JavaScript’s built-in functions. The functions related to data conversion include `parseInt`(), `parseFloat`(), `Number`(), `String`(), and `Boolean`(), which convert the data type of the input argument to integer, floating-point, numeric, string, and Boolean types.

Working with type-conversion functions

### Workshop

Create the following variables at the end of the script in the `workshop2.html` file.

;`x` = "15.25" , `y` = 123 , `z` = 1

```
...15... …number… ;(x)1 let num1 = parseInt
```

....………… ...…… (`y`)2 `let` `num2` = `parseFloat`

....………… ...…… ;(`x`)3 `let` `num3` = `Number`

....………… ...…… ;(`true`)4 `let` `num4` = `Number`

....………… ...…… ;(`y`)5 `str` = `String` ...………… ...…… ;(`z`)6 `let` `bool` = `Boolean`

Then check the value and data type of the variables created on lines 2 through 7 using the `typeof`() function and write the result in the blanks as in the example. To check the values and types of the variables, follow a pattern like this:

```
;)(num1)num1 +": "+ typeof(console.log
```

### Note

The reason the keyword `let` is not used for the variables `x`, `y`, `z`, and `str` is that these variables were created in previous workshops. Therefore, using the word `let` again causes an error.

```
عملگرها (Operators)
```

![Book image](../images/p208-01.png)

In programming languages, operators are used to perform operations on variables and values. The values that an operator acts on are called operands (`Operand`). In the expression `z` = `x` + `y`, the + and = signs are operators and the letters `x`, `y`, and `z` are considered operands. This section describes JavaScript’s operators.

Figure 8


---
