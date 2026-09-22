**Page 219**

The principles of defining a function in JavaScript are as follows:

When defining a function, first the keyword `function` is written and then its name.

The function name must start with a lowercase letter, and each new word must begin with an uppercase letter.

The function’s input parameters are specified inside parentheses.

The number of parameters can be zero, one, or more. The set of function statements is written inside braces.

The function’s output is usually returned to the call site by the `return` statement.

The statements inside a function are executed when the function is called.

To call a function, you must use the function name together with the input arguments. The general form of calling a function is as follows:

```
functionName(Arguments)
```

### Example

In the example below, a function named `calculateCartTotal` has been created with three input parameters `price3`, `price2`, `price1`. The function `calculateCartTotal` calculates the sum of these three parameters’ values and stores it in the variable `total`. The `return` statement returns the value of the variable `total` to the call site.

![Book image](../images/p225-01.png)

![Book image](../images/p225-02.png)

### Note

Parameters are variables that are used when the function is defined. In the example above, the variables `price3`, `price2`, `price1` are the function’s input parameters. An argument refers to the values that are sent to the function when it is called. In other words, arguments are the values that are assigned to the function’s parameters.


---

**Page 220**

Creating a function and calling it

### Workshop

Create a new file named `workshop8.html` and write the function `calculateCartTotal` inside it.

Then call the function with input arguments of your choice.

A function does not necessarily have a return value. A function can be written with the goal of executing a set of instructions without returning a value to the call site. In that case, there will be no need to use the `return` statement. In the example below, the function `showCartTotal` receives three values as input parameters, calculates their sum, and displays the result in the browser console; but it does not return any value to the call site.

![Book image](../images/p226-01.png)

![Book image](../images/p226-02.png)

JavaScript built-in functions (`Built-in` `Functions`): JavaScript has a set of built-in functions that are used to perform various operations. JavaScript’s built-in functions allow programmers to manage data easily and implement complex tasks simply. These functions include mathematical, string, array, object, input–output, and date and time functions, which are introduced in this section.

Using JavaScript’s mathematical functions

### Workshop

JavaScript’s mathematical functions, which are organized inside the `Math` object, are a set of powerful and efficient tools for performing complex mathematical calculations. Access to mathematical functions is possible in dotted form as `Math.functionName`, and using them not only makes coding shorter and more readable but also prevents possible errors in manually implementing algorithms and creates more optimal performance in applications. A few examples of commonly used mathematical functions in JavaScript are as follows:

`:Math.abs`(): Returns the absolute value of the input argument.

`:Math.round`(): Rounds the value of the input argument.

`:Math.random`(): Returns a random number between 0 (inclusive) and 1 (exclusive).

`:Math.max`(): Returns the largest number among the input arguments.

`:Math.min`(): Returns the smallest number among the input arguments.


---

**Page 221**

In designing online stores, JavaScript’s mathematical functions play a vital role, because managing main operations such as calculating the final price after applying a discount, totaling the items in the shopping cart, and determining shipping costs requires precise use of these functions. To become familiar with how to call and how these functions work, create a file named `shopping-cart.html` and write the script below in it.

Then examine and analyze the results obtained in class.

![Book image](../images/p227-01.png)

![Book image](../images/p227-02.png)


---

**Page 222**

Using string functions in JavaScript

### Workshop

JavaScript’s string functions and properties are essential tools for processing and managing text that make it possible to format and change strings with high precision and efficiency. These methods make it possible to validate user input data and optimize text for display or sending to the server. Some of JavaScript’s string functions are as follows:

`:toUpperCase`(): Converts the letters of the input string to uppercase.

`:indexOf`(): Returns the index of the position of the character or string inside the parentheses in the main string.

`:substring`(): Returns a substring from the main string. The inputs of this function are the start and end indices of the substring.

`:split`(): Splits the string based on the separator inside the parentheses (such as a comma) and returns an array of strings.

`:replace`(): Receives two strings as input and places the second string (/) in place of the first string (-) in the main string. This function performs the string replacement at the first position where the desired string (-) is found.

`:startsWith`(): Checks for the presence of a letter or string at the beginning of a string variable.

The `string` object has a property named `length` that determines the length of a string. Based on this, the statement below displays the value 11.

```
;(str1.length)console.log
```

Create a file named `user-info.html` and write the script below to become familiar with how string functions work:

![Book image](../images/p228-01.png)

![Book image](../images/p228-02.png)


---

**Page 223**

### Learn more

Using array functions in JavaScript: JavaScript’s array functions are suitable tools for managing, searching, filtering, and transforming structured data. With these methods you can perform various operations such as sorting (`sort`), filtering (`filter`), and extracting information from lists simply and without needing to write complex loops. Some array functions are as follows:

`:push`(): Is used to add one or more elements to the end of an array.

`:slice`(): Is used to extract part of an array and create a new array.

`:filter`(): Creates a new array by filtering the elements of the main array based on a specific condition.

`:sort`(): Sorts the elements of the array.

The `length` property returns the number of elements in the array. For example, the expression `names.length` returns the number 6.

Create a file named `customer-list.html` and write the script below to become familiar with how array functions work. Examine and analyze the script results in class.

![Book image](../images/p229-01.png)

![Book image](../images/p229-02.png)


---

**Page 224**

### Learn more

Using JavaScript’s input and output functions and statements: Input and output (`I/O`) functions in JavaScript are the communication bridge between the program and the world outside it and make it possible to create an interactive and dynamic experience for users. In the browser environment, these functions are used to receive input from the user, display a message box, display data in the console, and receive user confirmation.

To examine how input and output functions work, create a new file named `user-interaction.html` and write the code below in the `body` section.

![Book image](../images/p230-01.png)

Save the file and observe the result in the browser.

![Book image](../images/p230-06.png)

`:console.log`(): Is responsible for displaying values in the browser console.

`:prompt`(): Displays a dialog box to receive data from the user. The received value is sent to the call site.

`:alert`(): Displays a warning window with a message and an `.OK` button. `:confrim`(): Displays a confirmation window that includes an `OK` button and `.Cancel`. The return value of the function is `True` or

```
False است.
```

![Book image](../images/p230-02.png)

![Book image](../images/p230-03.png)

The `alert` and `prompt` windows

![Book image](../images/p230-05.png)

![Book image](../images/p230-04.png)

The `confrim` window

`:document.write`(): Writing directly to the web page (using this method is not recommended in modern programming).
