<!-- page 132 -->

**Flexbox layout**

Flex is a CSS layout model used to create flexible, responsive, one-dimensional layouts. Flex can arrange page elements horizontally or vertically, and lets the developer align elements and share out space automatically. Layouts made with flexbox fit different screen sizes (Table 10).

### Setting the properties of the parent element

The flex model is used to arrange the child elements of an element horizontally or vertically. For this, the display property with the value Flex is used on the parent element. By default this lays out the children of the parent horizontally.

To turn on Flexbox, just add the property below to the parent element:

```
display: flex;
```

**flex-direction**: sets the direction in which elements are arranged, horizontally or vertically. Its values are given in Table 10.

*Table 10: The values of flex-direction and how they arrange elements*

| Value | row | `Row-reverse` |
| --- | --- | --- |
| **Description** | Horizontal (default)<br>`flex-direction:row`<br>box1 box2 box3 | Horizontal (right to left)<br>`flex-direction:row-reverse`<br>box3 box2 box1 |
| **Value** | **column** | `Column-reverse` |
| **Description** | Vertical, top to bottom<br>`flex-direction:column`<br>box1<br>box2<br>box3 | Vertical, bottom to top<br>`flex-direction:column-reverse`<br>box3<br>box2<br>box1 |

<!-- page 133 -->

**flex-wrap**: sometimes the page is not wide enough for all elements to sit side by side. flex-wrap decides whether extra elements move to the next line or are all squeezed into the same line (Table 11).

*Table 11: The values of flex-wrap*

| Value | wrap | nowrap |
| --- | --- | --- |
| **Description** | Move to the next line | Do not move to the next line |

**flex-flow**: flex-flow combines flex-direction and flex-wrap. Instead of writing two lines of code, you can set both properties in one line, as below:

```
.container{
       flex-flow: row wrap;
}
```

**justify-content**: controls the alignment of elements and how the empty space between them is shared along the main axis (Table 12).

*Table 12: The values of justify-content*

| Value | Description | Value | Description |
| --- | --- | --- | --- |
| `Flex-start` | Places the elements on the left | `Space-around` | Equal empty space around each element |
| `Flex-end` | Places the elements on the right | `Space-between` | Equal empty space between elements (the first and last touch the edges) |
| Center | Places the elements in the center | `Space-evenly` | Equal empty space between elements and also between the elements and the edges |

<!-- page 134 -->

**align-items**: ویژگی align-items در Flexbox برای تراز‌کردن عناصر در راستای محور متقاطع (عمود بر محور اصلی) استفاده می‌شود. به کمک این ویژگی می‌توان عناصر را در بالا، پایین و وسط یک سطر قرار داد (شکل 26).

![Figure 26](../images/p140-01.png)
*Figure 26*

*Table 13: The values of align-items*

| Value | Stretch | `flex-start` | `flex-end` | center |
| --- | --- | --- | --- | --- |
| **Description** | Stretched inside the parent element (default) | At the top of the parent element. | At the bottom of the parent element. | In the middle of the parent element. |

<!-- page 135 -->

### Laying out pages with Flexbox

> **Workshop**
>
> **Arranging the navigation menu with Flexbox**
>
> Open the file `index.html` and make the following changes:
>
> 1. Add the elements below inside the `<nav>` tag after the `</ul>` tag, and put the shopping cart icon and the text «Login | Sign up» in them:
>
> ![Book image](../images/p141-01.png)
>
> To get a shopping cart icon, go to `svgrepo.com` and search for shopping-cart. Choose a shopping cart you like, then click Edit vector to edit the image. Set the icon size to the minimum. Then click the Export button. An svg file is downloaded. Save it as `shopping-cart.svg` in the images folder.
>
> 2. Set the style of the navigation bar (.top-menu) as in the figure below:
>
> ![Book image](../images/p141-02.png)
>
> ![Book image](../images/p141-03.png)
>
> - display: flex turns the navigation bar into a flex container, so the items inside it (the menu list on the right and the user-action part on the left) are arranged horizontally.
>
> - `justify-content: space-between;` places the menu list and the user-actions part horizontally at the two ends of the container.
>
> - align-items: center centers the elements inside the flex container vertically.
>
> - max-width: 1200px sets the maximum width of the navigation bar to 1200 pixels, so it is not stretched too far on large screens.
>
> - margin:0 auto is used to put the menu bar area in the middle of the page.

<!-- page 136 -->

> **Workshop (continued)**
>
> 3. Set the style of the elements inside the `<ul>` tag as below:
>
> - display:flex is used to arrange the elements inside the `<ul>` tag horizontally, and justify-content shares out the space between the elements properly.
>
> - ویژگی margin-left:25px فاصله هر عنصر منو را از عنصر سمت چپ مشخص می‌نماید.
>
> ![Book image](../images/p142-01.png)
>
> ![Book image](../images/p142-02.png)
>
> 4. Set the style of the user-actions part as below:
>
> - display:flex shows the two elements «Login|Sign up» and the shopping cart side by side, and align-items:Center centers them vertically in the user-actions area.
>
> - The shopping cart image must be 25 pixels wide, and its left margin (margin-left) must be set to zero.
>
> ![Book image](../images/p142-03.png)
>
> ![Book image](../images/p142-04.png)

<!-- page 137 -->

> **Workshop (continued)**
>
> ![Book image](../images/p143-01.png)

### Creating the main part of the page

After designing the site's header, it is time to design the main content of the page, with the «Newest products» and «Special services» sections.

The `<main>` tag is used for the main part of the page. It must come after the `</header>` tag and before `</body>`.

The content of the «Newest products» and «Special services» areas must be inside the `<main>` element.

> **Workshop**
>
> **Designing the «Newest products» section with Flexbox**
>
> 1. Add a `<main>` tag after the `</header>` tag and put a `<section>` element in it: create a `<section>` element with the class container inside the `<main>` element. It must contain a heading (h2) and a container element (div) to hold the product cards. Write the heading «Newest products» inside the `<h2>` tag.
>
> 2. Give the `<div>` element the class products and put the product cards inside it. Create each product card with an element with the class product-card. Each card holds the product's image, title, and price.
>
> ![Book image](../images/p143-02.png)
>
> 3. So that the image, title, and price can be clicked together, put the whole content of the card inside an `<a>` tag. The column layout of the image, title, and price is set on the `<a>` element.
>
> ![Book image](../images/p143-03.png)
>
> Product card

<!-- page 138 -->

> **Workshop (continued)**
>
> ![Book image](../images/p144-01.png)
>
> Write the content of three more cards like the code on the previous page. Add the element styles to the page step by step and check the result of each change in the browser.
>
> max-width sets the maximum width of the container area.
>
> margin:20px auto centers the container horizontally on the page. display:flex arranges the cards in the products element with the flex technique.
>
> justify-content:center places the cards in the middle of the container area.
>
> flex-wrap:wrap changes the layout when the device gets narrower, so that product cards move to the next row.
>
> gap sets the space between the product cards.
>
> Since the «image, title, and price» group is inside the `<a>` element, the column layout of these elements is set with the selector `.product-card a`.
>
> flex-direction:column arranges the elements in a column.
>
> align-items:center aligns the elements along the vertical axis.
>
> ![Book image](../images/p144-02.png)
