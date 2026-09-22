**Page 160**

Page grid (`Grid` `Systems`) Bootstrap has a grid system named `Grid` that is created with `Flexbox` and makes it possible to divide the page width into 12 columns. Each cell in this grid can hold the content of part of the page. The `Grid` system makes it possible to group columns to create wider columns so that there is enough space to place content inside a column. The `Grid` system is responsive and, depending on the page size, rearranges the columns automatically.

![Book image](../images/p166-01.png)

Using grid classes (`rows` and `columns`) To create the rows and columns of the grid, the classes `row` and `col` are used. The class `row` causes the grid cells to be placed on a horizontal line and applies suitable spacing between them. The width of the columns is set automatically by the `size` parameter in the name of the `col` class. The general form of the `col` class is `-col` `breakpoint-size`; the `breakpoint` parameter refers to the device size (`sm`, `md`, `lg`,`xl`, `xxl`) and the size parameter refers to the column size. For example, `col-sm-3` means occupying three columns out of 12 on all devices larger than or equal to 576 pixels.

The grid of rows and columns must be placed inside a container element. Bootstrap has two classes named `container` and `container-fluid` that are used to create a container. The difference between these two containers is the amount of left and right margin. The class `container` creates an empty space of equal width on the left and right of the container element, while the class `container-fluid` occupies the full width of the page.

### Example

In the example below, a row with three columns is created in which each column’s share is 4 out of 12:

![Book image](../images/p166-02.png)

![Book image](../images/p166-03.png)


---

**Page 161**

The columns in the example on the previous page are displayed side by side on all devices. If instead of the class `col` the class `col-sm-4` is used, these columns will be side by side on all devices larger than or equal to 576 pixels, but on smaller devices they stack on top of each other.

The `breakpoint` and `size` parameters determine how the columns are displayed on different devices (mobile, tablet, desktop).

The `grid` system has various classes for column size on different devices, which are referred to in the table below:

Table 8 Parameters of the `-col` class for different devices

Parameter

### Usage

Explanation for very small devices page width less than 576 pixels `-col`

Without the prefix }`sm-`{`n` for small devices page width greater than or equal to 576 pixels `-col-sm` }`md-`{`n` for medium devices page width greater than or equal to 768 pixels `-col-md` }`lg-`{`n` for large devices page width greater than or equal to 992 pixels `-col-lg` }`xl-`{`n` for large devices page width greater than or equal to 1200 pixels `-col-xl` }`xxl-`{`n` for large devices page width greater than or equal to 1400 pixels `-col-xxl` {`n`} is a number from 1 to 12. By `n` is meant the number of columns that an element occupies out of the 12 `grid` columns.

### Example

__4 and 12 __8 is created:

In the example below, a row with two columns in two sizes 12

![Book image](../images/p167-01.png)

__4

These two columns are displayed side by side on devices with a width greater than or equal to 576 pixels with the sizes 12 __8. But on smaller devices, the content of the columns stacks and and 12 as a result each column will occupy 100% of the page width.

![Book image](../images/p167-02.png)

![Book image](../images/p167-03.png)

Device width: greater than or equal to 576 pixels Device width: less than 576 pixels


---

**Page 162**

### Example

To create dynamic and flexible layouts, you can use the classes above in combination. As in the example below:

![Book image](../images/p168-04.png)

These two columns are displayed one under the other on devices smaller than 576 pixels; on devices

__9 and 12 __3 and on devices

with a width greater than 576 pixels and smaller than 992 pixels in the size 12

__4 and 12 __8 are displayed.

larger with the size 12

Web page footer layout

### Workshop

In the file `index.html`, create the footer area as shown below after the `<main/>` tag:

![Book image](../images/p168-01.png)

For the content of the first column, use the following code:

![Book image](../images/p168-02.png)

The second column is for social network icons. To get the icon codes, go to the address `.icons` `getbootstrap.com` and at the end of this page, in the `CDN` section, copy the link to the icons `CSS` file and paste it in the `<head>` section. This link looks like the following:

![Book image](../images/p168-03.png)


---

**Page 163**

Then go back to the beginning of the icons page and, to search for an icon, type the name of the desired social network in the `ilterf` box. After the icons appear, click one of them as you prefer so that the icon’s dedicated page opens. In the `icon` `font` section, copy the `html` code and paste it in the second column of the footer. Set the content of the second column as follows:

![Book image](../images/p169-01.png)

In the third column, enter the code from the figure below:

![Book image](../images/p169-02.png)

In the fourth column, write the code from the figure below:

![Book image](../images/p169-03.png)

To remove the underline from links and set the color and size of the footer texts, add the style from the figure below to the file `styles.css`:

![Book image](../images/p169-04.png)

To set the style of the paragraph “All material and intellectual rights ....”, use the code from the figure below:

![Book image](../images/p169-05.png)


---

**Page 164**

This style displays the paragraph text in the center of the page with a line above it. The style above is applied only to the last paragraph, because only this paragraph is a direct child of the `footer` element.

To change the alignment of elements in the mobile view and move where the last paragraph is displayed, add the style from the figure below:

![Book image](../images/p170-01.png)

Because of the presence of `bottom-navbar` at the bottom of the page, it is not possible to see the final footer paragraph in the mobile view; for that reason, the position of the paragraph is set with the `position` and `bottom` properties.

After all elements are placed correctly in their positions, remove the background color of the columns.

Responsiveness and related classes Responsiveness means the ability of a web page to change and adapt to different sizes and features of devices and screens. In a responsive design, website elements automatically change their size and layout to suit the size of the user’s screen. The goal of doing a responsive design (`Responsive`) is to provide a better user experience for visitors. To design responsive elements, there are various methods as follows:

`Media` `query` 1: To set the properties of elements on different devices `Flexbox` 2: To manage how elements are arranged and the space between them `CSS` `Grid` 3: To organize elements in rows and columns

4 Using `max-width` instead of `width` so that images display correctly at different sizes:

![Book image](../images/p170-02.png)

5 Using relative units %, `rem`, and `em` instead of using fixed units (such as `px`)

6 Using frameworks such as Bootstrap that have ready-made responsive classes.


---

**Page 165**

### Try this

Research the units `rem` and `em`.

Bootstrap’s responsive classes cover various topics that are addressed in Table 9:

Table 9 Bootstrap responsive classes

Class type

Class names

```
Container
container و container-sm، container-md، container-lg و...
```

`Grid`

```
row، row-cols، col، col-sm، col-md و col-lg و...
d-flex، d-*-flex، d-*-inline، d-*-block start، d-*-none مانند زیر:
Layout
d-sm-none، d-md-block، flex-md-row، justify-content-sm-center
align-items-md- و...
Margin
m-*-size مانند mb-sm-3 و mx-sm-1
Padding
p-*-size مانند py-sm-3، px-lg-3
d-none ، d-block،d-*-none، d-*-block
Display Classes
```

`Image`

```
img-fluid
Components
button، form، navbar، cards، carousel و...
```

In the classes in Table 10, the * mark is equivalent to `sm`, `lg`, and so on.

```
جدول10 Breakpoints
کلاسBreakpoint
```

Page width less than `xs576` `px`

```
Extra small
```

`sm`

`Small`

576 `px` and more

`md`

```
Medium
```

768 `px` and more

`lg`

`Large`

992 `px` and more

`xl`

1200 `px` and more

```
Extra large
```

`xxl`

1400 `px` and more

```
Extra extra large
```


---
