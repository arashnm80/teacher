<!-- page 139 -->

> **Activity**
>
> Set the background color of the cards to `rgb(251, 248, 249)` and check the result.
>
> Add a few more cards and see how they are arranged.
>
> Make the browser as narrow as possible and check how the cards are arranged. As the space shrinks, do the cards move to the next row? Remove flex-wrap:wrap and check again what happens when the page gets narrower.
>
> Replace the value of justify-content with space-around and space-evenly and check how the products are arranged.

> **Learn more**
>
> **طرح‌بندی صفحه با چیدمان شبکه‌ای (Grid)**
>
> Unlike flex, which works in only one dimension (a row or a column), Grid lets you create rows and columns of content at the same time. With the grid system you have precise control over spacing and sizes. It is flexible and very useful for building orderly, responsive grid structures. To create a grid layout, the display property is used with the value grid. The number of columns is set with grid-template-columns, and the space between columns with gap.

> **Workshop**
>
> **Designing the «Special services» section with the Grid model**
>
> Make the following changes to the file `index.html` step by step.
>
> 1. Download five logo images like the figure below and save them in the site's images folder (images).
>
> 2. Create a `<section>` element with the class services-area for the «Special services» section. It must contain an `<h2>` element and a `<div>` container with the class services-grid. The `<div>` holds the special service items.
>
> 3. Create each special service item with a `<div>` element with the class service-item. These items sit side by side in several columns using the grid model.
>
> ![Book image](../images/p145-01.png)

<!-- page 140 -->

> **Workshop (continued)**
>
> 4. Each special service item has a logo image (img) and its title (p). Complete the HTML for the special services section like the code in the figure below:
>
> ![Book image](../images/p146-01.png)
>
> ![Book image](../images/p146-02.png)
>
> 5. Add the element styles to the page step by step and see the result in the browser. display: grid turns the services-grid element into a grid container, so all its direct children (service-item) become grid items that can be arranged in rows and columns.
>
> grid-template-columns with five auto values creates five columns whose width depends on the content of each column. With it, the logo images appear in five columns.
>
> gap:20px sets the space between the columns to 20 pixels.

<!-- page 141 -->

> **Workshop (continued)**
>
> ![Book image](../images/p147-01.png)

> **Learn more**
>
> **Positioning page elements with the position property**
>
> position is one of the most important properties for controlling where elements sit on the page. It is used to set an element's place relative to its parent or to other elements. It has the values static, relative, absolute, fixed, and sticky:
>
> **static**: all page elements have the default value static.
>
> **relative**: sets an element's place relative to its original position. To move the element from its original position, the top, left, right, and bottom properties are used.
>
> **absolute**: sets the element's position relative to its parent element.
>
> **fixed**: keeps an element in a fixed place.
>
> Show a chat-widget button image at a fixed position (30, 600). To do this, add the chat widget button image to the page at 45×45. Use paint to set the image size. Put the image before the `</main>` tag:
>
> ![Book image](../images/p147-02.png)
>
> Set the style of the image like the code opposite.
>
> ![Book image](../images/p147-03.png)
>
> The button image will be shown in the bottom right corner of the page.
>
> ![Book image](../images/p147-04.png)
