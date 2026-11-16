<!-- page 128 -->

### مدل جعبه‌ای (Box Model)

The box model (Box Model) in CSS is used to design and lay out elements in web pages. Each HTML element is treated as a «box» with four parts: the content (content), the extra space inside the element (padding), the border (border), and the distance from neighboring elements (margin). These settings can be seen and examined in the example below: (Figure 25).

The width and height properties set only the width and height of the content area (content). So giving values to padding, margin, and border makes the final box bigger, and these values must be included when working out the box's size. To stop border and padding from affecting an element's width and height, the box-sizing property is used with the value border-box. Then the content, padding, and border together equal the width and height values, horizontally and vertically.

![Figure 24](../images/p134-01.png)
*Figure 24*

> **Workshop**
>
> **Examining the box model**
>
> Create a file named `box-model.html` and put two elements, `<div>` and `<img>`, with their styles in it:
>
> ![Book image](../images/p134-02.png)

<!-- page 129 -->

در فایل `index.html` (کارگاه قبل) ویژگی‌های مارجین و پدینگ عنصر ul را برابر صفر قرار دهید (`margin:0;padding:0(` و برای عنصر header مقداری پدینگ تنظیم کنید (`padding:10px 20px`) سپس تغییرات منو را در مرورگر بررسی کنید.

### مدل نمایش (Display Model)

The display model in CSS is about how elements are shown and behave in a web page. It decides how elements sit next to each other and interact. The display model is set with the display property and its different values, described below:

**block**: elements with display: block are shown as blocks and take up the full width of the line. By default they start on a new line, and you can set their width and height.

**Inline**: inline elements behave like words: they sit one after another and do not start a new line. They take up only as much space as their content, so setting width and height has no effect on them. Top and bottom margins do not take effect either.

**Inline-block**: a mix of block and inline. inline-block elements can behave like blocks but sit within the current line. They can have a width and height and take up as much space as their content.

*Table 9: Comparing Block and Inline elements in CSS*

| Inline elements | Block elements | Property |
| --- | --- | --- |
| Continue on the same line. | Always start on a new line. | Starting on a new line |
| Only as wide as the element's content. | Take the whole line even when a width is set. | Width (width) |
| Usually only as tall as the content. | Can be set. | Height (height) |
| `<span>, <a>, <b>, <i>` | `<div>, <p>, <h1>, <section>` | Sample elements |
| Several elements sit side by side. | Each sits on its own line. | Behavior next to each other |

<!-- page 130 -->

> **Workshop**
>
> به‌کارگیری ویژگی display با مقادیر block، Inline و Inline-block .
>
> ![Book image](../images/p136-01.png)
>
> ![Book image](../images/p136-02.png)

<!-- page 131 -->

> **Workshop**
>
> **Using the display property to design a site login form**
>
> Create the file `login.html` in the web folder for logging users in to the site.
>
> ![Book image](../images/p137-01.png)
