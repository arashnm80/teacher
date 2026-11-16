<!-- page 116 -->

## Learning unit 2

## Have you ever thought about this

How can you set the text color and background color of web page elements?

How can you lay out page elements with suitable spacing?

Can you transform the look of a site without changing its HTML structure?

How can you change the layout and style of page elements on different devices?

How does the visual appeal of a web page affect the user experience?

## By the end, the student is expected to

1. Know the different ways of writing CSS and their order of priority.

2. Be able to style text elements, including their font, size, color, weight, and alignment.

3. Be able to set the visual properties of elements, including color, background, opacity, border, and shadow.

4. Know the kinds of selectors (simple, combinator, pseudo-class, and attribute) and use them to select elements precisely and efficiently.

5. Understand the box model and be able to set the outer (margin) and inner (padding) spacing of elements.

6. Know what the Display property does and use it to control how elements are shown.

7. Be able to lay out page elements responsively with Flex and Grid.

8. Write CSS code readably with proper indentation, and use suitable, understandable comments for each of the page's styles.

## Performance standard

Using CSS, build and adjust the look and layout of web page elements according to the principles and standards of modern web design.

<!-- page 117 -->

## Styling a page with CSS

The previous unit showed how to design the structure of web pages with HTML tags. Pages built only with HTML have plain text, a white background, and default spacing and layout, so they have no visual appeal. To give a page an attractive, user-friendly look, CSS is needed to style its elements. CSS lets web developers manage the look and layout of page elements simply and flexibly.

CSS stands for Cascading Style Sheets; it is a language for styling and controlling the look of web pages. It lets web developers manage the look and layout of elements completely separately from the main structure of the page, which makes the site easier to maintain and update. With CSS you can set all kinds of styles for the elements of a website, such as text and background colors, shadows, borders, changes when the mouse is over an element, and so on.

![Figure 22](../images/p123-01.png)
*Figure 22*

### The structure of CSS

CSS is a set of rules made of selectors (selectors) and properties (properties). Each rule is usually written like this:

```
selector {
      property: value;
}
```

The Selector selects elements of the page. For example, to style paragraph elements the selector p is used, and to select all elements of the page the \* sign is used. A Property is something that can be given a value in CSS, such as color, font-size, and border. The Value is the value of the element's property.

<!-- page 118 -->

> **Example**
>
> In the example below, the background color of the h1 element is set to orange.
>
> ```
> h1 {
>       background-color: orange;
> }
> ```

### How to apply CSS to pages

There are three ways to create custom styles and apply them to page elements:

1. **Inline CSS**: the style of the elements is written inside the HTML tags.

> **Example**
>
> In the example below, the text and background colors of the h1 element are set inline:
>
> ![Book image](../images/p124-01.png)
>
> ```
> <h1 style=”color:blue; background-color:orange”> سلام دنیا! </h1>
> ```

2. **Internal CSS**:

- The styles are written inside the `<style>` tag in the `<head>` part.

- With inline styles, if an element is given many properties, its code becomes cluttered and hard to read. So internal or external CSS is used to manage styles better.

> **Example**
>
> The example below shows internal **CSS** for setting the properties of the h1 element:
>
> ```
> <head>
>       <style>
>                h1 {
>                      color: blue;
>                      background-color: pink;
>                }
>       </style>
> </head>
> ```

3. **External CSS**:

- With external CSS, the styles are put in a file with the CSS extension. This file needs no `<style>` tag; it only sets the styles of elements. The CSS file must be linked to the web page with the `<link>` tag so that its rules apply to the page's elements. The CSS file is linked to the HTML file in the `<head>` part:

```
<head>
      <link rel=”stylesheet” href=”./styles.css”>
</head>
```

<!-- page 119 -->

External CSS files are the best way to style medium and large projects. The main advantages of the external method are:

1. The CSS file is reusable; it can be linked to different pages of the site.

2. With CSS and HTML code separated, maintaining, updating, and debugging (Debug) the styles and the HTML code become easier.

3. Browsers can store external CSS files in their cache (cache), which helps pages load faster on later visits to the site.

The drawback of this method is that the CSS file must be loaded separately, which can slow down how quickly the page's styles load the first time.

For small exercises, such as styling a single element, you can use inline CSS. Internal styles suit small projects, and external styles suit medium, large, and complex projects.

## The priority of the kinds of styles

If different styles are written for one element, the order of priority is inline, then internal, then external. If an element has none of these styles, it uses the style of its parent element.

> **Workshop**
>
> **Checking the priority of styles on page elements**
>
> - Create a web page named `test-style.html`.
>
> - Create a CSS file named `styles.css`.
>
> ![Book image](../images/p125-01.png)
>
> - Set the content of the HTML and CSS files as in the image opposite.
>
> - Save the files and check the result in the browser.
>
> - The text color is set in all three styles, but the inline style's color (green) is applied to the text.
>
> - The background color is set only in the internal style, so the yellow background is applied to the h1 element.
>
> - The width of the element is set only in the external style, so the h1 element will be 200 pixels wide.
>
> ![Book image](../images/p125-02.png)

<!-- page 120 -->

### Comments (Comment) in CSS

- To add single-line or multi-line comments in CSS, the /\* \*/ marks are used, as in Figure 23.

```
/* this is a comment */
```

*Figure 23*

### Formatting text with CSS

CSS has a set of properties for formatting text. They let you set the font, font size, line height, text decoration, and so on. The properties of text elements are:

**font-family and font-size**: set the font and its size

**text-align**: sets the text alignment, with the values left, right, center, and justify

**text-shadow**: creates a shadow with any color and size. The general form of this property is:

```
text-shadow: offset-x offset-y blur-radius color;
```

*Figure 24*

Its values are, in order, the horizontal and vertical offset of the shadow, the amount of blur, and the color of the shadow.

**text-transform**: changing the form of the letters to capital, small and so on, with the values uppercase, lowercase, capitalize, none and …

**direction**: sets the direction of the text, with the values ltr and rtl for left-to-right and right-to-left

**line-height**: sets the vertical distance between lines of text. Its value includes the height of the letters (the font) plus the empty space above and below them.

**text-decoration**: sets text decoration, with the values none, underline, overline, and line-through. text-decoration with the value none removes the underline of a link.

**vertical-align**: vertical alignment of text, with the values top, bottom, baseline, and so on
