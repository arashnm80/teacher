**Page 104**

`width` and `height:` These two attributes specify the width and height of page elements such as an image. The value of these attributes can be in pixels or percent. When the browser sees the expression `"width="100`, it sets the width of the element to 100 pixels. Therefore, to set the unit in percent, you must use an expression similar to `"width="100`. It is better to use `CSS` to set width and height in percent.

`title:` An explanatory text that appears when the mouse pointer is placed on the image.

Using the `img` tag

### Workshop

In the `products.html` file, display an image for each of the books.

To do this, in the `web` folder create a folder named `images` and place the book images inside it.

Using the `paint` software, set the image dimensions to 200×280. If necessary, increase the empty space around the product.

Then display the images after the book headings.

Turn each image into a link. Since the destination pages of the links do not exist, use the # symbol for the link destination. Then refresh the page by pressing the (`F5`) key.

![Book image](../images/p110-01.png)

![Book image](../images/p110-02.png)

1 General courses

2 Foundation courses

3 Non-technical competency courses

4 Technical competency courses


---

**Page 105**

### Learn more

Designing a table (`table`) A table is one of the tools for displaying data, because it makes it possible to display information in an orderly and understandable way. Today, tables are used to display various data such as product lists, prices, or any kind of information that needs organization.

To create a table in `HTML`, the `<table>` tag and its child tags are used as follows:

`<table>:` This tag marks the start and end of the table.

`<caption>:` Used to set the table title. This tag specifies the topic of the table for users and search engines.

`<tr>:` Used to define a row (`Row`) in the table.

`<th>:` Used to create a header cell (`Header`) in the header row. This tag improves the user experience.

`<td>:` Used to define a data cell (`Data` `Cell`) in the table.

The `<table>` tag has various attributes for setting the appearance of the table, which are mentioned below.

`rowspan:` For merging cells vertically.

`colspan:` For merging cells horizontally.

`thead` ,`tbody` ,`tfoot:` For semantic structuring.

### Try this

Research the `rowspan` and `colspan` attributes and their use in a table, and present the result in class with a project.

### Note

In `HTML5`, using the `border` attribute on the `<table>` tag is not allowed, and setting the style of the table lines must be done with `CSS`. Since the `CSS` topic is covered in the second competency unit, the `border` attribute is used only for temporary display of the lines.


---
