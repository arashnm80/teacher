**Page 128**

Box model (`Box` `Model`) The box model (`Box` `Model`) in `CSS` is used to design and lay out elements on web pages. Every `HTML` element is treated as a “box” that includes four parts: content (`content`), extra space inside the element (`padding`), border (`border`), and the distance of the element from neighboring elements (`margin`). In the example below these settings can be viewed and examined: (Figure 25).

The `width` and `height` properties only specify the width and height of the content area (`content`). So assigning values to the `padding`, `margin`, and `border` properties increases the final dimensions of the box. These values must be included in box dimension calculations. To

![Book image](../images/p134-01.png)

Distance to other elements

prevent the `border` and `padding` properties from affecting

Distance between content and border

the width and height of the element, use the `box-sizing` property with

Element content

the value `border-box`. When you do this, the total of content, `padding`, and `border` dimensions in

Element border

the horizontal and vertical directions will equal the `width` and `height` values.

**Figure 24**

Examining how the box model works

### Workshop

Create a file named `box-model.html` and put two `<div>` and `<img>` elements along with their styles into the file:

![Book image](../images/p134-02.png)


---

**Page 129**

In the `index.html` file (previous workshop), set the margin and padding properties of the `ul` element to zero (`margin:0`;`padding:0`) and set some padding for the `header` element (`padding:10px20.px`). Then check the menu changes in the browser.

```
مدل نمایش (Display Model)
```

The display model in `CSS` refers to how elements are shown and behave on the web page. This model determines how elements are placed next to each other and how they interact. The display model is set by the `display` property with various values. The values of this property are described below:

`block:` elements with `display:` `block` are shown as blocks and take the full width of the line. By default these elements start on a new line, and you can set `width` and `height` for them.

`Inline:` `inline` elements behave like words—that is, elements sit one after another and do not create a new line. These elements only take as much space as their content; so setting `width` and `height` for them has no effect. Also, assigning `margin` properties for the top and bottom of the element will not have an effect.

`Inline-block:` this mode is a mix of `block` and `inline`. `inline-block` elements can behave as blocks but sit in the current line. These elements can have width and height and take as much space as their content.

Table 9 Comparing `Block` and `Inline` elements in `CSS`

`Inline` elements`Block` elements

Property

Continue on the same row.

Always start on a new row.

Start on a new row

Only as wide as the element content. Even when width is set, it takes the whole row.

```
پهنا (width)
```

Usually only as tall as the content.

Can be set.

Height (`height`)

```
<span>, <a>, <b>, <i>
<div>, <p>, <h1>, <section>
```

Example elements

Several elements sit side by side.

Each sits on a separate line.

Behavior next to each other


---

**Page 130**

Using the `display` property with the values `block`, `Inline`, and `Inline-block`.

### Workshop

![Book image](../images/p136-02.png)

![Book image](../images/p136-01.png)

![Book image](../images/p136-03.png)

Box number 1 Box number 2 Each box sits on a separate row and the width of each equals the full width of the page.

Item number 1 Item number 2 Sit next to each other like words; you cannot set width and height.

Box `A`

Box `B`

The boxes sit next to each other; you can set width and height.


---

**Page 131**

Using the `display` property in designing a site login form

### Workshop

Create the `login.html` file in the `web` folder for user login to the site.

![Book image](../images/p137-02.png)

![Book image](../images/p137-01.png)


---
