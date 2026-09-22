**Page 139**

### Activity

Set the background color of the cards to the value `rgb`(251, 248, 249) and check the result.

Add a few more cards to the set of cards and observe how the cards are laid out.

Reduce the browser width as much as possible and check the layout of the cards. When space decreases, do the cards move to the next row? Remove the `flex-wrap:wrap` property and again check the result of reducing the page width.

Replace the value of the `justify-content` property with `space-around` and `space-evenly` and check the result of arranging the products.

### Learn more

Page layout with grid layout (`Grid`) Unlike the `flex` model, which works in only one dimension (row or column), the `Grid` model lets you create rows and columns that hold content at the same time. Using the `grid` system, you can have precise control over spacing and sizes. This method is flexible and very useful for creating regular, responsive grid structures. To create a grid layout, use the `display` property with the value `grid`. The number of grid columns is set by the `grid-template-columns` property and the spacing between columns by the `gap` property.

Designing the “Special services” section using the `Grid` model

### Workshop

In the `index.html` file, apply the following changes gradually.

1 Download five logo images as in the figure below and save them in the site images folder (`images`).

2 Create a `<section>` element with the class `services-area` for the “Special services” section. This element should contain an `<h2>` element and a container `<div>` with the class `services-grid`. The `<div>` element holds the special service items inside it.

3 Create each special service item with a `<div>` element that has the class `service-item`.

These items are placed next to each other in several columns using the grid model.

![Book image](../images/p145-01.png)


---

**Page 140**

4 Each special service item includes a logo image (`img`) and its title (`p`). Complete the `HTML` code of the special services section like the code in the figure below:

![Book image](../images/p146-01.png)

![Book image](../images/p146-02.png)

5 Gradually add element styles to the page and view the result in the browser.

```
ویژگی display: grid عنصر services-grid را
```

turns it into a grid container. As a result, all of its direct children (`service-item`) become grid items and can be distributed in rows and columns.

```
ویژگی grid-template-columns با پنج
```

`auto` values creates five columns whose width depends on the content of each column. With this property the logo images appear in five columns.

The `gap:20px` property sets the spacing between columns to 20 pixels.


---

**Page 141**

![Book image](../images/p147-01.png)

### Learn more

Positioning page elements with the `position` property The `position` property is one of the most important properties for controlling how elements are placed on the page. This property is used to set the position of an element relative to parent elements or other elements. The `position` property has the values `static`, `relative`, `absolute`, `fixed`, and `sticky` as follows:

`static:` all page elements have the default value `static`.

`relative:` sets the position of an element relative to its initial position. To move the element relative to its initial position, use the `top`, `left`, `right`, and `bottom` properties.

`absolute:` sets the position of the element relative to the parent element.

`fxied:` keeps the position of an element fixed.

Display the image of a `chat-widget` button fixed at position (30, 600). To do this, add the chat widget button image at 45×45 to the page. Use the `paint` program to set the image size. Place the image before the `<main/>` tag:

![Book image](../images/p147-02.png)

Set the image style like the code opposite.

![Book image](../images/p147-03.png)

This button image will be shown in the bottom-right corner of the page.

![Book image](../images/p147-04.png)


---
