<!-- page 160 -->

### Grid Systems

Bootstrap has a grid system named Grid, built with Flexbox, that divides the page width into 12 columns. Each cell of this grid can hold the content of part of the page. The Grid system lets you group columns into wider columns, so there is enough room for content in one column. The Grid system is responsive and rearranges the columns automatically depending on the page size.

![Book image](../images/p166-01.png)

### Using the grid classes (rows and columns)

The row and col classes are used to create the rows and columns of the grid. The row class puts the grid cells on one horizontal line with suitable spacing between them. The width of the columns is set by the size parameter in the col class name. The general form of the col class is `col-breakpoint-size`, where breakpoint is the device size (sm, md, lg, xl, xxl) and size is the column size. For example, col-sm-3 means taking three of the 12 columns on all devices 576 pixels or wider.

The grid of rows and columns must be inside a container element. Bootstrap has two classes, container and container-fluid, for creating containers. They differ in their left and right margins: the container class leaves equal empty space on the left and right of the container, while container-fluid takes the full width of the page.

> **Example**
>
> The example below creates a row with three columns, each taking 4 of the 12:
>
> ![Book image](../images/p166-02.png)

<!-- page 161 -->

> **Example (continued)**
>
> The columns in the example on the previous page are shown side by side on all devices. If col-sm-4 is used instead of col, these columns sit side by side on all devices 576 pixels or wider, but on smaller devices they are stacked. The breakpoint and size parameters decide how the columns are shown on different devices (phone, tablet, desktop).

The grid system has different classes for column sizes on different devices, listed in the table below:

*Table 8: The parameters of the col- class for different devices*

| Parameter | Use | Description |
| --- | --- | --- |
| No prefix | For extra-small devices: screen width less than 576 pixels | `col-` |
| `sm-{n}` | For small devices: screen width 576 pixels or more | `col-sm-` |
| `md-{n}` | For medium devices: screen width 768 pixels or more | `col-md-` |
| `lg-{n}` | For large devices: screen width 992 pixels or more | `col-lg-` |
| `xl-{n}` | For large devices: screen width 1200 pixels or more | `col-xl-` |
| `xxl-{n}` | For large devices: screen width 1400 pixels or more | `col-xxl-` |

{n} is a number from 1 to 12: the number of the grid's 12 columns that an element takes up.

> **Example**
>
> The example below creates a row with two columns of the sizes 4/12 and 8/12:
>
> ![Book image](../images/p167-01.png)
>
> On devices 576 pixels or wider, these two columns are shown side by side with the sizes 4/12 and 8/12. On smaller devices the contents of the columns are stacked, so each column takes 100% of the page width.
>
> ![Book image](../images/p167-02.png)
>
> ![Book image](../images/p167-03.png)
>
> **Device width: 576 pixels or more** (first image) — **Device width: less than 576 pixels** (second image)

<!-- page 162 -->

> **Example**
>
> To build dynamic, flexible layouts, the classes above can be combined, as in the example below:
>
> ![Book image](../images/p168-04.png)
>
> These two columns are stacked on devices narrower than 576 pixels; on devices wider than 576 and narrower than 992 pixels they are shown at 9/12 and 3/12, and on larger devices at 4/12 and 8/12.

> **Workshop**
>
> **Laying out the web page footer**
>
> In the file `index.html`, create the footer area after the `</main>` tag as below:
>
> ![Book image](../images/p168-01.png)
>
> For the content of the first column, use the code below:
>
> ![Book image](../images/p168-02.png)
>
> The second column holds the social network icons. To get the icon code, go to `icons.getbootstrap.com`, and at the bottom of that page, in the CDN section, copy the link of the icons' CSS file and paste it into the `<head>` part. The link looks like this:
>
> ![Book image](../images/p168-03.png)

<!-- page 163 -->

> **Workshop (continued)**
>
> Then go back to the top of the icons page and type the name of the social network you want in the filter box. When the icons appear, click one you like to open its own page. In the icon font section, copy the html code and paste it into the second column of the footer. Set the content of the second column as below:
>
> ![Book image](../images/p169-01.png)
>
> In the third column, enter the code in the figure below:
>
> ![Book image](../images/p169-02.png)
>
> In the fourth column, write the code in the figure below:
>
> ![Book image](../images/p169-03.png)
>
> To remove the underline of the links and set the color and size of the footer text, add the style in the figure below to the file `styles.css`:
>
> ![Book image](../images/p169-04.png)
>
> To style the paragraph «All rights reserved ....», use the code in the figure below:
>
> ![Book image](../images/p169-05.png)

<!-- page 164 -->

> **Workshop (continued)**
>
> This style shows the paragraph text in the middle of the page with a line above it. It applies only to the last paragraph, because only this paragraph is a direct child of the footer element.
>
> To change the alignment of the elements in the mobile view and move the last paragraph, add the style in the figure below:
>
> ![Book image](../images/p170-01.png)
>
> Because the bottom-navbar is at the bottom of the page, the footer's last paragraph cannot be seen in the mobile view; that is why the paragraph's position is set with the position and bottom properties.
>
> Once all the elements are in the right places, remove the background color of the columns.

### Responsiveness and the related classes

Responsiveness is a web page's ability to change and adapt to the sizes and features of different devices and screens. In a responsive design, the website's elements change their size and layout automatically to suit the user's screen. The goal of responsive (Responsive) design is a better experience for visitors. There are several ways to design responsive elements:

1. Media query: to set the properties of elements on different devices

2. Flexbox: to manage how elements are arranged and the space between them

3. CSS Grid: to organize elements in rows and columns

4. Using max-width instead of width so that images are shown correctly at different sizes:

![Book image](../images/p170-02.png)

5. Using the relative units %, rem, and em instead of fixed units (such as px)

6. Using frameworks such as Bootstrap that have ready-made responsive classes.

<!-- page 165 -->

> **Curiosity**
>
> Research the rem and em units.

Bootstrap's responsive classes cover several topics, shown in Table 9:

*Table 9: Bootstrap's responsive classes*

| Kind of class | Class names |
| --- | --- |
| Container | container, container-sm, container-md, container-lg, and so on |
| Grid | row, row-cols, col, col-sm, col-md, col-lg, and so on |
| Layout | d-flex, d-\*-flex, d-\*-inline, d-\*-block, for example: d-sm-none, d-md-block, flex-md-row, justify-content-sm-center, align-items-md-start, and so on |
| Margin | m-\*-size, such as mb-sm-3 and mx-sm-1 |
| Padding | p-\*-size, such as py-sm-3, px-lg-3 |
| Display Classes | d-none, d-block, d-\*-none, d-\*-block |
| Image | `img-fluid` |
| Components | button, form, navbar, cards, carousel, and so on |

In the classes of Table 10 the sign \* is equal to sm, lg and so on.

*Table 10: Breakpoints*

| Screen width | Class | Breakpoint |
| --- | --- | --- |
| Less than 576 px | xs | Extra small |
| 576 px and more | sm | Small |
| 768 px and more | md | Medium |
| 992 px and more | lg | Large |
| 1200 px and more | xl | Extra large |
| 1400 px and more | xxl | Extra extra large |
