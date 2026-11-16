<!-- page 219 -->

**The principles of defining a function in JavaScript are as follows**:

- In defining a function, first the key phrase function and then its name are written.

- The name of a function must start with a lowercase letter and each new word must start with a capital letter.

- The input parameters of the function are specified inside the parentheses.

- The number of parameters can be zero, one or more. The set of statements of the function is written inside braces.

- The output of the function is usually returned to the place of the call by the return statement.

- The statements inside a function run when the function is called.

- To call a function, the name of the function with the input arguments must be used. The general form of calling a function is as follows:

```
functionName(Arguments)
```

> **Example**
>
> In the following example a function named calculateCartTotal is created with three input parameters price1, price2, price3. The function calculateCartTotal calculates the sum of the values of these three parameters and stores it in the variable total. The return statement gives the value of the variable total back to the place of the call.
>
> ![Book image](../images/p225-01.png)
>
> ![Book image](../images/p225-02.png)

> **Note**
>
> Parameters are variables used when defining a function. In the example above the variables price1, price2, price3 are the input parameters of the function. Arguments are the values sent to the function when it is called. In other words, arguments are values that are assigned to the parameters of the function.

<!-- page 220 -->

> **Workshop**
>
> **Creating a function and calling it**
>
> Create a new file named `workshop8.html` and write the function calculateCartTotal in it. Then call the function with input arguments of your choice.
>
> A function does not necessarily have a return value. A function can be written with the aim of running a set of instructions without returning a value to the place of the call. In that case there is no need to use the return statement. In the following example the function showCartTotal receives three values as input parameters, calculates their sum and shows the result in the browser console; but it returns no value to the place of the call.
>
> ![Book image](../images/p226-01.png)

### JavaScript's Built-in Functions

JavaScript has a set of ready-made functions used for different operations. JavaScript's ready-made functions let programmers manage data easily and implement complex tasks simply. These functions include mathematical, string, array, object, input-output and date and time functions, which are introduced in this section.

> **Workshop**
>
> **Using JavaScript's mathematical functions**
>
> JavaScript's mathematical functions, which are organised inside the Math object, are a set of powerful and efficient tools for doing complex mathematical calculations. The mathematical functions can be reached with the dot form `Math.functionName()`, and using them not only makes the coding shorter and more readable, but also prevents possible errors in implementing algorithms by hand and creates more optimal performance in applications. Some commonly used mathematical functions in JavaScript are as follows:
>
> `Math.abs()`: returns the absolute value of the input argument.
>
> `Math.round()`: rounds the value of the input argument.
>
> `Math.random()`: returns a random number from 0 (included) up to 1 (not included).
>
> `Math.max()`: returns the largest number among the input arguments.
>
> `Math.min()`: returns the smallest number among the input arguments.

<!-- page 221 -->

> **Workshop (continued)**
>
> In designing online shops, JavaScript's mathematical functions play a vital role, because managing the main operations, such as calculating the final price after applying a discount, totalling the items of the cart and deciding the shipping cost, needs the exact use of these functions. To get to know how these functions are called and how they work, create a file named `shopping-cart.html` and write the following script in it. Then check and analyse the results you get in class.
>
> ![Book image](../images/p227-01.png)

<!-- page 222 -->

> **Workshop**
>
> **Using string functions in JavaScript**
>
> JavaScript's string functions and properties are essential tools for processing and managing text, which make formatting and changing strings possible with high accuracy and efficiency. These methods make it possible to validate the users' input data and to optimise text for display or sending to the server. Some of JavaScript's string functions are as follows:
>
> `toUpperCase()`: turns the letters of the input string into capital letters.
>
> `indexOf()`: returns the index of the position of the character or string inside the parentheses in the main string.
>
> `substring()`: returns a substring of the main string. The inputs of this function are the starting and ending index of the substring.
>
> `split()`: splits the string based on the separator inside the parentheses (such as a comma) and returns an array of strings.
>
> `replace()`: takes two strings as input and puts the second string (/) in place of the first string (-) in the main string. This function does the replacement at the first position where the wanted string (-) is found. `startsWith()`: checks for the existence of a letter or string at the start of a string variable.
>
> The string object has a property named **length**, which gives the length of a string. Based on this, the following statement shows the value 11.
>
> ```
> console.log(str1.length);
> ```
>
> Create a file named `user-info.html` and write the following script to get to know how the **string functions** work:
>
> ![Book image](../images/p228-01.png)

<!-- page 223 -->

> **Learn more**
>
> **Using array functions in JavaScript**
>
> JavaScript's array functions are suitable tools for managing, searching, filtering and converting structured data. With the help of these methods various operations such as sorting (sort), filtering (filter) and extracting information from lists can be done easily without needing to write complex loops. Some of the array functions are as follows:
>
> `push()`: used to add one or more elements to the end of an array.
>
> `slice()`: used to extract a part of an array and create a new array.
>
> `filter()`: creates a new array by filtering the elements of the main array based on a certain condition. `sort()`: sorts the elements of the array.
>
> The length property returns the number of elements in the array. For example the expression `names.length` returns the number 6.
>
> Create a file named `customer-list.html` and write the following script to get to know how the array functions work. Check and analyse the results of the script in class.
>
> ![Book image](../images/p229-01.png)
>
> ![Book image](../images/p229-02.png)

<!-- page 224 -->

> **Learn more**
>
> **Using JavaScript's input and output functions and statements**
>
> Input and output (`I/O`) functions in JavaScript are the bridge between the program and the world outside it, and make an interactive and dynamic experience possible for users. In the browser environment, these functions are used to receive input from the user, show a message box, show data in the console and receive the user's confirmation.
>
> To check how the input and output functions work, create a new file named `user-interaction.html` and write the following code in the body section.
>
> ![Book image](../images/p230-01.png)
>
> Save the file and see the result in the browser.
>
> ![Book image](../images/p230-05.png)
>
> **`console.log()`**: responsible for showing values in the browser console.
>
> **`prompt()`**: shows a dialog box to receive data from the user. The value received is sent to the place of the call.
>
> **`alert()`**: shows a warning window with a message and an OK button.
>
> **`confirm()`**: shows a confirmation window with the buttons OK and Cancel. The returned value of the function is True or False.
>
> ![Book image](../images/p230-02.png)
>
> ![Book image](../images/p230-04.png)
>
> ![Book image](../images/p230-03.png)
>
> **`document.write()`**: writing directly into the web page (using this method is not recommended in modern programming).
