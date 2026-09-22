# Developing interactive web pages with Bootstrap


---

**Page 146**

## Learning unit 1

## Developing interactive web pages with Bootstrap

### Have you ever thought

How can you design responsive, mobile-friendly websites without writing complex `CSS` code?

Are there frameworks that provide ready-made `CSS` classes for web developers?

What ready-made classes and components does Bootstrap have for designing different parts of web pages?

How can you use Bootstrap to design data-entry forms quickly and in a modern style?

How can you optimize web page design with Bootstrap so that pages display in the best way on all devices?

### At the end, the student is expected to

1 Fully design the structure of a web page (including header, body, and footer) using Bootstrap’s grid system (`Grid` `System`), so that the layout responds correctly on different screen sizes (mobile, tablet, desktop).

2 Select and use utility classes (`Utility` `Classes`) such as color, spacing (`Margin/Padding`), shadow, and typography classes for fast, standard styling of elements without writing manual `CSS` for common cases.

3 Build a practical and attractive navigation bar (`Navbar`) that includes links, buttons, and responsive features, and also design a structured footer.

4 Gain skill in implementing user-interface components such as carousels (sliding images) and accordions to present information in an engaging and dynamic way.

5 Build registration or contact forms with complete Bootstrap styling.

6 Change and override Bootstrap’s default styles using customization methods to match the website’s appearance with the brand or the specific needs of the project.

### Performance standard

Use Bootstrap’s ready-made classes to set the style of different page elements such as buttons, forms, menus, and so on, and be able to design a responsive page on different devices.


---

**Page 147**

### Definition of a framework

A framework (`Framework`) is a pre-designed software framework used to speed up the process of designing and developing websites and web applications. By providing a set of tools, libraries, and ready-made patterns, a framework lets developers focus only on the specific features and functions of the project and avoid repetitive, basic work.

```
Bootstrap چیست؟
```

Bootstrap is an open-source framework for designing a site’s appearance that includes a set of ready-made code written in the languages `Css`, `Html`, and `Java` `Script`. Instead of writing everything from scratch, developers use this ready-made code.

Features of `Bootstrap:` Bootstrap has many features for designing web pages that have made it popular among web developers and designers. These features are as follows:

Responsive design (`Responsive` `Design`): Bootstrap has a 12-column grid system that makes responsive design possible for different devices.

Pre-designed components (`Components`): Bootstrap includes various components such as buttons, forms, navigation menus, cards, modals, and search bars that are ready to use.

JavaScript support: Bootstrap contains JavaScript libraries for creating interactions and animations in different parts of the page.

Browser support: Bootstrap is compatible with most modern browsers such as `Chrome`, `Firefox`, `Safari`, and `Edge`.

Comprehensive documentation: The official Bootstrap site (`getbootstrap.com`) has complete documentation for learning how to use Bootstrap’s components and classes.

Uses of `Bootstrap` Designing responsive websites: Designing and developing corporate sites, stores, blogs, and so on.

Creating attractive user interfaces: Designing beautiful, modern user interfaces for websites and web applications.

`minimum` `viable` `product` (`MVP`) projects: Building website prototypes (`MVP`) and evaluating design ideas.

Designing forms: Designing beautiful, responsive forms using Bootstrap’s ready-made classes.


---

**Page 148**

Using Bootstrap on a web page To use Bootstrap’s features on a web page, you must first create a basic `HTML` file and then attach Bootstrap’s `CSS` and JavaScript files to it. The basic file includes the `<DOCTYPE`!>,

```
<html>، <head>، متاتگ‌های viewport، <title> و <body> است.
```

Using `CDN1` on a web page

### Workshop

Create a web page named `test-bs.html` and write its initial tags. Then open the site `getbootstrap.com`. Scroll the page to the `Include` `via` `CDN` section so you can see the ready-made `<Link>` and `<script>` codes. Copy the `<link>` code into the `<head>` section and the `<script>` code before `<body/>`. These two codes attach Bootstrap’s `CSS` and JavaScript files to the web page.

The Bootstrap link and script code contains an attribute called `Integrity` that is used to keep the file received from the `CDN` secure. However, it is also possible to use Bootstrap classes without `Integrity`. For that reason, in the code above the `Integrity` attribute has been removed to make the code more readable, but using this attribute is essential in real projects.

![Book image](../images/p154-01.png)

Bootstrap classes and components Bootstrap classes are a set of predefined styles that make it possible to design user-interface parts of web pages quickly and easily. These classes, which were created using `CSS`, help the web developer add user-friendly, responsive elements to the web page while writing less `CSS` code.

```
)شبکه توزیع محتوا( CDN: Content Delivery Network١
```


---

**Page 149**

Bootstrap components are pre-designed elements that make it possible to design website user interfaces quickly and easily. With these ready-made elements, the web developer can add user-friendly, responsive elements to the web page without writing `CSS` and `JavaScript` code. Among Bootstrap’s components are the button, navigation bar1, carousel2, accordion3, and modal4. This section introduces Bootstrap’s classes and components.

`Utility` classes: `Utility` classes in Bootstrap are used especially for styling page elements and work directly with `HTML` and `CSS`. You do not need JavaScript to use these classes. Bootstrap’s ready-made classes can be used to set color, element size, spacing, border, shadow, and so on.

Color classes: Bootstrap’s color classes are divided into two groups: background colors and text colors.

Each color class has a specific meaning and color. Background and text color classes have the prefixes `bg` and `text`, respectively. Some of these classes are collected in the table below:

Table 1 Bootstrap color classes

Background color class

Text color class

Meaning

```
bg-primary
text-primaryرنگ اصلی
bg-secondary
text-secondaryرنگ ثانویه
bg-success
```

`text-success` Success color

```
bg-danger
text-dangerرنگ خطر
bg-warning
text-warningرنگ هشدار
bg-info
```

`text-info` Information color

```
bg-light
text-lightرنگ روشن
bg-dark
```

`text-dark` Dark color

1- Navigation bar (`Navbar`): The top bar of the page that usually includes the logo, links, and menus.

2- Carousel (`Carousel`): An interactive element that displays a set of images or content one after another in a defined space, and the user can move between them.

3- Accordion (`Accordion`): A section that can open and close to display content.

4- Modal (`Modal`): A window or dialog box that appears over the page content.


---

**Page 150**

### Try this

For more information about other color classes, search for the phrases `Bootstrap5.3` `background` and `Bootstrap5.3` `colors` on Google.

Using Bootstrap color classes

### Workshop

Open the file `test-bs.html`, then insert a `<div>` element with the following settings after the `body` tag.

![Book image](../images/p156-03.png)

Save the file and check the result in the browser.

Add the word `subtle` to the end of the color class (`bg-primary-subtle`) and view the result in the browser.

Sizing classes (`Sizing`) Bootstrap has two sets of classes, `*-w` and `*-h`, for setting the width and height of elements. The * parameter can be replaced with the numbers 25, 50, 75, and 100 and the word `auto`. Assigning the class `w-75` to an element makes the element’s width equal to 75% of the parent element’s width. The classes `w-auto` and `h-auto` set an element’s width and height to the size of its content.

Using `Sizing` classes

### Workshop

In the file `test-bs.html`, add another `div` element to the web page as shown below. This element contains a paragraph element whose width and height will be 75% of the width and height of the `div` element.

![Book image](../images/p156-01.png)

In the code above, the width and height of the paragraph element are set by the classes `w-75` and `h-75`. Save the file and check the result in the browser.

![Book image](../images/p156-02.png)


---
