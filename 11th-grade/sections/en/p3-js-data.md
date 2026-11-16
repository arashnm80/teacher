<!-- page 206 -->

### Arrays

Array variables can hold several elements with different data types. When defining a variable of the array type, the values of the array are written inside square brackets. An array can have elements of the same or different data types.

> **Example**
>
> In the following example three arrays with string, numeric and mixed values are defined:
>
> ```
> let cars = ["Opel", "Saab", "Volvo", "BMW", "Hyundai"];
> let numbers = [1, 20 , 5 , 25 , 1000 , 10 , 1 , 5];
> let data = [123, "Opel", false , 12 , 35];
> ```

Each element of an array has an index. The index of the array elements starts from zero, so if an array has 5 elements, the index of the first element is zero and the index of the last element is 4. To reach the elements of the array, the index of the elements is used. The following figure shows the elements of the array cars and their values:

| Hyundai | BMW | Volvo | Saab | Opel | The value of the elements |
| --- | --- | --- | --- | --- | --- |
| 4 | 3 | 2 | 1 | 0 | **The index of the elements** |

To reach the first element of the array the expression `cars[0]` is used, and to reach the fourth element the expression `cars[4]` is used.

> **Example**
>
> In the second line of the following example the value of the third element of the array cars, and in the third line the whole array, is shown in the console.
>
> ![Figure 9](../images/p212-01.png)
> *Figure 9*
>
> If the index of an array element is not specified, all the elements of the array are printed on the page.

> **Note**
>
> When an array is defined with the keyword const, it is possible to change the elements of the array, but the array variable cannot be assigned to another array. For example, writing the following expression gives an error: `cars = ["Tara", "Shahin", "Dena"," Lamari Eama"]`

<!-- page 207 -->

> **Workshop**
>
> **Creating an array and printing the values**
>
> 1. Create a new file named `workshop4.html` and in it define an array named colors with the values yellow, blue, red, green and orange. After checking the program is correct, write the statements in the blanks.
>
> 2. Write a statement that shows the element blue in the browser console.
>
> ……………………………
>
> 3. Write a statement that prints all the elements of the array colors at once.
>
> ……………………………

> **Learn more**
>
> **Multi-dimensional arrays**
>
> In the previous section, how to create a one-dimensional array and reach its elements was introduced. JavaScript also makes it possible to define a multi-dimensional array. A multi-dimensional array is created when each of the elements of the array holds another array. The most common type of multi-dimensional array is the two-dimensional array, which can be used as a matrix.
>
> In the following example a two-dimensional array named users is defined:
>
> ![Book image](../images/p213-02.png)
>
> ![Book image](../images/p213-01.png)
>
> To reach the first element of the first array (Arash) the expression `users[0][0]` must be used, and to reach the fourth element of the second array (Doctor) the expression `users[1][3]`. The picture on the right shows the indexes of the elements of the two-dimensional array users.
>
> **Working with two-dimensional arrays**
>
> In the file `workshop4.html` write the content of the array users (from the previous example).
>
> 1. Enter the following statements after introducing the array and check the output of each statement in the browser console. Note the result opposite each statement.
>
> ```
> console.log(users);               ………………………………………
> console.log(users[1]);             ………………………………………
> console.log(users[2][3]);           ………………………………………
> ```
>
> 2. Write a statement that makes the element Rose be shown.
>
> .…………………………………

<!-- page 208 -->

### Objects in JavaScript

An object is a data structure used to store a set of related data in the form of key: value pairs; in the object data structure, a set of keys point to their matching values. Objects are used to store and organise the data and behaviours of an entity. It has a structure similar to the dictionary in Python.

> **Example**
>
> In the following example the object person has four properties, first name, last name, age and eye colour, each of which has a specific value:
>
> ![Book image](../images/p214-01.png)
>
> When defining an object, spaces and new lines do not matter; so the object person can also be defined as follows:
>
> ![Book image](../images/p214-02.png)
>
> Reaching the value of the properties of an object is possible with the dot or with square brackets. Both of the following statements show the value of the property firstName in the object person:
>
> ![Book image](../images/p214-03.png)

> **Learn more**
>
> Besides properties, an object has behaviours that are defined as methods. Defining methods is usually done at the end of the key-value pairs of the object.
>
> The new way
>
> The old way
>
> ```
> methodName:function(){
>                                  methodName(){
> ```
>
> // the statements the method does
>
> // the statements the method does
>
> ```
>                                }
> }
> ```
>
> In lines 13 to 15 of the code on the next page the method `displayInfo()` is defined for the object person, and in line 17 it is called.

<!-- page 209 -->

> **Learn more**
>
> ![Book image](../images/p215-03.png)

In the definition above, the keyword **this** points to the current object (person) and is used to reach the properties of the current object. This method returns the information of the object person to the place of the call.

To call the method of an object, first the name of the object (Person) and then the name of the method (displayInfo) are written with the () signs.

The string that is returned by the method `displayInfo()` to the place of the call must be put inside the backtick sign. This sign is located at the top corner of the keyboard, under the esc key.

> **Workshop**
>
> **Creating an object in JavaScript**
>
> 1. Create a new file named `workshop5.html`.
>
> 2. Create an object named book with the properties title, author and year and the values "JavaScript", "Douglas Crockford" and 2008.
>
> ……………………………………………………………
>
> 3. Write a statement that prints the value of the property author in the object book. ..………………....

> **Learn more**
>
> **Combining objects and arrays**
>
> JavaScript makes it possible to combine objects and arrays. A JavaScript programmer can create an array of objects or an object that contains an array.

> **Example**
>
> The following example creates an array of objects:
>
> ![Book image](../images/p215-02.png)
>
> ![Book image](../images/p215-01.png)

<!-- page 210 -->

> **Example**
>
> In the following example the object school contains the array students:
>
> ![Book image](../images/p216-01.png)
>
> ![Book image](../images/p216-02.png)

> **Activity**
>
> **Working with objects and arrays**
>
> In the file `workshop5.html` define the arrays students and school as in the example above and check the results in the browser console
>
> Write a statement that shows the name and age of Ms. mona in the console.
>
> …………………………………………………

### Conditional structures and loops in JavaScript

Conditional structures and loops are basic parts of programming languages, including JavaScript. Conditional structures control the logic of the program based on certain conditions, and loop structures do certain operations repeatedly. This section introduces these structures.

### The If conditional statements

A conditional statement makes it possible to run a set of statements when a certain condition holds. Depending on the needs of the program, the if statement can be written in three forms. Table 20 shows the general form of the if conditional structure in three different cases.

*Table 20: Types of if conditional structures*

| `else-if` | `if-else` | A simple if |
| --- | --- | --- |
| `if (condition1) {`<br>statement1<br>`} else if (condition2) {`<br>statement2<br>`} else {`<br>statement3<br>`}` | `if (condition){`<br>Statement1<br>`}else{`<br>Statement2<br>`}` | `if (condition){`<br>statements<br>`}` |
