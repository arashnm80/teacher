**Page 132**

`Flexbox` layout Flex is a layout model in `CSS` used to create flexible, responsive, one-dimensional designs. Flex can create a horizontal or vertical layout for page elements; it also lets the developer align elements and distribute space automatically. Designs created with `flexbox` will adapt to different screen sizes (Table 10).

Setting parent element properties for horizontal or vertical arrangement of child elements In a given element, the flex model is used. To do this, the `display` property with the value `Flex` is applied to the parent element. By default this creates a horizontal layout for the children of the parent element.

To enable `Flexbox`, it is enough to add the following property to the parent element:

```
;display: flex
```

`felx-direction:` this property is used to set the direction of arranging elements, horizontally or vertically.

The values of this property are shown in Table 10.

Table 10 Values of the `flex-direction` property and their effect on how elements are arranged

Value`row`

```
Row-reverse
```

Horizontal (default)

Horizontal (right to left)

```
flex-direction:row
flex-direction:row-reverse
```

Explanation

`box3`

`box2`

`box1`

`box1`

`box2`

`box3`

Value`column`

```
Column-reverse
```

Vertical from top to bottom

Vertical from bottom to top

```
flex-direction:column
flex-direction:column-reverse
```

`box1`

`box3`

Explanation

`box2`

`box2`

`box3`

`box1`


---

**Page 133**

`felx-wrap:` sometimes the page width is not enough for all elements to sit next to each other. The `flex-wrap` property specifies whether extra elements move to the next row or all are squeezed into the same row (Table 11).

Table 11 Values of the `felx-wrap` property

Value`wrap`

```
nowrap
```

Explanation

Move to the next row

Do not move to the next row

`felx-folw:` the `flex-flow` property combines `flex-direction` and `flex-wrap`. Instead of writing two lines of code, you can set both properties in one line. As below:

```
{.container
;flex-flow: row wrap
```

}

`justify-content:` this property controls the alignment of elements and how empty space is distributed between elements along the main axis (Table 12).

Table 12 Values of the `justify-content` property

Value

### Explanation

Value

### Explanation

Arrange elements on the

Create equal empty space around each

```
Flex-start
Space-around
```

left

element

Arrange elements on the

Equal empty space between elements (the first and last

```
Flex-end
Space-between
```

right

elements stick to the edges)

Equal empty space between elements and also between

```
Center
```

Arrange elements in the center `Space-evenly`

elements and the edges


---

**Page 134**

`align-items:` the `align-items` property in `Flexbox` is used to align elements along the cross axis (perpendicular to the main axis). With this property you can place elements at the top, bottom, and middle of a row (Figure 26).

![Book image](../images/p140-01.png)

`box1`

`box2`

`box3`

`box1`

`box2`

`box3`

`box3`

`box2`

`box1`

`box1`

`box2`

`box3`

**Figure 26**

Table 13 Values of the `align-items` property

```
مقدارStretch
flex-start
flex-end
center
```

Stretched inside

Placed at the top of the parent

Placed at the bottom of the parent

In the middle of the parent

Explanation

the parent element

element.

element.

element.

(default)


---

**Page 135**

Page layout with `Flexbox` Setting the layout of navigation menu elements using `Flexbox`

### Workshop

Open the `index.html` file and make the following changes in it:

1 Add the following elements inside the `<nav>` tag after the `<ul/>` tag and place the shopping cart icon and the phrase “Login | Sign up” inside it:

![Book image](../images/p141-01.png)

To get a shopping cart icon, go to the site `svgrepo.com` and search for `shopping-cart`. Choose a shopping cart you like, then click `Edit` `vector` to edit the image. Set the icon size to the minimum value. Then click the `Export` button. An `svg` file is downloaded. Save this file as `shopping-cart.svg` in the images folder.

2 Set the style of the navigation bar (`.top-menu`) as in the figure below:

![Book image](../images/p141-02.png)

![Book image](../images/p141-03.png)

The `flex:` `display` property turns the navigation bar into a flex container so that the items inside it (the menu list on the right and the `user-action` section on the left) are arranged horizontally.

The ;`space-between:` `justify-content` property places the menu list and the `user-actions` section horizontally at the two ends of the container.

The `align-items:` `center` property makes the elements inside the flex container centered vertically.

The `max-width:` `1200px` property sets the maximum width of the navigation bar to 1200 pixels.

This setting keeps the navigation bar from stretching too much on large displays.

The `margin:0` `auto` property is used to center the menu bar area on the page.


---

**Page 136**

3 Set the style of the elements inside the `<ul>` tag as follows:

The `display:flex` property is used for horizontal layout of elements inside the `<ul>` tag, and the `justify-content` property distributes the space between elements appropriately.

The `margin-left:25px` property sets the distance of each menu element from the element on its left.

![Book image](../images/p142-01.png)

![Book image](../images/p142-02.png)

4 Set the style of the `user-actions` section as follows:

Using the `display:flex` property shows the two elements “Login|Sign up” and the shopping cart horizontally, and the `align-items:Center` property shows these elements centered vertically in the `user-actions` area.

The shopping cart image width should be 25 pixels and its left margin (`margin-left`) should be set to zero.

![Book image](../images/p142-03.png)

![Book image](../images/p142-04.png)


---

**Page 137**

Remove the background colors from the `top-menu` and `user-actions` classes so you get the result below

![Book image](../images/p143-01.png)

Creating the main section of the page After designing the site header section, it is time to design the main page content, including the “Newest products” and “Special services” sections.

To design the main section of the page, use the `<main>` tag. This tag must be placed after the `<header/>` tag and before `<body/>`.

The content of the “Newest products” and “Special services” areas must be inside the `<main>` element.

Designing the “Newest products” section using `Flexbox`

### Workshop

1 Insert a `<main>` tag after the `<header/>` tag and place a `<section>` element inside it. Create a `<section>` element with the class `container` inside the `<main>` element. This element should contain a heading (`h2`) and a container element (`div`) to hold the product cards. Write the title “Newest products” inside the `<h2>` tag.

2 Assign a class named `products` to the `<div>` element and place the product cards inside the `products` element. Create the product card with an element that has the class `product-card`. Each card contains the product image, title, and price.

![Book image](../images/p143-02.png)

3 So that the set of image, title, and price is clickable, place the entire card content inside an `<a>` tag. Decisions about the column layout of the product image, title, and price are made in the settings of the `<a>` element.

![Book image](../images/p143-03.png)

Product card


---

**Page 138**

![Book image](../images/p144-01.png)

Also write the content of three other cards like the code on the previous page. Gradually add element properties to the page and check the result of each change in the browser.

The `max-width` property sets the maximum width of the container area.

The `margin:20px` `auto` property centers the container element horizontally on the page.

The `display:flex` property distributes the cards in the `products` element using the flex technique.

The `justify-content:center` property distributes the cards in the center of the container area.

The `flex-wrap:wrap` property changes the layout of elements when the device width gets smaller, so that product cards move to the next row.

The `gap` property sets the spacing between product cards.

Because the set “product image, title, and price” is inside the `<a>` element, the column layout of these elements is set with the selector `.product-card` `a`.

The `flex-direction:column` property lays out the elements in a column.

The `align-items:center` property sets the alignment of elements along the vertical axis.

![Book image](../images/p144-02.png)


---
