<!-- page 173 -->

> **Workshop**
>
> **Designing the navigation bar**
>
> In this workshop you will add Bootstrap's collapsible navigation bar to the page `index.html`. Before doing this, remove the top-menu code or put it completely inside `<!-- -->` so that the browser does not interpret it.
>
> The navigation bar needs the file `bootstrap.bundle.min.js` to work correctly. If this file is not in the `<head>` part or before `</body>`, add it as explained in «Using a CDN in a web page»; otherwise clicking the hamburger button (☰) will not show its content.
>
> Replace the top-menu element with the code in the figure below:
>
> ![Book image](../images/p179-01.png)
>
> The code above has two elements: a «button» and a «collapsible area». The button is created with the `<button>` tag. Inside it is a `<span>` element with the class `navbar-toggler-icon`, which shows a three-line icon.
>
> The list content is in a container with the ID navbarCollapse. Clicking the menu button should open the area holding the list. For this, the data-bs-target attribute is used with the value `#navbarCollapse`.
>
> `data-bs-target="#navbarCollapse"` gives the ID of the menu to open or close.
>
> The attribute `data-bs-toggle="collapse"` makes the menu open and close when the button is clicked.
>
> The color of the navigation bar is set with bg-primary; if you like, you can use other background color classes.
>
> The collapse class makes the content inside the div collapsed (collapsed), and the toggle button opens/closes it. (This class turns on opening and closing of the content.)
>
> The navbar-collapse class puts the links vertically (one under another) when the menu opens and gives the menu standard padding (padding) that matches the other navigation parts. If only collapse is used, the menu links look messy.

<!-- page 174 -->

> **Workshop (continued)**
>
> Now it is time to write the list of menu items. Add the code in the figure below at the marked place in the previous code:
>
> ![Book image](../images/p180-01.png)
>
> The list's parent element (ul) uses the navbar-nav class, and the list items use the nav-item class. By default the navigation menu options appear on the right of the page. The mx-auto class is used to set the left and right margins of the menu.
>
> - Save the file and check the result in the browser.
>
> navbar-expand-lg makes the menu bar horizontal at widths above 992 pixels. Change lg to md and check the result.
>
> In shopping sites, the navigation menu is hidden in the mobile and tablet views; add the classes d-none and d-md-block to the nav element and check the result in the mobile and tablet views.
>
> > **Curiosity**
> >
> > What effect does the active class, applied only to the first option, have on how that option looks?
>
> - The first option of most shopping sites is «Product categories», which holds a list of product groups. To create this option, add the code in the figure below before the first item of the list above (Customer club):
>
> ![Book image](../images/p180-02.png)
>
> nav-item: used for each menu option.

<!-- page 175 -->

> **Workshop (continued)**
>
> dropdown: used for the element that holds a submenu.
>
> nav-link: used to style the links of the navigation bar (Navbar) so they look like the Navbar.
>
> active: shows an option differently (bolder) from the others and means the option is active.
>
> dropdown-toggle: tells Bootstrap's JavaScript that this element can open and close, and adds a small arrow ▼ next to the menu option to show it has a submenu.
>
> `data-bs-toggle="dropdown"`: turns on the two-state (open and closed) behavior of the menu. dropdown-menu: usually used on the `<ul>` element; it makes the content of the list a hidden box under the menu option.
>
> dropdown-item: sets the style of each option of the drop-down menu.
>
> Remove the active class from the first option of the list in the previous step (Customer club). Save the file. You should get the result below:
>
> ![Book image](../images/p181-01.png)
>
> As mentioned, the dropdown-toggle class shows a downward arrow. You can remove it if you like, but then you need to add the style below to open the submenu on hover:
>
> ![Book image](../images/p181-02.png)

> **Note**
>
> Since hover does not happen in the mobile view, this code works only in the desktop view.

### Buttons

A button is one of the interactive elements of a page; clicking it carries out an action. A button can be created in a web page with the three tags below:

1. `<button>`

2. `<input>`

3. `<a>`

<!-- page 176 -->

Bootstrap has different classes for styling buttons. They let you customize the color, size, and other features of buttons. To style a button with Bootstrap classes, the btn class is required; to choose the button's color and size, other button classes can be added alongside btn.

These classes are summarized in Table 11:

*Table 11: Button classes in Bootstrap*

| Kind of class | Class names |
| --- | --- |
| Color | btn-primary, btn-secondary, btn-danger, btn-light, btn-dark, btn-link, and so on |
| Button borders | btn-outline-primary, btn-outline-secondary, and so on |
| Button sizes | btn-sm, btn-lg |
| Disabled state | disabled |

> **Example**
>
> In the example below, six buttons are created with different tags and classes:
>
> ![Book image](../images/p182-01.png)
>
> ![Book image](../images/p182-02.png)

> **Learn more**
>
> **Laying out a product page**
>
> In this workshop you will design a product information page in three columns: the product image, the product features, and the product price. The header and footer of this page are the same as in the file `index.html`; only the main part has different content. To speed up the design, make a copy of `index.html`: open `index.html` in the text editor, choose Save As from the File menu, and type `product-details.html` as the page name.

<!-- page 177 -->

> **Learn more (continued)**
>
> Delete the whole content of the `<main>` tag. Save the file and open the product-details page in the browser to make sure everything works. At this stage the product-details page should have the banner at the top, the logo bar, the navigation bar, and the footer.
>
> Write the code in the figure below inside the `<main>` tag to lay out the product page:
>
> ![Book image](../images/p183-01.png)
>
> This layout uses the Grid system. On devices 992 pixels or wider, the columns take 4/12, 5/12, and 3/12. At widths of 768 to 992 pixels each column takes 4/12, and on smaller devices the contents of the columns are stacked.
>
> Define the width of the product-information element in the file `styles.css` as below:
>
> ![Book image](../images/p183-02.png)
>
> Add the image of the book «Basic Technical Knowledge» to the first column as below:
>
> ![Book image](../images/p183-03.png)
>
> So that the product image sits in the middle of the column on all devices, add the classes d-flex, `justify-content-center`, and align-items-center to the first column, after the col-lg-4 class:
>
> ![Book image](../images/p183-04.png)
>
> To control the size of the image on devices narrower than 768 pixels, add the style below to the file `styles.css`:
>
> ![Book image](../images/p183-05.png)

<!-- page 178 -->

> **Learn more (continued)**
>
> Write the content of the second column as in the figure below:
>
> The fs-3 class sets the text size, and the text-sm-end class sets the text alignment (on the right of the column).
>
> ![Book image](../images/p184-01.png)
>
> Set the style of the second column's content as in the figure below:
>
> ![Book image](../images/p184-02.png)
>
> In the mobile view, the content of the second column sticks to the right edge of the browser and does not look good. To move the content away from the right side so that it sits in the middle of the column, the content of the second column is put inside a div element with the class details-container. Set the properties of this element as in the figure below:
>
> ![Book image](../images/p184-03.png)
>
> Enter the code written in the figure below inside the third column:
>
> ![Book image](../images/p184-04.png)

<!-- page 179 -->

> **Learn more (continued)**
>
> Write the style of the third column's content as in the figure below:
>
> ![Book image](../images/p185-01.png)
>
> On devices 992 pixels or wider the result should look like this:
>
> ![Book image](../images/p185-02.png)

> **Activity**
>
> In the file `index.html`, link the product «Basic Technical Knowledge» to the page `product-details.html`.

### Forms

Data-entry forms are tools for users to interact with the page and for collecting information. The look of forms plays a vital role in the user experience and in a website's success. Attractive, user-friendly forms increase user interaction and build trust and satisfaction. Messy, confusing forms, on the other hand, can confuse users, raise the bounce rate, and in the end lower the website's credibility.
