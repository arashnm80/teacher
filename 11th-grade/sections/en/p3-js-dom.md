**Page 225**

### Try this

Research why using the `prompt`() and `confirm`() functions for input operations can disrupt the user experience.

Classes and objects: In programming languages, a class means a pattern for creating objects. A class contains a set of properties and methods. An object that is defined from a class will have the properties and methods defined in that class.

### Learn more

In the example below, a class titled `Person` has been created that contains the properties `name` and `age`:

![Book image](../images/p231-01.png)

![Book image](../images/p231-02.png)

The `constructor` method is used to define and initialize the properties of an object. When a new object is created from a class, the `constructor` method is called automatically and assigns the initial values to that object’s properties. In the example above, the `constructor` method accepts two parameters `name` and `age` and assigns them to the corresponding properties in the object.

The `person` class has a method named `greet` that displays a message in the browser console.

The variable `person1` is an object of the `person` class type whose property values are `amin` and 47. This example shows that to create an object from a class you must use the keyword `new`. Given that the `person` class has a method named `greet`, the object `person1` can also use this method. The `greet` method will display the phrase `"My` `name` `is` `amin` `and` `I` `am` 47 `years` `old"` in the console.

Creating a class and an object: Create a new file named `object.html` and inside it create a new class named `Car` with the properties

```
auto_maker، model وyear ایجاد کنید.
```

Write a method named `print_Details` to print the car’s properties. The print format should be as follows:

```
Auto maker: Toyota , Model: Camry , Year: 2020
```


---

**Page 226**

Create an object with the values `Toyota`, `Camry`, 2020 and use the `print_details` method for the new object.

![Book image](../images/p232-01.png)

![Book image](../images/p232-02.png)

Accessing `DOM` elements: To perform various operations on page elements, JavaScript needs access to those elements. For this reason, JavaScript has methods for accessing elements. For example, to access an element with the identifier `demo`, the `getElementById` method is used as follows:

In this script, the new value of the `para` element is specified by the `textContent` property.

There are various methods for selecting and accessing each of the page elements, which are referred to in this section.

Selection based on `ID:` Page elements are selected based on their identifier (`id`).

Selection based on class: A set of elements with a specified class name is selected.

Selection based on tag name: A set of elements with the same tag name is selected.

![Figure 12](../images/p232-03.png)

**Figure 12**

![Figure 13](../images/p232-04.png)

**Figure 13**


---

**Page 227**

### Try this

To study other methods for accessing elements, search for the phrase «`how` `to` `get` `elements` `by` `JavaScript`» in Google and from the results list open the site `w3schools.com`.

In the following, exercises are presented for working on various page elements with JavaScript.

Managing page elements with JavaScript

### Workshop

Accessing element content, changing content and element style: Write a script that changes the content and style of a button and a text element with JavaScript. These changes should occur when the button is clicked.

Create a file named `product.html` and enter the code below in the `<body>` section:

![Book image](../images/p233-01.png)

![Book image](../images/p233-03.png)

![Book image](../images/p233-02.png)

In lines 6 through 13 of the script above, a function named `change`() is defined that accesses the elements `addToCart` and `para` and then changes their content and style. The function `change`() is called when the button is clicked.

In lines 7 and 8, access to the paragraph and button elements is performed. In lines 9 and 10, the content of the paragraph and button elements is changed using the `innerHTML` and `textContent` properties. In lines 11 and 12, the style of the elements is changed using the `style` property. Save the file and check the result in the browser.

### Learn more

Accessing elements and changing their attributes: Write a script that changes the `src` attribute of an image when the mouse is placed over it.


---

**Page 228**

In the file `products.html`, add a product image to the `<body>` section. Then use the script below to change the value of the image’s `src` attribute.

![Book image](../images/p234-01.png)

Save the file and check the result in the browser.

When the mouse pointer is moved onto the image, the `onmouseover` event is activated and as a result the function `changeImage`() is called to change the image. When the mouse moves away from the image, the `onmouseleave` event is activated and therefore the function `resetImage`() is called. This function restores the original image.

![Book image](../images/p234-02.png)

![Book image](../images/p234-03.png)

In both functions above, the `setAttribute`() method is used to change the image.

![Book image](../images/p234-04.png)

Adding and removing elements with JavaScript:

Write a script that, when a button titled Consultation is clicked, adds a panel to the page to guide the user and closes it after a few seconds.

Create a new file named `open-panel.html` and write the script inside it according to the figure opposite.


---

**Page 229**

Add the element styles to the `<head>` section. Then save the file and observe the result in the browser.

When the button “Consultation with a sales expert” is clicked, the function `openPanel`() is called. This function is written in lines 3 through 12.

In line 4, a new `div` element is created by the `createElement` method.

In line 5, the element’s content is set by the `InnerHTML` property.

The new element needs a style to be set. This style is specified by the class `consultpanel`.

In line 6, the class name of the new element is set.

In line 7, the new element is added to the page by the `appendChild` method.

The consultation panel (the `div` element) is hidden by default. In line 8, the panel’s display status is changed to `block`.

In line 9, the `setTimeout` method is used to set the time for removing the consultation panel.

In line 9, the consultation panel is removed after 5 seconds by the `remove` method.

Accessing form information and validating user data: Write a simple script to validate user input data. In this validation, check that the text fields are filled so that if a text field is empty, a warning message is displayed.

Create a file named `sign-in.html` and enter the code from the figure below into it:

![Book image](../images/p235-01.png)

![Book image](../images/p235-02.png)

This form contains three fields for receiving a username, a password, and an email.


---

**Page 230**

To validate the form, use the script from the figure below. This script contains the function `validateForm`(), which checks the input values of the text fields. This function is called in the `onsubmit` event of the form on the previous page.

![Book image](../images/p236-01.png)

![Book image](../images/p236-02.png)

The function `validateForm`() receives the username and password in lines 2 and 3 and places their values in the two variables `username` and `password`. In lines 4 through 7, whether `username` is empty is checked; if this variable is empty, a warning message appears and the statement `return` `false` prevents the form content from being sent to the server. Similarly, in lines 8 through 11, whether the variable `password` is empty is checked. If the conditions of the `if` statements in lines 4 and 8 are not true, the statement in line 12 is executed and the form information is sent to the server.

Next, check the length of the username and password so that if the length of either of these two fields is less than 6 characters, a warning message is displayed. To do this, write the condition below after line 11.

![Book image](../images/p236-03.png)

![Book image](../images/p236-05.png)

![Book image](../images/p236-04.png)

### Note

`DOM` is the foundation of all interactive websites; mastering it means taking a step into the professional world of web design.
