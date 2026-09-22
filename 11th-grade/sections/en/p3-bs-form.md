**Page 180**

Bootstrap has a set of ready-made classes for laying out various forms. With these classes you can create responsive and attractive forms quickly and with little need for coding. Table 12 contains some form classes in Bootstrap 5.

Table 12 Form classes

Class name

### Use

```
form-control
```

Sets the style of input fields such as `input`, `textarea`, and `select`

`form-label` Sets the style of form labels `form-check` Styles checkboxes and radio buttons

```
form-check-label
```

This class is used for the text next to a checkbox or radio button.

`form-check-input` For styling a checkbox and radio button

```
form-text
```

This class is used to show helpful text under a form field.

### Learn more

Designing the sign-up form. In this workshop you will design a sign-up form like the one opposite using Bootstrap classes.

![Book image](../images/p186-02.png)

1 Create a web page named `signup-form.html` and write the initial `HTML` document code in it. Then add the `charset`, `viewport`, and `title` meta tags and the Bootstrap `CDN` link in the `<head>` section of the page. Also set the page direction to `rtl`.

![Book image](../images/p186-01.png)


---

**Page 181**

2 On the `signup-form.html` page only one form is displayed. This form should appear in the horizontal and vertical center of the page. Therefore set the properties of the `body` tag as shown below:

![Book image](../images/p187-01.png)

`vh` is a unit of measurement in `CSS` that stands for `Viewport` `Height`. The word `viewport` refers to the part of the page that is in the user’s view. `1vh` equals 1% of the `viewport` height. Therefore, `height:100vh` means that the height of the `<body>` element should equal 100% of the `viewport` height.

In other words, this element should occupy the full height of the page.

Using the `d-flex` and `align-items-center` classes makes the content of the `body` section sit in the middle of the page.

3 Inside the `body` element create a container element with the content shown below:

![Book image](../images/p187-02.png)

4 The width of the form should be controlled on different devices. For this it is better to use the `grid` classes so that, depending on the device size, the width of the form’s container element changes. In the code above a container element with the `row` class has been created, and inside it there is only one column containing the form and its title. Because the form is inside a `grid` column, the form width will change depending on the column width.

The `justify-content-center` class centers the content of the container element on the page.

The `col-10`, `col-md-6`, and `col-lg-5` classes set the width of the `grid` column on mobile, tablet, and desktop devices.


---

**Page 182**

5 Add the form content according to the code in the figure below in the place set aside in the code above:

![Book image](../images/p188-01.png)

Save the file and check the result in the browser.

6 Change the color of the form title text to blue and the color of the label text to gray. Do this with Bootstrap classes.

7 Remove the underline from the “Sign in” link at the bottom of the page with a Bootstrap class.

### Learn more

`Modal`

A modal is a user interface that appears as a floating dialog box on top of the page and requires the user to interact with it before returning to the web page. This element is usually used to show extra information, get user confirmation, forms, or other interactions with the user.

Pressing the `Esc` key, clicking the `close` button, or clicking an area outside the modal window closes the dialog box.

A modal window has three sections: `header`, `body`, and `footer`. These sections are created with the `modal-header`, `modal-body`, and `modal-footer` classes. All three sections sit inside a container element with the `modal-content` class.

A modal depends on JavaScript, so adding the Bootstrap JavaScript file before `</body>` is required.

To show the dialog box you need an activating element such as a button.


---

**Page 183**

![Book image](../images/p189-03.png)

Complete structure of a modal in `Bootstrap`

Showing a message that a product was added to the shopping cart with a `Modal`

### Workshop

In previous workshops you designed the product information page (`product-details.html`). On some shopping sites, when the user clicks the “Add to cart” button, a message with the content “The selected product was added to the shopping cart” is displayed. In this workshop you will change the `product-details.html` page in the same way.

Open the `product-details.html` file and change the Add to cart button according to the code in the figure below:

![Book image](../images/p189-01.png)

When you click this button, the dialog box (modal) with the id `addTocartMsg` appears.

`btn:` Assigns a Bootstrap button style to the `<button>` element.

`"data-bs-toggle="modal:` Specifies that this button is for opening a modal.

`"data-bs-target="#addToCartMsg:` Specifies which modal should open.

Add the modal code to the page after the `</button>` tag:

![Book image](../images/p189-02.png)


---

**Page 184**

![Book image](../images/p190-01.png)

`tabindex` specifies the order in which focus moves among elements when the `Tab` key is used.

The expression `tabindex=-1` means that the modal cannot receive focus with the `Tab` key.

`btn-close` sets the style of the close button in the modal window as an × mark.

`data-bs-dismiss="modal":` Specifies the behavior of the `close` button so that when the user clicks the button, the modal closes.

By default the `close` button at the top of the modal window appears on the right side of the window. That is why the `d-flex`, `justify-content-end`, and `ms-0` classes are used to set the position of the button.

After clicking the “View cart” button, the `shopping-cart.html` page should open. For this, use the button’s `onclick` attribute and set its value to a JavaScript statement as shown below:

![Book image](../images/p190-02.png)

```
کروسل (Carousel)
```

A carousel is a JavaScript-based tool used to create a set of slides or a horizontal image gallery. A carousel lets you show several pieces of content or images in a limited space so that users can see the next items with control buttons or by swiping (`swipe`).

On a shopping site, carousels or sliders let you show a set of products or promotional content in a rotating way. Using a carousel provides a better user experience.

To create a Bootstrap carousel, the `carousel` class and its related classes are used.

Table 13 describes the class names and their uses:


---
