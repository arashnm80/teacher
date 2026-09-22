**Page 166**

Working with Bootstrap responsive classes

### Workshop

In this workshop you will use Bootstrap classes to make changes to the `index.html` page.

Part one: using the `row-cols` classes: In the previous workshop the column sizes were set with the `col-sm-3` class. That class makes the columns appear side by side on devices wider than 576 pixels, and stack on top of each other on smaller devices.

Bootstrap has another responsive class named `row-cols` that lets you set how many columns appear (in each row) on different devices; the column size is set on the `row` element, not on the `.col` elements. The table below shows how to use these two methods.

Method of setting column size

### Explanation

![Book image](../images/p172-01.png)

Setting column size on

This code creates a row (`row`) with two columns (`col-6`). Each column occupies half of

the `col` elements

6).

__

the row width (12

`B`

`A`

![Book image](../images/p172-02.png)

`B`

`A`

`D`

`C`

Setting column size on `row` elements

The `row-cols-2` class creates 2 columns in each row. In the code above there are 4 `col` elements; therefore two rows are produced, each containing two columns.

If you add more `col` elements, the columns move to the next row.

`Bootstrap` automatically adjusts the column widths; therefore you do not need to set the size of each column by hand.


---

**Page 167**

1 In the `index.html` file, add the following code after the newest products:

![Book image](../images/p173-01.png)

Save the file and check the result in the browser. Then follow the steps below and view the result after each step.

2 For all images use the `border`, `border-4`, and `rounded-circle` classes so the images are round and have a border.

3 For each `col` class add the `mb-3` class so that in the mobile view the images have space from the image below them.

4 To set the image size, add the style shown below to the `styles.css` file.

![Book image](../images/p173-02.png)

Place each product title inside an `<h3>` tag:

![Book image](../images/p173-03.png)

5 To set the size of the `h3` text and its distance from the image above, write the style shown below:

![Book image](../images/p173-04.png)


---

**Page 168**

After you finish the previous steps, you are expected to get the output below in the desktop view.

![Book image](../images/p174-01.png)

6 To see how the images look on different devices, press the `f12` key. In response to the message window, choose the Open DevTools button. As in the image below, from the toolbar at the top of the page choose the Toggle Device button:

![Book image](../images/p174-02.png)

7 From the `Dimension` drop-down, choose the device type and then observe the images.

![Book image](../images/p174-03.png)

8 If you wish, choose the `Responsive` option from the drop-down and then drag the right edge of the device to change its width as you like.

How the `row-cols` classes work in the workshop above is as follows:

`row-cols-sm-1:` On devices with a width of 576 pixels and more, the product images are shown in 2 columns.

`row-cols-lg-2:` On devices with a width of 992 pixels and more, the product images are shown in 4 columns.

Part two: using the `container` classes. The `container` classes are responsive and create different widths for the container element on different devices.


---

**Page 169**

`container` classes and their widths on different devices

```
XX-Large
X-large
```

`Large`

```
Medium
```

`Small`

```
Extra small
```

`1400px`≤

`1200px`≤

`992px`≤

`768px`≤

`576px`≤

`576px<`

`1320px`

`1140px`

`960px`

`720px`

`540px`

100%

```
.Container
```

`1320px`

`1140px`

`960px`

`720px`

`540px`

100%

```
.Container-sm
```

`1320px`

`1140px`

`960px`

`720px`

100%

100%

```
.Container-md
```

`1320px`

`1140px`

`960px`

100%

100%

100%

```
.Container-lg
```

`1320px`

`1140px`

100%

100%

100%

100%

```
.Container-xl
```

`1320px`

100%

100%

100%

100%

100%

```
.Container-xxl
```

100%

100%

100%

100%

100%

100%

```
.Container-fluid
```

In the “Designing the store introduction section” workshop, the width of the `article` element was set to 75% and 90% on desktop and mobile devices, respectively. Here you will use responsive `container` classes instead of `CSS` code. Follow the steps below:

On the `article` element use the `container-sm` class:

![Book image](../images/p175-01.png)

Remove both styles for the `article` element from the `styles.css` file.

Save the `HTML` and `CSS` files and check the result in the browser. With this change, the width of the `article` element for devices with a page width of 576 pixels and larger is set by the `container` class, and for smaller devices the element width will be 100%.

Part three: working with the `display` classes. In the “Designing the `Toolbar`” workshop, a toolbar was designed at the top of the page. The “Sign up|Sign in” options and its logo were hidden in the mobile view and placed at the bottom of the page inside a new layer named `bottom-toolbar`. The goal of this workshop is to hand control of showing/hiding the elements of the `toolbar` and `bottom-toolbar` layers over to the `d-*` classes and remove the related `CSS` code.


---

**Page 170**

First add the `d-flex` and `d-lg-none` classes to the set of classes on the `bottom-toolbar` element:

![Book image](../images/p176-01.png)

Remove the `display:none` property from the set of properties of the `.bottom-toolbar` element in the `styles.css` file.

In the `media` rule, remove the `.bottom-toolbar` selector. Save the file and check the result in the browser.

To hide the two “Sign up|Sign in” and logo elements at widths less than 992 pixels, add the `d-none` and `d-lg-block` classes to the `signin-signup` and `logo` elements inside the `toolbar` element:

![Book image](../images/p176-02.png)

After adding the `d-*` classes, remove the style below from the `media` rule.

![Book image](../images/p176-03.png)

Save the file and check the result in the browser. You are expected that on devices 992 pixels and larger, the four elements logo, search box, “Sign in|Sign up” option, and shopping cart are present, but on smaller devices the logo and “Sign in|Sign up” elements are hidden.

To control the amount of extra space around the `Toolbar` element, assign the `p-3` class to the `toolbar` element and then remove the `padding` property from the `toolbar` class. From the `Dimension` drop-down in the browser, choose the `Responsive` option and then check the result.

![Book image](../images/p176-04.png)

Part four: creating a responsive image. The goal of this part is to add a banner above the `toolbar` element so that the banner image is responsive to the page width. To do this, insert the `top-banner.jpg` image at the beginning of the `<header>` tag and use the `img-fluid` class for it:

```
>"class="img-fluid w-100 "img src="./images/top-banner.gif<
```

The `img-fluid` class is one of the important `Bootstrap` classes for making images responsive; it makes the image resize to match its parent, not become wider than the `container`, and display correctly on mobile, tablet, and desktop.


---

**Page 171**

Of course, creating a responsive image is not limited to using the `img-fluid` class. For images that fill the full width, it is better to design another version of the image for smaller devices. In the example below, three versions of the banner image are used for mobile, tablet, and desktop. Based on the page width, the browser chooses the appropriate image to display:

![Book image](../images/p177-01.png)

Most modern browsers today support the `picture` tag; therefore in modern browsers, the images set in the `<source>` tags are displayed. In older browsers such as Internet Explorer 11 and earlier, the default image appears. In the code in the figure above, the default image is specified in the `<img>` tag.

### Activity

Design three banner images in three different sizes for display on mobile, tablet, and desktop, and write the display code for them according to the code above. You are expected to get an output like the figure below.

![Book image](../images/p177-02.png)

Attention

If the edges of the banner are not flush with the edges of the browser, set the `padding` and `margin` values for the `header` element to zero.

```
اجزای رابط کاربری (User Interface Components)
```

Users of web pages interact with the page through various components. These components include buttons, menus, search bars, icons, forms, images, colors, fonts, and other visual elements that shape the user experience. Bootstrap has a set of ready-made classes for various user interface components such as the navbar, form, button, accordion menu, and so on, which are covered in this section.


---

**Page 172**

```
Navbar
```

The `navbar` class is used to create a navigation bar (`Navigation` `Bar`) or the menu at the top of the page. This class is used together with other classes such as `navbar-expand-*` to set the behavior and appearance of the navigation bar at different screen sizes. The set of `Navbar` classes is as follows:

`navbar:` The main class for creating a navigation bar.

`navbar-expand-*:` These classes determine at what width the navigation bar appears horizontally and at what width it collapses. The * character can be replaced with `sm`, `md`, `lg`, or `xl`. For example, using `navbar-expand-sm` makes the navigation bar appear horizontally on devices with a width of 576 pixels and more, and on smaller devices it collapses and is shown as a hamburger button (☰).

`navbar-brand:` Used to display a logo or brand name in the navigation bar.

`navbar-nav:` Used to create a navigation list (`Navigation` `list`) in the navigation bar.

`nav-link:` Used for the links in the navigation list.

`navbar-toggler:` Used for the small menu button. This button appears in the mobile view so the user can click it to see the menu content and click again to close the menu. (It creates a button to control opening and closing the menu.) `navbar-toggler-icon:` Used to show the hamburger icon (☰) for the menu button in the collapsed state.

`navbar-collapse:` Used to group and hide the menu options on small devices.

`dropdown:` Used to create drop-down menus in the navigation bar.

`navbar-light` and `navbar-dark:` Used to set the color of the navigation bar content so that the readability of the elements inside it is preserved. The `navbar-light` class creates a navigation bar with a light background and dark text color, and the `navbar-dark` class creates a navigation bar with a dark background and light text.

Choosing these classes correctly increases readability and improves the user experience.


---
