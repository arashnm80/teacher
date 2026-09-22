**Page 173**

Designing the navigation bar

### Workshop

In this workshop you will add a Bootstrap navigation bar with a collapse feature to the `index.html` page. Before you do this, delete the code related to `top-menu`, or place it completely inside <-- --!> marks so the browser does not interpret its content.

Correct operation of the navigation bar requires the `bootstrap.bundle.min.js` file. If this file is not present in the `<head>` section or before `</body>`, add it to the page according to the instructions for using a `CDN` on a web page; otherwise, when you click the hamburger button (☰), its content will not be displayed.

Replace the `top-menu` element with the code in the figure below:

![Book image](../images/p179-01.png)

The code above includes two elements: a “button” and a “collapsible area.” The `<button>` tag is used to create the button. Inside this tag there is a `<span>` element with the `navbar-toggler-icon` class that displays a three-line icon.

The list content is placed inside a container element with the id `navbarCollapse`. You are expected that when you click the menu button, the area containing the list opens. For this purpose the `data-bs-target` attribute with the value `#navbarCollapse` is used.

`"data-bs-target="#navbarCollapse` specifies the identifier (`ID`) of the menu that should open or close.

The `"data-bs-toggle="collapse` attribute makes the menu open and close when you click the button.

The color of the navigation bar is set by `bg-primary`. If you wish, you can use other background color classes.

The `collapse` class makes the content inside the `div` collapsed, and it opens/closes with the `toggle` button. (This class enables the ability to open and close the content.) The `navbar-collapse` class makes the links stack vertically (one under another) when the menu opens, and makes the menu’s inner space (`padding`) standard and coordinated with the other navigation components. If you use only `collapse`, the menu links will look untidy.


---

**Page 174**

Now it is time to write the list of menu items. Add the code in the figure below in the place set aside in the previous code:

![Book image](../images/p180-01.png)

On the parent element of the list (`ul`) the `navbar-nav` class is used, and on the list items the `.nav-item` class is used. By default the navigation menu options appear on the right side of the page. The `mx-auto` class is used to set the left and right margin of the menu.

Save the file and check the result in the browser.

The `navbar-expand-lg` class makes the menu bar appear horizontally at widths above 992 pixels. Change the `lg` parameter to `md` and check the result of the change.

On shopping sites, the navigation menu is hidden in the mobile and tablet views. Add the `d-none` and `d-md-block` classes to the `nav` element and check the result in the mobile and tablet views.

### Try this

What effect does the `active` class, which is applied only to the first option, have on the appearance of that option?

The first option on most shopping sites is “Product categories,” which contains a list of product classifications. To create this option, add the code in the figure below before the first list item above (Customers club):

![Book image](../images/p180-02.png)

`nav-item:` Used for each of the menu options.


---

**Page 175**

`dropdown:` This class is used for the element that contains the submenu.

`nav-link:` Used to style the links in the navigation bar (`Navbar`) and displays the link according to the `Navbar` style.

`active:` This class makes one option look different (thicker) from the other options and means that an option is active.

`dropdown-toggle:` This class tells Bootstrap’s JavaScript that this element can open and close; it also adds a small arrow ▼ next to the menu option, which means it has a submenu.

`"data-bs-toggle="dropdown:` Used to enable the two-state behavior of the menu (open and close).

`dropdown-menu:` This class is usually used for a `<ul>` element and makes the list content appear as a hidden box under the menu option.

`dropdown-item:` Used to set the style of each option in the drop-down menu.

Remove the `active` class from the first option of the previous list (Customers club). Save the file.

You are expected to get the result below:

![Book image](../images/p181-01.png)

As stated, the `dropdown-toggle` class displays a downward arrow. If you wish you can remove it, but you need to enable showing the submenu on `hover` by adding the style below:

![Book image](../images/p181-02.png)

### Note

Because the `hover` event does not occur in the mobile view, this code works only in the desktop view.

Buttons. A button is one of the interactive elements of a page that lets the user perform an action with a click. Creating a button on a web page is possible with the three tags below:

```
button< 1>
input< 2>
```

`a<` 3>


---

**Page 176**

In Bootstrap there are various classes for styling buttons. These classes let you customize the appearance of buttons in terms of color, size, and other properties. To set the appearance of a button with Bootstrap classes, using the `btn` class is required. To choose the color and size of the button you can also add other button-related classes to the `btn` class.

These classes are summarized in Table 11:

Table 11 Button classes in Bootstrap

Class type

Class names

Color

```
btn-primary، btn-secondary، btn-danger، btn-light، btn-dark، btn-link و...
```

Button borders

```
btn-outline-primary، btn-outline-secondary و....
```

Button sizes `btn-sm`, `btn-lg` Disabled state `disabled`

### Example

In the example below, six buttons with different labels and classes have been created:

![Book image](../images/p182-01.png)

![Book image](../images/p182-02.png)

### Learn more

Layout of the product detail page. In this workshop you will design the product information page in three columns containing the product image, product features, and product price. On this page the `header` and `footer` sections are the same as in the `index.html` file; only the `main` section has different content. To speed up the design work, create a copy of the `index.html` file. To do this, open the `index.html` file in a text editor. From the `File` menu choose `Save` `As` and then type `product-details.html` as the page name.


---

**Page 177**

Clear the content of the `<main>` tag completely. Save the file and display the `product-details` page in the browser to make sure you have done this correctly. At this stage the `product-details` page should contain the banner bar at the top of the page, the logo bar, the navigation bar, and the footer.

Write the code in the figure below inside the `<main>` tag for the product page layout:

![Book image](../images/p183-01.png)

In this layout the `Grid` system is used. The column shares on devices 992 pixels and

larger are 4/12,

5/12,

and 3/12. At widths from 768 to 992 pixels each column’s share is 4/12,

and on

smaller devices the column contents stack on top of each other.

Define the width of the `product-information` element as shown below in the `styles.css` file:

![Book image](../images/p183-02.png)

Add the image of the book “Basic Technical Knowledge” to the first column as shown below:

![Book image](../images/p183-03.png)

So that the product image is centered in the column on all devices, add the `d-flex`, `justify-content-center`, and `align-items-center` classes to the first column after the `col-lg-4` class:

![Book image](../images/p183-04.png)

So that the image size is controlled on devices smaller than 768 pixels, add the style below to the `styles.css` file:

![Book image](../images/p183-05.png)


---

**Page 178**

Write the content of the second column as shown below:

The `fs-3` class sets the text size and the `text-sm-end` class sets the text alignment (on the right side of the column).

![Book image](../images/p184-01.png)

Set the style of the second column’s content as shown below:

![Book image](../images/p184-02.png)

In the mobile view, the content of the second column sticks to the right edge of the browser and does not look pleasant. So that the content has space from the right and sits in the middle of the column, the content of the second column is placed inside a `div` element with the `details-container` class. Set the properties of this element as shown below:

![Book image](../images/p184-03.png)

Enter the code written in the figure below into the third column:

![Book image](../images/p184-04.png)


---

**Page 179**

Write the style of the third column’s content as shown below:

![Book image](../images/p185-01.png)

You are expected that the result on devices 992 pixels and larger looks like the figure below:

![Book image](../images/p185-02.png)

### Activity

In the `index.html` file, link the product “Basic Technical Knowledge” to the `product-details.html` page.

Forms. Data-entry forms are tools for user interaction with the page and for collecting information. The appearance of entry forms plays a vital role in the user experience and the success of a website. Attractive and user-friendly forms increase user interaction and create a sense of trust and satisfaction. In contrast, messy and confusing forms can lead to user confusion, a higher bounce rate, and ultimately lower credibility for the website.


---
