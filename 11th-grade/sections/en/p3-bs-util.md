**Page 151**

Bootstrap’s `margin` and `padding` classes Bootstrap has two sets of classes, `m`{`side`}`-size` and `p`{`side`}`-size`, for setting the space around and the extra space inside elements, which in `CSS` are set by the `margin` and `padding` properties. The `side` parameter determines the direction in which the margin or empty space is applied, and the `size` parameter determines the size of the margin or empty space. The sets of `m` and `p` classes and their meanings are shown in the table below:

Table 2- `margin` and `padding` classes in Bootstrap

`margin` classes `padding` classes

Meaning

```
m-size
```

`p-size` in all directions

```
m{t}-size
p{t}-size
```

top (`top`)

```
m{e}-size
p{e}-size
```

right side in `ltr` (`end`)

```
m{b}-size
p{b}-size
پایین(bottom)
m{s}-size
p{s}-size
```

left side in `ltr` (`start`)

```
m{x}-size
p{x}-size
```

left and right (`x` axis)

```
m{y}-size
p{y}-size
```

top and bottom (`y` axis)

The value of `size` is a number from zero to five. Each number in this range represents a specific distance in `px`.

Table 3 Values of the `size` parameter in the measurement unit `px`

Size in `Sizepx`

`4px`

1

`8px`

2

`16px`

3

`24px`

4

`48px`

5

The `size` parameter can also have the value `auto`. The word `auto` means automatic adjustment. Using `mx-auto` sets the left and right spacing of the element to equal values, so that the element is placed in the middle of its parent element.


---

**Page 152**

Using `margin` and `padding` classes

### Workshop

Continuing the previous workshop, add a `div` element with the following settings to the web page:

![Book image](../images/p158-01.png)

In the code above, the distance of the `<div>` element from the element above it is set to `24px` or (`mt-4`), and its left and right spacing is set automatically (`mx-auto`). Also, the extra space inside the element in all directions is set to `16px` (`p-3`).

```
کلاس‌های border، rounded و shadow
```

Bootstrap contains a set of classes about borders, corner rounding, and other elements. The `border` classes are used to create a border and set its color and thickness. The `rounded` classes are used to round corners, and the `shadow` classes are used to create shadows on elements. Table 4 introduces the types of `border`, `rounded`, and `shadow` classes.

Table 4 Types of `border`, `rounded`, and `shadow` classes

Shadow and its size

Corner rounding

Border color

Border and its thickness

```
border-primary
rounded
border-secondary
border
rounded-circle
-shadow-none shadow
border-success
border-1
rounded-pill
```

`sm`

```
danger-danger
border-2
rounded-top
shadow
border-info
border-3
rounded-bottom
shadow-lg
border-warning
border-4
rounded-start
border-light
border-5
rounded-end
border-dark
```

Table 5 Bootstrap classes for setting corner rounding size and border thickness

Size

Corner rounding amount

Border thickness

Border

`1px`

```
0px (no rounding)
1 rounded
1 border
```

`2px`

`2px`

```
2 rounded
2 border
```

`4px`

`3px`

```
3 rounded
3 border
```

`6px`

`4px`

```
4 rounded
4 border
```

`5px`

```
5 rounded
5 border
```


---

**Page 153**

In the set of `rounded` classes, the class `rounded-circle` is used to make an element fully round.

The condition for an element to become fully round is that its width and height are equal. The class `rounded-pill` is also used to round corners like a pill or capsule. The words `start` and `end` refer to the left and right sides of an element.

Using `border`, `shadow`, and `rounded` classes

### Workshop

Continuing the previous workshop, add two elements with the following settings to the page `test-bs.html`.

To create the rectangular box in the image below, write the following code:

![Book image](../images/p159-01.png)

To create a circular image, add a product image with equal dimensions to the page and set it as follows:

![Book image](../images/p159-02.png)

```
کلاس‌هایtypography
```

Bootstrap’s text classes are used to set font size and weight, alignment, list styles, and other items. Table 6 refers to some of the text classes.

Table 6 Bootstrap text classes

Text size

Weight

Text alignment

List style

Text decoration

```
fs-1 … fs-6
fw-bold
text-start
list-unstyled
text-decoration-none
```

`h1` … `h6`

```
fw-light
text-center
list-inline
text-capitalize
display-1 … display-4
fw-lighter
text-end
text-uppercase
```

The `*-fs` classes are used to set the font size of text elements from small (`fs-6`) to large (`fs-1`).

The classes `h1` through `h6` are used to set the size of heading tags.

The `*-display` classes are used to create large headings and attract the user’s attention and do not convey a special meaning.


---

**Page 154**

The class `list-unstyled` removes the default list style; that means the markers or numbers next to the item disappear and the value of `padding-left` becomes zero.

The class `list-inline` prepares list items for horizontal layout, provided that the list items have the class `-list` `inline-item`. This type of list is useful for simple menus and small navigations.

`felx` classes Bootstrap has various classes for designing page elements with the `Flexbox` technique. The flex system has two base classes named `d-flex` and `d-inline-flex` that are used for container elements. For example, a product introduction section needs a container element in which the products are placed flexibly next to each other. The table below introduces some flex classes based on different topics.

Table 7 `Flexbox` classes

Horizontal alignment of elements

Vertical alignment of elements

Layout direction

Wrapping to the next row

```
justify-content-start
align-items-start
flex-row
flex-wrap
justify-content-center
align-items-center
flex-row-reverse
flex-nowrap
justify-content-end
align-items-end
flex-column
flex-wrap-reverse
justify-content-between
align-items-baseline
flex-column-reverse
justify-content-around
justify-content-evenly
```

The `*-justify-content` classes are used to set the horizontal alignment of content in a container element. The first three classes align an element’s content to the left (`start`), center (`center`), and right (`end`). The next three classes determine how elements are distributed based on the space between them.

The `*-align-items` classes are used to set the alignment of elements along the vertical axis.

Using different classes in the product images layer

### Workshop

In this workshop you will change the code of the “Newest products” layer using Bootstrap classes as shown below.

1 Open the `index.html` file from work unit 1. Add the Bootstrap 5 `CDN` link and script code in the appropriate place.

2 In the `<main>` element, apply the following changes:

![Book image](../images/p160-01.png)


---

**Page 155**

```
3 استایل‌های مربوط به .products-section h2، .products و ویژگی margin در .products-section را
```

Remove them from the file `styles.css`.

![Book image](../images/p161-04.png)

Designing the store introduction section

### Workshop

In this workshop you will create a section with text content at the end of the store page. Use different Bootstrap classes to design this part.

In the file `index.html`, add the `<article>` tag as shown below before the `<main/>` tag:

![Book image](../images/p161-01.png)

Add the following headings and paragraphs inside the `<article>` tag:

![Book image](../images/p161-02.png)

Save the file and view the result in the browser.

Bootstrap version 3 had a class named `text-justify` that was used for justified text alignment (`justify`). This class does not exist in Bootstrap version 5. Therefore, to create justified text alignment in paragraphs, you need to add the custom class `text-justify` to the file `styles.css` using the code below:

![Book image](../images/p161-03.png)


---
