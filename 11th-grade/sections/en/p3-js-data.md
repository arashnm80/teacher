**Page 206**

Arrays (`Arrays`) Array variables can hold several elements with different data types. When you define a variable of array type, the array values are written inside square brackets. An array can have elements of the same data type or of different types.

### Example

In the following example, three arrays with string, numeric, and mixed values are defined:

```
;]"let cars = ["Opel", "Saab", "Volvo", "BMW", "Hyundai
;]let numbers = [1, 20 , 5 , 25 , 1000 , 10 , 1 , 5
;]let data = [123, "Opel", false , 12 , 35
```

Each of the array elements has an index. Array element indexes start at zero, so if an array has 5 elements, the index of the first element is zero and the index of the last element is 4. To access array elements, the element indexes are used. The figure below shows a view of the elements of the `cars` array and their values:

```
Hyundai
```

`Volvo`

`Saab`

`Opel`Element values

`BMW`

0Element indexes

4

3

2

1

**Figure 9**

To access the first element of the array, the expression `]cars[0` is used, and to access the fourth element, the expression `]cars[4` is used.

### Example

On the second line of the following example, the value of the third element of the `cars` array is displayed in the console, and on the third line the entire array is displayed.

![Book image](../images/p212-02.png)

![Book image](../images/p212-01.png)

If the index of an array element is not specified, all elements of the array are printed on the page.

### Note

When you define an array with the keyword `const`, you can still change the elements of the existing array; but the array variable cannot be assigned to another array. For example, writing the following expression causes an error:

```
]"cars = ["Tara", "Shahin", "Dena"," Lamari Eama
```


---

**Page 207**

Creating an array and printing values

### Workshop

1 Create a new file named `workshop4.html` and inside it define an array named `colors` with the values `yellow`, `blue`, `red`, `green`, and `orange`. After checking that the program is correct, write the statements in the blanks.

2 Write a statement that displays the element `blue` in the browser console.

……………………………

3 Write a statement that prints all elements of the `colors` array at once.

……………………………

### Learn more

Multidimensional arrays In the previous section, how to create a one-dimensional array and access its elements was introduced. JavaScript also makes it possible to define a multidimensional array. A multidimensional array is created when each of the array’s elements contains another array. The most common type of multidimensional array is a two-dimensional array, which can be used as a matrix.

In the following example, a two-dimensional array named `users` is defined:

![Book image](../images/p213-02.png)

![Book image](../images/p213-01.png)

To access the first element of the first array (`Arash`), the expression `]users[0][0` must be used, and to access the fourth element of the second array (`Doctor`), the expression `].users[1][3` The image on the right shows the indexes of the elements of the two-dimensional array `users`.

Working with two-dimensional arrays In the `workshop4.html` file, write the contents of the `users` array (the previous example).

1 Enter the following statements after introducing the array and check the output of each statement in the browser console. Note the result next to each statement.

……………………………………… ;(`users`)`console.log` ……………………………………… ;)`]users[1`(`console.log` ……………………………………… ;)`]users[2][3`(`console.log`

2 Write a statement that causes the element `Rose` to be displayed.

………………………………….


---

**Page 208**

Objects in JavaScript An object (`Object`) is a data structure used to store a set of related data as key: value pairs; in an object data structure, a set of keys (`keys`) point to their corresponding values (`values`). Objects are used to store and organize the data and behaviors of an entity. which has a structure similar to a dictionary in Python.

### Example

In the following example, the object `person` has four properties—first name, last name, age, and eye color—each of which has a specific value:

![Book image](../images/p214-01.png)

When defining an object, using spaces and creating a new line does not matter; therefore the object `person` can also be defined as follows:

![Book image](../images/p214-02.png)

Accessing the value of an object’s properties is possible with a dot or with square brackets. Both of the following statements display the value of the `firstName` property in the object `person`:

![Book image](../images/p214-03.png)

### Learn more

In addition to properties, an object has behaviors that are defined as methods. Methods are usually defined at the end of the object’s key-value pairs.

New method

Old method

```
{)(methodName:function
{)(methodName
```

// Statements that the method performs

// Statements that the method performs

}

}

On lines 13 through 15 of the code on the next page, the method `displayInfo`() is defined for the object `person`, and on line 17 it is called.


---

**Page 209**

### Learn more

![Book image](../images/p215-03.png)

In the definition above, the keyword `this` refers to the current object (`person`) and is used to access the properties of the current object. This method returns the information of the object `person` to the place where it is called.

To call an object’s method, first the object name (`Person`) and then the method name (`displayInfo`) are written together with the () marks.

The string that the method `displayInfo`() returns (`return`) to the place where it is called must be placed inside a `backtick` mark. This mark is at the top corner of the keyboard, below the `esc` key.

Creating an object in JavaScript

### Workshop

1 Create a new file named `workshop5.html`.

2 Create an object named `book` with the properties `title`, `author`, and `year` and the values `"JavaScript"`, `"Douglas` `Crockford"`, and 2008.

……………………………………………………………

3 Write a statement that prints the value of the `author` property in the object `book`. ..………………....

### Learn more

Combining objects and arrays JavaScript makes it possible to combine objects and arrays. A JavaScript programmer can create an array of objects or an object that contains an array.

### Example

The following example creates an array of objects:

![Book image](../images/p215-02.png)

![Book image](../images/p215-01.png)


---

**Page 210**

### Example

In the following example, the object `school` contains the array `students`:

![Book image](../images/p216-01.png)

![Book image](../images/p216-02.png)

### Activity

Working with objects and arrays In the `workshop5.html` file, define the array `students` and `school` according to the example above and check the results in the browser console. Write a statement that displays Ms. `mona`’s name and age in the console.

…………………………………………………

Conditional and loop structures in JavaScript Conditional and loop structures are essential parts of programming languages, including JavaScript. Conditional structures control the program’s logic based on specific conditions, and loop structures perform particular operations repeatedly. This section introduces these structures.

Conditional `If` statements A conditional statement makes it possible to run a set of statements when a particular condition is met.

Depending on what the program needs, the `if` statement can be written in three forms. Table 20 shows the general form of the `if` conditional structure in three different cases.

Table 20 Types of `if` conditional structures

```
else-if
ifif-else ساده
{ (condition1) if
statement1
{(condition) if
{(condition) if
{ (condition2) else if }
Statement1
statements
statement2
{else}
```

}

```
{ else }
Statement2
statement3
```

}

}


---
