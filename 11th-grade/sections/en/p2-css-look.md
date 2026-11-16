<!-- page 121 -->

> **Activity**
>
> Apply the text formatting properties to the elements of the file `test.html` and see the result in the browser.

## طراحی ظاهر عناصر (رنگ‌ها، پس زمینه‌ها، شفافیت و خط دور)

CSS دارای ویژگی‌های مختلفی در زمینه تنظیم ظاهر عناصر است. این ویژگی‌ها برای تعیین رنگ متن، رنگ زمینه، تصویر پس‌زمینه، کنترل تصویر پس‌زمینه، شفافیت و خط دور عناصر به‌کار می‌روند. در ادامه به برخی از این ویژگی‌ها اشاره می‌شود.

**color and background-color**: set the text color and background color of elements. For both you can use a color name, a hexadecimal color code, or an RGB code.

> **Example**
>
> The example opposite uses all three ways of giving a color.
>
> ```
> color: blue;
> background-color: #0000FF;
> background-color: rgb(0,0,255);
> ```

**opacity**: sets how transparent an element is. The value of opacity is a number between 0 and 1. Low values make the element more transparent, and values near 1 make it more opaque.

**background-image**: sets the background image. Its value is written as the word url followed by the image name in parentheses,

> **Example**
>
> as in the example opposite:
>
> ```
> background-image:url(./images/background.jpg);
> ```

**background-repeat**: images that do not cover the width of the page are repeated. This property sets whether and how the image repeats, with values such as no-repeat, repeat-x, repeat-y, and so on.

**background-size**: sets the size of the background image, that is, at what size it is shown inside the element. To cover the width of the page without repeating the image, this property is used with the value cover.

**background-position**: sets where the background image is shown, with values such as center, left, right, left top, right bottom, and so on.

<!-- page 122 -->

**background-attachment**: if the background image is larger than the visible area, scrolling shows its lower parts. To keep the image fixed while the page scrolls, this property is used with the value fixed.

**border**: page elements can be shown with a border. Borders are created with the border property. Its values set, in order, the thickness, the type, and the color of the border.

```
border: 1px solid gray;
```

**border-radius**: rounds the corners; its value can be in pixels or percent:

```
border-radius:10px;
```

> **Workshop**
>
> **طراحی ظاهر عناصر (رنگ‌ها، پس‌زمینه‌ها، شفافیت و خط دور)**
>
> Write the HTML code below in the file `test.html` and see the result in the browser. Then add the styles step by step to understand the effect of each one on the page's elements.
>
> ![Book image](../images/p128-01.png)

<!-- page 123 -->

> **Workshop (continued)**
>
> In Paint, create a new file named `background.jpg` and save it in the images folder next to the file `test.html`. Set its size to 50×50 pixels. Draw two hollow circles in a soft color inside it (like the image opposite) and save the file. This image is applied as the background of the div element.
>
> ![Book image](../images/p129-01.png)
>
> ![Book image](../images/p129-04.png)

### CSS selectors

The element or set of elements a CSS style is written for is called a selector. CSS has several kinds of selectors, including simple, combinator, pseudo-class, pseudo-element, and attribute selectors, which this part covers.

### انتخاب‌گرهای ساده (Simple)

These selectors use tag names, IDs, classes, and the \* sign to select elements. The kinds of simple selectors are listed in Table 8:

*Table 8: Kinds of simple selectors*

| Kind of selector | What it does |
| --- | --- |
| Element (Element) | Selects page elements by tag name, such as h2, p, table, body, and so on |

![Book image](../images/p129-02.png)

![Book image](../images/p129-03.png)

<!-- page 124 -->

![Table](../images/p130-01.png)

![Book image](../images/p130-02.png)

![Book image](../images/p130-03.png)

![Book image](../images/p130-04.png)

![Book image](../images/p130-05.png)

<!-- page 125 -->

| Kind of selector | What it does |
| --- | --- |
| Group (Group) | Selects a group of elements: group selectors apply a set of CSS rules to several elements. In a group selector the element names are written with commas between them. In the example below, h1, h2,p is a group selector. The rules above are applied to the `<h1>`, `<h2>`, and `<p>` tags, so all of them become blue and centered. |
| Universal (universal) | **Selecting all page elements with the** \* **sign**: in the example below, the outer margin (margin) and inner spacing (padding) of all page elements are set to zero. |

![Book image](../images/p131-01.png)

![Book image](../images/p131-02.png)

![Book image](../images/p131-03.png)

### انتخاب‌گر ترکیبی(Combinator)

Combinator selectors in CSS define a structural and positional relationship between two or more selectors, such as the child selector with the `>` sign and the descendant selector with a space. Elements written nested inside each other have a parent–child relationship. For example, li is a child of ul, so to select the li elements you write ul li or `ul > li`. Using the `>` sign limits the effect to the direct children of an element.

<!-- page 126 -->

> **Example**
>
> The image below shows an example of using a combinator selector.
>
> ![Book image](../images/p132-01.png)

### انتخاب‌گرهای شبه‌کلاس (Pseudo-class Selectors)

Pseudo-class selectors let you style elements based on their state, position, or dynamic properties. Some of them become active depending on what the user does. Pseudo-classes are written with a : sign after the element name. The pseudo-class selectors are:

**hover**: active when the user moves the mouse pointer over an element.

**focus**: happens when an element (usually a form element) becomes active and the user can interact with it.

**active**: active when an element is in the active state, for example while the user clicks a button.

**`nth-child()`**: selects the children of an element by their position.

**`first-child`**: selects the first child of an element.

**`last-child`**: selects the last child of an element.

<!-- page 127 -->

### انتخاب‌گر ویژگی (Attribute selector)

An attribute selector selects elements by their attributes. For example, to select the text elements of a form the selector `input[type="text"]` is used, and to select elements that have an href attribute the selector \[href\] is used.

> **Workshop**
>
> **کار با انواع انتخاب‌گرهای CSS (طراحی منو)**
>
> Create a file named `index.html` and write the HTML code below in it. Save the file and see the result in the browser. Then add the element styles to the head part step by step and check the result of each style.
>
> ![Book image](../images/p133-01.png)
>
> ![Book image](../images/p133-02.png)

> **Activity**
>
> 1. In front of each selector, write its kind as a comment. Put the comment text inside the /\* \*/ marks.
>
> 2. What does the list-style property with the value none do?
