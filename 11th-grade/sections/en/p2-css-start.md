# Styling web page appearance with CSS


---

**Page 116**

## Learning unit 2

## Styling web page appearance with CSS

### Have you ever thought

How can you set the text color and background of web page elements?

How can you arrange page elements with appropriate spacing?

Can you change the look of a site without changing the `HTML` structure?

How can you change the layout and style of page elements on different devices?

What effect does the visual appeal of a web page have on the user experience?

### By the end, the student is expected to

1 Know the different ways to define `CSS` and the order in which they are applied.

2 Be able to set text element styles including font type, size, color, weight, and alignment.

3 Be able to set visual properties of elements including color, background, opacity, border, and shadow.

4 Know simple, combined, pseudo-class, and attribute selectors and use them to select elements precisely and efficiently.

5 Be familiar with the box model and be able to set the internal (`padding`) and external (`margin`) spacing of elements.

6 Know what the `Display` property does and use it to control how elements are shown.

7 Be able to create responsive layouts of page elements using `Flex` and `Grid`.

8 Write `CSS` code in a readable way with proper indentation and use clear, understandable comments for each page style.

### Performance standard

Using `CSS` features, implement and adjust the appearance and layout of web page elements according to modern web design principles and standards.


---

**Page 117**

### Beautifying a page with CSS

In the previous work unit, you learned how to design the structure of web pages using `HTML` tags.

Pages created with `HTML` alone have plain text, a white background, and default spacing and layout, so they lack visual appeal. To create a beautiful, user-friendly look, you need `CSS` to style the elements. This tool lets web developers manage the appearance and layout of page elements simply and flexibly.

`CSS` stands for `Cascading` `Style` `Sheets` and is a language for styling and controlling the appearance of web pages.

This language lets web developers manage the appearance and layout of elements completely separately from the main page structure. That makes it easier to maintain and update the site. With `CSS` you can set many styles for different website elements—for example text and background colors, shadows, borders, appearance changes when the mouse is over elements, and more.

![Book image](../images/p123-01.png)

Page output with

Page output without

**Figure 22**

`CSS` structure `CSS` is a set of rules made of selectors (`selectors`) and properties (`properties`). Each rule is usually written as follows:

```
{ selector
;property: value
```

}

The word `Selector` means the selector and is used to choose page elements. For example, to style paragraph elements you use the `p` selector, and to select all page elements you use the * symbol. `Property` refers to the assignable properties in `CSS`, such as `color`, `font-size`, and `.border`. `Value` refers to the value of the element property.


---

**Page 118**

### Example

In the example below, the background color of the `h1` element is set to `orange`.

{ `h1`

```
;background-color: orange
```

}

How to use `CSS` in pages To create and apply custom styles to page elements, you use three methods as follows:

1 Inline `CSS` (`Inline`): Element styles are written inside `HTML` tags.

### Example

In the example below, the text color and background of the `h1` element are set inline:

![Book image](../images/p124-01.png)

```
</h1> سلام دنیا! >”h1 style=”color:blue; background-color:orange<
CSS 2 داخلی (Internal):
```

Element styles are written inside a `<style>` tag in the `<head>` section.

With inline style, if you assign many properties to an element, the element code becomes crowded and hard to read. So internal or external `CSS` is used for better style management.

### Example

The example below is a sample of internal `CSS` for setting `h1` element properties:

```
<head>
<style>
```

{ `h1`

```
;color: blue
;background-color: pink
```

}

```
</style>
</head>
CSS 3 خارجی (External):
```

In the external `CSS` method, element styles go in a file with a `CSS` extension. The content of this file does not need a `<style>` tag; only the styles of the elements are defined in it. The `CSS` file must be attached to the web page with a `<link>` tag so that the rules in this file apply to the page elements. Attaching the `CSS` file to the `HTML` file is done in the `<head>` section:

```
<head>
<link rel=”stylesheet” href=”./styles.css”>
</head>
```


---

**Page 119**

Using external `CSS` files is the best styling method in medium and large projects. The most important advantages of the external method are:

1 The `CSS` file can be reused—that is, it can be attached to different pages of the site.

2 With `CSS` and `HTML` code separated, maintaining, updating, and debugging (`Debug`) styles and `HTML` code becomes easier.

3 Browsers can store external `CSS` files in their cache (`cache`), which helps pages load faster on later visits to the site.

The disadvantage of this method is that the `CSS` file must be loaded separately, which may slow down the loading of page element styles on the first load.

For small exercises that only style one element, you can use inline `CSS`. Internal style suits small projects, and external style suits medium, large, and complex projects.

### Priority of applying style types

If different styles are written for one element, the order of applying styles is inline, then internal, then external. If an element has none of these styles, it uses the style of its parent element.

Examining the priority of applying style to page elements

### Workshop

Create a web page named `test-style.html`.

Create a `CSS` file named `styles.css`.

![Book image](../images/p125-01.png)

Set the contents of the `HTML` and `CSS` files as shown in the image opposite.

Save the files and check the result in the browser.

In all three styles the text color is specified, but the inline style color (green) is applied to the text.

The background color is set only in the internal style, so the yellow background color is applied to the `h1` element.

![Book image](../images/p125-02.png)

The element width is only in the external style

Output

specified, so the width of the `h1` element will be 200 pixels.

![Book image](../images/p125-03.png)


---

**Page 120**

Comments (`Comment`) in `CSS` To add single-line or multi-line comments in `CSS`, use the /* */ symbols as in Figure 23.

```
/* this is a comment */
```

**Figure 23**

How to format text in `CSS` `CSS` has a set of properties for formatting text. These properties let you set the font, font size, line height, text decorations, and more. Text element properties are as follows:

`font-family` and `font-size:` set the font type and size

`text-align:` set text alignment with values `left`, `right`, `center`, and `justify`

`text-shadow:` create a shadow with the color and size you want. The general structure of this property is as follows:

```
;text-shadow: offset-x offset-y blur-radius color
```

**Figure 24**

The values of this property are, in order, the horizontal and vertical shadow offset, the blur amount, and the shadow color.

`text-transform:` change letter case to uppercase, lowercase, and so on, with values `lowercase`, `upper`

```
cas، capitalize none،…
```

`direction:` set the text display direction, with values `ltr` and `rtl` for left-to-right and right-to-left

`line-height:` set the vertical spacing between text lines. This property sets the vertical spacing of the text line. The value of this property includes the height of the letters plus the empty space before and after them. It includes the height of the letters (font) plus the empty space before and after them.

```
text-decoration: تعیین تزیینات متن، شامل مقادیر none، underline، overline، .line-through
```

The `text-decoration` property with the value `none` removes the underline from a link.

`vertical-align:` vertical text alignment, with values `top`, `bottom`, `baseline`, and so on.


---
