<!-- page 225 -->

> **Curiosity**
>
> Research why using the functions `prompt()` and `confirm()` for input operations can disturb the user experience.

### Classes and objects

In programming languages, a class means a pattern for creating objects. A class contains a set of properties and methods. An object that is defined from a class will have the properties and methods defined in that class.

> **Learn more**
>
> In the following example a class titled Person is created that contains the properties **name** and **age**:
>
> ![Book image](../images/p231-01.png)
>
> - **The constructor method** is used to define and give values to the properties of an object. When a new object is created from a class, the constructor method is called automatically and assigns the initial values to the properties of that object. In the example above the constructor method accepts the two parameters name and age and assigns them to the matching properties in the object.
>
> - The class person has a method named **greet** that shows a message in the browser console.
>
> - The variable person1 is an object of the class person whose property values are amin and 47. This example shows that to create an object from a class the keyword **new** must be used. Considering that the class person has a method named greet, the object person1 can use this method too. The method greet will show the phrase "My name is amin and I am 47 years old" in the console.
>
> **Creating a class and an object**
>
> Create a new file named `object.html` and in it create a new class named Car with the properties `auto_maker`, model and year.
>
> Write a method named `print_Details` to print the properties of the car. The printing form must be as follows: Auto maker: Toyota, Model: Camry, Year: 2020

<!-- page 226 -->

> **Learn more (continued)**
>
> - Create an object with the values Toyota, Camry, 2020 and use the method `print_details` for the new object.
>
> ![Book image](../images/p232-01.png)

## Reaching DOM elements

To do various operations on the elements of a page, JavaScript needs to reach those elements. That is why JavaScript has methods for reaching elements. For example, to reach an element with the id demo, the method getElementById is used as follows:

In this script the new value of the element para is given with the property textContent.

There are different ways to select and reach each of the page's elements, which are mentioned in this section.

**Selecting by ID**: the elements of the page are selected by their identifier (id).

**Selecting by class**: a set of elements with a given class name are selected.

**Selecting by tag name**: a set of elements with the same tag name are selected.

![Figure 12](../images/p232-02.png)
*Figure 12*

![Figure 13](../images/p232-03.png)
*Figure 13*

<!-- page 227 -->

> **Curiosity**
>
> To read about the other methods of reaching elements, search the phrase "how to get elements by JavaScript" on Google and open the site `w3schools.com` from the list of results.

Next, exercises are given for working on different elements of the page with JavaScript.

> **Workshop**
>
> **Managing page elements with JavaScript**
>
> **Reaching the content of elements, changing the content and the style of elements**: write a script that changes the content and style of a button and a text element with JavaScript. These changes must happen when the button is clicked.
>
> - Create a file named `product.html` and enter the following code in the `<body>` section:
>
> ![Book image](../images/p233-01.png)
>
> ![Book image](../images/p233-02.png)
>
> ![Book image](../images/p233-03.png)
>
> In lines 6 to 13 of the script above a function named `change()` is defined that reaches the elements addToCart and para and then changes their content and style. The function `change()` is called when the button is clicked.
>
> In lines 7 and 8 the paragraph and the button elements are reached. In lines 9 and 10 the content of the paragraph and button elements is changed with the properties innerHTML and textContent. In lines 11 and 12 the style of the elements is changed with the style property. Save the file and check the result in the browser.

> **Learn more**
>
> **Reaching elements and changing their properties**: write a script that changes the src property of an image when the mouse is placed over it.

<!-- page 228 -->

> **Learn more (continued)**
>
> - In the file `products.html` add the picture of a product to the `<body>` section. Then use the following script to change the value of the src property of the image.
>
> ![Book image](../images/p234-01.png)
>
> Save the file and check the result in the browser.
>
> When the mouse pointer is moved over the image, the onmouseover event is activated and as a result the function `changeImage()` is called to change the image. When the mouse moves away from the image, the onmouseleave event is activated and so the function `resetImage()` is called. This function brings back the original image.
>
> ![Book image](../images/p234-02.png)
>
> In both functions above, the method `setAttribute()` is used to change the image.
>
> ![Book image](../images/p234-03.png)
>
> **Adding and removing elements with JavaScript**: write a script that, when a button titled Consultation is clicked, adds a panel to the page to guide the user and closes it after a few seconds.
>
> - Create a new file named `open-panel.html` and write the script in it as in the figure opposite.

<!-- page 229 -->

> **Learn more (continued)**
>
> Add the style of the elements to the `<head>` section. Then save the file and see the result in the browser.
>
> When the button "Consultation with a sales expert" is clicked, the function `openPanel()` is called. This function is written in lines 3 to 12.
>
> - In line 4 a new div element is created with the method createElement.
>
> - In line 5 the content of the element is set with the property InnerHTML.
>
> - The new element needs a style. This style is specified by the class consultpanel.
>
> - In line 6 the class name of the new element is set.
>
> - In line 7 the new element is added to the page with the method appendChild.
>
> - The consultation panel (the div element) is hidden by default. In line 8 the display state of the panel is changed to block.
>
> - In line 9 the method setTimeout is used to set the time for removing the consultation panel.
>
> - In line 9 the consultation panel is removed after 5 seconds by the method remove.
>
> **Reaching the form information and validating the user's data**: write a simple script to validate the user's input data. In this validation, check that the text fields are filled, so that if a text field is empty, a warning message is shown.
>
> - Create a file named `sign-in.html` and enter the code of the following figure in it:
>
> ![Book image](../images/p235-01.png)
>
> ![Book image](../images/p235-02.png)
>
> **This form contains three fields to receive the username, the password and the email**.

<!-- page 230 -->

> **Learn more (continued)**
>
> To validate the form use the script of the following figure. This script contains the function `validateForm()`, which checks the input value of the text fields. This function is called in the onsubmit event of the form on the previous page.
>
> ![Book image](../images/p236-01.png)
>
> The function `validateForm()` receives the username and password in lines 2 and 3 and puts their values in the two variables username and password. In lines 4 to 7 it is checked whether username is empty; if this variable is empty, a warning message appears and the statement return false prevents the form's content from being sent to the server. Similarly in lines 8 to 11 it is checked whether the variable password is empty. If the conditions of the ifs in lines 4 and 8 do not hold, the statement of line 12 runs and the form's information is sent to the server.
>
> Next, check the length of the username and the password; so that if the length of either of these two fields is less than 6 characters, a warning message is shown. For this write the following condition after line 11.
>
> ![Book image](../images/p236-03.png)
>
> ![Book image](../images/p236-02.png)

> **Note**
>
> The DOM is the foundation of all interactive websites; mastering it means stepping into the professional world of web design.
