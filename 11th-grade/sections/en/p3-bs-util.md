<!-- page 151 -->

### The margin and padding classes

Bootstrap has two sets of classes, `m{side}-size` and `p{side}-size`, for setting the space around and the extra space inside elements, which in CSS are set by the properties margin and padding. The side parameter sets the direction of the margin or the empty space and the size parameter sets the size of the margin or the empty space. The sets of classes m and p and their meaning are given in the table below:

*Table 2: The margin and padding classes in Bootstrap*

| margin classes | padding classes | Meaning |
| --- | --- | --- |
| `m-size` | `p-size` | On all sides |
| `m{t}-size` | `p{t}-size` | Top (top) |
| `m{e}-size` | `p{e}-size` | Right side in ltr (end) |
| `m{b}-size` | `p{b}-size` | Bottom (bottom) |
| `m{s}-size` | `p{s}-size` | Left side in ltr (start) |
| `m{x}-size` | `p{x}-size` | Left and right (the x axis) |
| `m{y}-size` | `p{y}-size` | Top and bottom (the y axis) |

The size value is a number from zero to five. Each number in this range stands for a certain distance in px.

*Table 3: The values of the size parameter in px*

| Size in px | Size |
| --- | --- |
| 4px | 1 |
| 8px | 2 |
| 16px | 3 |
| 24px | 4 |
| 48px | 5 |

The size parameter can also be auto, which means automatic. mx-auto gives the element equal left and right margins, so that it sits in the middle of its parent.

<!-- page 152 -->

> **Workshop**
>
> **Using the margin and padding classes**
>
> Continuing the previous workshop, add a div element with the properties below to the web page:
>
> ![Book image](../images/p158-01.png)
>
> In the code above, the distance of the `<div>` element from the element above it is 24px (mt-4), and its left and right margins are set automatically (mx-auto). The extra space inside the element is set to 16px (p-3) on all sides.

### The border, rounded, and shadow classes

Bootstrap has a set of classes for borders, rounded corners, and shadows. The border classes create a border and set its color and thickness. The rounded classes round the corners, and the shadow classes create shadows. Table 4 introduces the kinds of border, rounded, and shadow classes.

*Table 4: Kinds of border, rounded, and shadow classes*

| Shadow and its size | Rounded corners | Border color | Border and its thickness |
| --- | --- | --- | --- |
| `shadow-none`<br>`shadow-sm`<br>`shadow`<br>`shadow-lg` | rounded<br>`rounded-circle`<br>`rounded-pill`<br>`rounded-top`<br>`rounded-bottom`<br>`rounded-start`<br>`rounded-end` | `border-primary`<br>`border-secondary`<br>`border-success`<br>`border-danger`<br>`border-info`<br>`border-warning`<br>`border-light`<br>`border-dark` | border<br>`border-1`<br>`border-2`<br>`border-3`<br>`border-4`<br>`border-5` |

*Table 5: Bootstrap classes for the amount of corner rounding and the border thickness*

| Size | Amount of rounding | Border thickness | Border |
| --- | --- | --- | --- |
| `0px (no rounding)` | `rounded-1` | 1px | `border-1` |
| 2px | `rounded-2` | 2px | `border-2` |
| 4px | `rounded-3` | 3px | `border-3` |
| 6px | `rounded-4` | 4px | `border-4` |
|  | `rounded-5` | 5px | `border-5` |

<!-- page 153 -->

Among the rounded classes, rounded-circle makes an element completely round; for that, its width and height must be equal. rounded-pill rounds the corners like a pill or capsule. The words start and end refer to the left and right sides of an element.

> **Workshop**
>
> **Using the border, shadow, and rounded classes**
>
> Continuing the previous workshop, add two elements with the properties below to the page `test-bs.html`.
>
> To create the rectangular box in the image below, write this code:
>
> ![Book image](../images/p159-01.png)
>
> To create a round image, add a product image with equal width and height to the page and set it up as below:
>
> ![Book image](../images/p159-02.png)

### Typography classes

Bootstrap's text classes are used to set the font size and weight, alignment, list styles, and more. Table 6 shows some of the text classes.

*Table 6: Bootstrap text classes*

| Text size | Weight | Text alignment | List style | Text decoration |
| --- | --- | --- | --- | --- |
| `fs-1 … fs-6`<br>h1 … h6<br>`display-1 … display-4` | `fw-bold`<br>`fw-light`<br>`fw-lighter` | `text-start`<br>`text-center`<br>`text-end` | `list-unstyled`<br>`list-inline` | `text-decoration-none`<br>`text-capitalize`<br>`text-uppercase` |

- The fs-\* classes set the font size of text elements, from small (fs-6) to large (fs-1).

- The classes h1 to h6 set the size of heading tags.

- The display-\* classes create large headings to catch the user's attention; they carry no special meaning.

<!-- page 154 -->

The list-unstyled class removes the list's default style; that is, the bullets or numbers next to the items disappear and padding-left becomes zero.

The list-inline class prepares list items to be laid out horizontally, provided the items have the class `list-inline-item`. This kind of list is used for simple menus and small navigation bars.

### The flex classes

Bootstrap has many classes for designing page elements with the Flexbox technique. The flex system has two base classes, d-flex and d-inline-flex, used on container elements. For example, the product introduction section needs a container in which the products sit flexibly side by side. The table below introduces some flex classes by topic.

*Table 7: Flexbox classes*

| Horizontal alignment of elements | Vertical alignment of elements | Layout direction | Move to the next line |
| --- | --- | --- | --- |
| `justify-content-start`<br>`justify-content-center`<br>`justify-content-end`<br>`justify-content-between`<br>`justify-content-around`<br>`justify-content-evenly` | `align-items-start`<br>`align-items-center`<br>`align-items-end`<br>`align-items-baseline` | `flex-row`<br>`flex-row-reverse`<br>`flex-column`<br>`flex-column-reverse` | `flex-wrap`<br>`flex-nowrap`<br>`flex-wrap-reverse` |

The justify-content-\* classes set the horizontal alignment of content in a container. The first three align the content of an element to the left (start), center (center), and right (end). The next three set how elements are spread out by the space between them.

The align-items-\* classes set the vertical alignment of elements.

> **Workshop**
>
> **Using different classes in the product images section**
>
> In this workshop you will change the code of the «Newest products» section with Bootstrap classes as below.
>
> 1. Open the `index.html` file from learning unit 1. Add the Bootstrap 5 CDN link and script code in the right places.
>
> 2. Make the following changes in the `<main>` element:
>
> ![Book image](../images/p160-01.png)

<!-- page 155 -->

> **Workshop (continued)**
>
> ![Book image](../images/p161-04.png)

> **Workshop**
>
> **Designing the shop introduction section**
>
> In this workshop you will create a section with text content at the bottom of the shop page. Use different Bootstrap classes to design it.
>
> In the file `index.html`, add the `<article>` tag as below before the `</main>` tag:
>
> ![Book image](../images/p161-01.png)
>
> Add the headings and paragraphs below inside the `<article>` tag:
>
> ![Book image](../images/p161-02.png)
>
> Save the file and see the result in the browser.
>
> Bootstrap version 3 had a class named text-justify for justifying text on both sides (justify). This class does not exist in Bootstrap version 5. So, to justify the text in paragraphs, add a custom text-justify class to the file `styles.css` with the code below:
>
> ![Book image](../images/p161-03.png)
