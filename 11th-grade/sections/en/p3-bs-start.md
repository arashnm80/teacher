<!-- page 146 -->

## Learning unit 1

## Have you ever thought about this

- How can you design responsive, mobile-friendly websites without writing complex CSS?

- Are there frameworks that give web developers ready-made CSS classes?

- What ready-made classes and components does Bootstrap have for designing the parts of web pages?

- How can you design data-entry forms quickly and in a modern style with Bootstrap?

- How can you optimize web page design with Bootstrap so that pages look their best on all devices?

## By the end, the student is expected to

1. Design the complete structure of a web page (header, body, and footer) with Bootstrap's grid system (Grid System), so that the layout responds correctly at different screen sizes (phone, tablet, desktop).

2. Choose and use utility classes (Utility Classes), such as color, spacing (`Margin/Padding`), shadow, and typography classes, to style elements quickly and in a standard way without writing CSS by hand for common cases.

3. Build a useful, attractive navigation bar (Navbar) with links, buttons, and responsive features, and design a structured footer.

4. Be skilled at building user interface components such as carousels (slide images) and accordions to present information in an engaging, dynamic way.

5. Build sign-up or contact forms fully styled with Bootstrap.

6. Change and override Bootstrap's default styles with customization techniques, to match the website's look to a brand or to the needs of the project.

## Performance standard

Use Bootstrap's ready-made classes to style page elements such as buttons, forms, and menus, and be able to design pages responsively for different devices.

<!-- page 147 -->

## What a framework is

A framework (Framework) is a predesigned software structure used to speed up designing and developing websites and web apps. By providing a set of tools, libraries, and ready-made patterns, a framework lets developers focus only on the specific features and functions of the project and avoid repetitive, basic work.

**What is Bootstrap?**

Bootstrap is an open-source framework for designing the look of a site, consisting of a set of ready-made code written in CSS, HTML and JavaScript. Instead of writing everything from zero, developers use this ready-made code.

**Features of Bootstrap**: Bootstrap has many features for designing web pages that have made it popular among web developers and designers. They are:

**Responsive Design**: Bootstrap has a 12-column grid system that makes responsive design possible for different devices.

**Pre-designed Components**: Bootstrap includes various components such as buttons, forms, the navigation menu, cards, modals and the search bar that can be used ready-made.

**JavaScript support**: Bootstrap includes JavaScript libraries for creating interactions and animations in different parts of the page.

**Browser support**: Bootstrap works with most modern browsers, such as Chrome, Firefox, Safari, and Edge.

**Thorough documentation**: Bootstrap's official site (`getbootstrap.com`) has complete documentation on how to use its components and classes.

**Uses of Bootstrap**

**Designing responsive websites**: designing and building company sites, shops, blogs, and so on.

**Creating attractive user interfaces**: designing beautiful, modern user interfaces for websites and web apps.

**MVP projects (minimum viable product)**: building first versions of websites (MVP) and testing design ideas.

**Designing forms**: designing beautiful, responsive forms with Bootstrap's ready-made classes.

<!-- page 148 -->

### Using Bootstrap in a web page

To use Bootstrap's features in a web page, first create a basic HTML file and then link Bootstrap's CSS and JavaScript files to it. The basic file contains the tags `<!DOCTYPE html>`, `<html>`, `<head>`, the viewport meta tag, `<title>`, and `<body>`.

> **Workshop**
>
> **Using a CDN¹ in a web page**
>
> Create a web page named `test-bs.html` and write its basic tags. Then open `getbootstrap.com`. Scroll down to the Include via CDN section to see the ready-made `<Link>` and `<script>` code. Copy the `<link>` code into the `<head>` part and the `<script>` code just before `</body>`. These two pieces of code link Bootstrap's CSS and JavaScript files to the web page.
>
> Bootstrap's link and script code has an attribute named Integrity, used to keep the file received from the CDN secure. Bootstrap's classes can still be used without Integrity, so in the code above Integrity has been removed to make the code easier to read; but in real projects using it is essential.
>
> ![Book image](../images/p154-01.png)

### Bootstrap classes and components

Bootstrap classes are a set of predefined styles that make it quick and easy to design the user interface of web pages. Built with CSS, they help web developers add user-friendly, responsive elements to a web page while writing less CSS.

> **Footnotes**
>
> 1. CDN: Content Delivery Network

<!-- page 149 -->

Bootstrap components are predesigned elements that make it quick and easy to design a website's user interface. With these ready-made elements, a web developer can add user-friendly, responsive elements to a web page without writing CSS and JavaScript. Bootstrap components include the button, the navigation bar¹, the carousel², the accordion³, and the modal⁴. This part introduces Bootstrap's classes and components.

**Utility classes**: Bootstrap's utility classes are used specifically to style page elements and work directly with HTML and CSS. Using these classes needs no JavaScript. Bootstrap's ready-made classes can set color, element size, spacing, borders, shadows, and so on.

**Color classes**: Bootstrap's color classes are of two kinds, background colors and text colors. Each color class has its own meaning and color. Background and text color classes start with bg and text. Some of them are listed in the table below:

*Table 1: Bootstrap color classes*

| Background color class | Text color class | Meaning |
| --- | --- | --- |
| `bg-primary` | `text-primary` | Primary color |
| `bg-secondary` | `text-secondary` | Secondary color |
| `bg-success` | `text-success` | Success color |
| `bg-danger` | `text-danger` | Danger color |
| `bg-warning` | `text-warning` | Warning color |
| `bg-info` | `text-info` | Info color |
| `bg-light` | `text-light` | Light color |
| `bg-dark` | `text-dark` | Dark color |

> **Footnotes**
>
> 1- Navigation bar (Navbar): the bar at the top of the page that usually holds the logo, links, and menus.
>
> 2- Carousel (Carousel): an interactive element that shows a series of images or content one after another in a given space, and the user can move between them.
>
> 3- Accordion (Accordion): a section that opens and closes to show content.
>
> 4- Modal (Modal): a window or dialog box that appears over the page content.

<!-- page 150 -->

> **Curiosity**
>
> For more information about the other color classes, search Google for Bootstrap5.3 background and Bootstrap5.3 colors.

> **Workshop**
>
> **Using Bootstrap's color classes**
>
> Open the file `test-bs.html`, then insert a `<div>` element with the properties below after the body tag.
>
> ![Book image](../images/p156-03.png)
>
> Save the file and check the result in the browser.
>
> Add the word subtle to the end of the color class (bg-primary-subtle) and see the result in the browser.

### Sizing classes

Bootstrap has two sets of classes, \*-w and \*-h, for setting the width and height of elements. The \* parameter can be replaced by the numbers 25, 50, 75 and 100 and the word auto. Giving the class w-75 to an element makes the width of the element 75% of the width of the parent element. The classes w-auto and h-auto set the width and height of an element to the size of its content.

> **Workshop**
>
> **Using the Sizing classes**
>
> In the file `test-bs.html`, add another div element to the web page as below. It contains a paragraph element whose width and height will be 75% of the width and height of the div element.
>
> ![Book image](../images/p156-01.png)
>
> In the code above, the width and height of the paragraph are set with the classes w-75 and h-75. Save the file and check the result in the browser.
>
> ![Book image](../images/p156-02.png)
