<!-- page 104 -->

**width and height**: these two attributes set the width and height of page elements such as images. Their values can be in pixels or in percent. When the browser sees `width="100"`, it makes the element 100 pixels wide. So to give the size in percent you must use something like `width="100%"`. It is better to use CSS to set width and height in percent.

**title**: a descriptive text that appears when the mouse pointer is over the image.

> **Workshop**
>
> **Using the img tag**
>
> In the file `products.html`, show an image for each of the books.
>
> - To do this, create a folder named images in the web folder and put the book images in it.
>
> - With the paint program, set the size of the images to 280×200. If needed, add empty space around the product.
>
> - Then show the images after the book titles.
>
> - Turn each image into a link. Since the destination pages do not exist yet, use the # sign as the destination. Then refresh the page by pressing (F5).
>
> ![Book image](../images/p110-01.png)
>
> ![Book image](../images/p110-02.png)

<!-- page 105 -->

> **Learn more**
>
> **طراحی جدول (table)**
>
> Tables are one of the tools for presenting data, because they show information in an orderly, understandable way. Today tables are used to show many kinds of data, such as product lists, prices, or any information that needs organizing.
>
> To create a table in HTML, the `<table>` tag and its child tags are used as follows:
>
> **`<table>`**: marks the start and end of the table.
>
> **`<caption>`**: sets the title of the table. This tag tells users and search engines what the table is about.
>
> **`<tr>`**: defines a row (Row) of the table.
>
> **`<th>`**: creates a header cell (Header) in the header row. This tag improves the user experience.
>
> **`<td>`**: defines a data cell (Data Cell) in the table.
>
> The `<table>` tag has several attributes for setting the look of the table, described below.
>
> **rowspan**: merges cells vertically.
>
> **colspan**: merges cells horizontally.
>
> **thead، tbody، tfoot**: برای ساختاردهی معنایی.

> **Curiosity**
>
> Research the rowspan and colspan attributes and how they are used in tables, and present your findings in class with a project.

> **Note**
>
> In HTML5 the border attribute of the `<table>` tag is not allowed, and the style of the table's lines must be set with CSS. Since CSS is covered in the second learning unit, the border attribute is used here only to show the lines for now.
