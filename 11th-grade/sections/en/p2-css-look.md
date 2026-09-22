**Page 121**

### Activity

Apply the text formatting properties to the elements in the `test.html` file and view the result in the browser.

### Styling element appearance (colors, backgrounds, opacity, and border)

`CSS` has various properties for setting element appearance. These properties are used to set text color, background color, background image, control the background image, opacity, and element borders. Some of these properties are described below.

`color` and `background-color:` used to set the text color and background of elements. For both properties above you can use a color name, a hexadecimal color code, or an `RGB` code.

### Example

In the example opposite, all three methods of setting a color value are used.

```
;color: blue
;background-color: #0000FF
;)0,0,255(background-color: rgb
```

`opacity:` element opacity is set with this property. The `opacity` value is a number between 0 and 1.

Low values of this property reduce the opacity of the element, and values near 1 increase the opacity of the element.

`background-image:` used to set the background image. To assign a value to this property, first write the word `url` and then the image name in parentheses.

### Example

As in the example opposite:

```
;)images/background.jpg/.(background-image:url
```

`background-repeat:` images that do not cover the width of the page are repeated. Use this property to set how the image is repeated or not repeated; it has various values such as `no-repeat`, `repeat-x`,

```
repeat-y و ... است.
```

`background-size:` sets the size of the background image. This property specifies at what dimensions the background image is shown inside the element. To cover the width of the page without repeating the image, use this property with the value `cover`.

`background-position:` used to set where the background image is shown, with various values such as `center`, `left`, `right`, `left` `top`, `right` `bottom`, and so on.


---

**Page 122**

`background-attachment:` if the background image is larger than the display area, you can show lower parts of the image by scrolling. To keep the image fixed while scrolling the page, use this property with the value `fixed`.

`border:` page elements can be shown with a border. Creating a border is done with the `border` property. The values of this property set, in order, the border thickness, border type, and its color.

```
;border: 1px solid gray
```

`border-radius:` use this property to round the corners; its value can be in pixels or percent:

```
;border-radius:10px
```

Styling element appearance (colors, backgrounds, opacity, and border)

### Workshop

In the `test.html` file, write the `HTML` code below and view the result in the browser. Then add the styles step by step so you understand the effect of each one on the page elements.

![Book image](../images/p128-02.png)

![Book image](../images/p128-01.png)

![Book image](../images/p128-03.png)


---

**Page 123**

In the `Paint` software, create a new file named `background.jpg` and save it in the `images` folder on the path of the `test.html` file. Set its dimensions to 50×50 pixels. Inside it create two hollow circles with a soft color (as in the image opposite) and save the file. This image is applied to the background of the `div` element.

![Book image](../images/p129-01.png)

Output

`CSS` selectors The element or set of elements for which a `CSS` style is written are called selectors. `CSS` has various types of selectors including simple, combined, pseudo-class, pseudo-element, and attribute selectors, which are covered in this section.

Simple selectors (`Simple`):

These selectors use tag names, IDs, classes, and the * symbol to select elements. Types of simple selectors are shown in Table 8:

Table 8 Types of simple selectors

Selector type

Function

Select page elements by tag name, such as `h2`, `p`, `table`, `body`, and so on

![Book image](../images/p129-02.png)

```
عنصر (Element)
```

![Book image](../images/p129-03.png)


---

**Page 124**

Select page elements by their ID: ID selectors start with the # symbol. These selectors select elements using their ID (`id`). For example, to select an element with the ID `test`, use the expression `test#`. The ID value of an element is specified in the `id` attribute. Each ID belongs to only one element and must not be repeated for other page elements. In the example below, the `test` selector belongs to the `<h2>` element.

![Book image](../images/p130-01.png)

ID (`Id`)

![Book image](../images/p130-02.png)

Select page elements by class name: class selectors start with the . symbol. These selectors select elements using their class name (`class`). A feature of the class selector is that it can select a set of elements with the same class name. For example, the `.class1` selector selects all page elements with the attribute `"class="class1`. In the example below, the two elements `<h1>` and `<p>` have the same class name, so the text color of both becomes blue and their font size becomes 18 pixels.

![Book image](../images/p130-03.png)

```
کلاس (Class)
```

![Book image](../images/p130-04.png)


---

**Page 125**

Selecting a group of elements: group selectors assign a set of `CSS` rules to several elements. In a group selector, element names are written with commas. In the example below, the expression `h1`, `h2`,`p` is a group selector.

![Book image](../images/p131-01.png)

```
گروهی(Group)
```

The rules above are applied to the `<h2<`, `>h1>`, and `<p>` tags. As a result, all of them become blue and centered.

![Book image](../images/p131-02.png)

Selecting all page elements with the * symbol:

In the example below, the outer margin (`margin`) and inner spacing (`padding`) on all page elements are set to zero.

```
سراسری (universal)
```

![Book image](../images/p131-03.png)

Combined selector (`Combinator`):

Combined selectors in `CSS` are used to define a structural and positional relationship between two or more selectors. For example, the child selector with the < symbol and the descendant selector using a space; elements written nested have a parent–child relationship. For example, the `li` element is a child of the `ul` element.

So to select `li` elements you use `ul` `li` or `ul` > `li`. Using the < symbol limits the effect to the direct children of an element.


---

**Page 126**

### Example

The image below shows an example of using a combined selector.

![Book image](../images/p132-01.png)

![Book image](../images/p132-02.png)

Output

Pseudo-class selectors (`Pseudo-class` `Selectors`) Pseudo-class selectors let you set element styles based on their state, position, or dynamic properties. Some of these selectors are activated by user actions. Pseudo-classes are written with the : symbol after the element name. Pseudo-class selectors are as follows:

`hover:` becomes active when the user moves the mouse pointer over an element.

`focus:` this event occurs when an element (usually form elements) becomes active and the user can interact with it.

`active:` becomes active when an element is in an active state—for example when the user clicks a button.

`:nth-child`() lets you select the children of an element based on their position.

`:frist-child` () is used to select the first child of an element.

`:last-child`() is used to select the last child of an element.


---

**Page 127**

Attribute selector (`Attribute` `selector`) The attribute selector selects elements based on their attributes. For example, to select text form elements use the selector `]"input[type="text`, and to select elements that have the `href` attribute use the selector `[href]`.

Working with types of `CSS` selectors (designing a menu)

### Workshop

Create a file named `index.html` and write the `HTML` code below inside it. Save the file and view the result in the browser. Then gradually add element styles to the `head` section and check the result of each style.

![Book image](../images/p133-01.png)

![Book image](../images/p133-03.png)

![Book image](../images/p133-02.png)

Output

### Activity

1 Next to each selector, write its type as a `comment`. Put the comment content inside the /* */ symbols.

2 What is the result of the `list-style` property with the value `none`?


---
