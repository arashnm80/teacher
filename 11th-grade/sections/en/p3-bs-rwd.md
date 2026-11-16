<!-- page 166 -->

> **Workshop**
>
> **Working with Bootstrap's responsive classes**
>
> In this workshop you will make changes to the page `index.html` using Bootstrap classes.
>
> **Part 1: using the row-cols classes**: in the previous workshop the column sizes were set with the col-sm-3 class. This class shows the columns side by side on devices wider than 576 pixels and stacks them (stack) on smaller devices.
>
> Bootstrap has another responsive class named row-cols that sets the number of columns (in each row) on different devices; the column size is set on the row element, not on the col elements. The table below shows how the two methods are used.
>
> | How the column size is set | Description |
> | --- | --- |
> | Setting the column size on the col elements | This code creates a row (row) with two columns (col-6). Each column takes half the width of the row (6 of 12). |
> | Setting the column size on the row element | The row-cols-2 class makes 2 columns in each row. The code above has 4 col elements, so two rows of two columns each are produced. If more col elements are added, the columns move to the next row. Bootstrap sets the column widths automatically, so you do not need to size each column by hand. |
>
> ![Book image](../images/p172-01.png)
>
> ![Book image](../images/p172-02.png)

<!-- page 167 -->

> **Workshop (continued)**
>
> 1. In the file `index.html`, add the code below after the newest products:
>
> ![Book image](../images/p173-01.png)
>
> Save the file and check the result in the browser. Then do the steps below and see the result after each step.
>
> 2. Use the classes border, border-4, and rounded-circle on all the images so that they are round with a border.
>
> 3. Add the mb-3 class to every col so that, in the mobile view, each image has some space from the image below it.
>
> 4. To set the image size, add the style in the figure below to the file `styles.css`.
>
> ![Book image](../images/p173-02.png)
>
> Put the title of each product inside an `<h3>` tag:
>
> ![Book image](../images/p173-03.png)
>
> 5. To set the size of the h3 text and its distance from the image above it, write the style in the figure below:
>
> ![Book image](../images/p173-04.png)

<!-- page 168 -->

> **Workshop (continued)**
>
> After finishing the steps above, you should get the output below in the desktop view.
>
> ![Book image](../images/p174-01.png)
>
> 6. To see how the images look on different devices, press f12. In the message window, choose Open Dev tools. As in the image below, choose the Toggle Device button in the toolbar at the top:
>
> ![Book image](../images/p174-02.png)
>
> 7. Choose the device type from the Dimension drop-down and look at the images.
>
> ![Book image](../images/p174-03.png)
>
> 8. If you like, choose Responsive from the drop-down and then change the device width by dragging its right edge.
>
> What the row-cols classes do in the workshop above:
>
> row-cols-sm-1: on devices 576 pixels or wider, the product images are shown in 2 columns.
>
> row-cols-lg-2: on devices 992 pixels or wider, the product images are shown in 4 columns.
>
> **Part 2: using the container classes**
>
> The container classes are responsive and give the container a different width on different devices.

<!-- page 169 -->

> **Workshop (continued)**
>
> **The container classes and their widths on different devices**
>
> | `XX-Large`<br>≤1400px | `X-large`<br>≤1200px | Large<br>≤992px | Medium<br>≤768px | Small<br>≤576px | Extra small<br>`<576px` |  |
> | --- | --- | --- | --- | --- | --- | --- |
> | 1320px | 1140px | 960px | 720px | 540px | 100% | `.Container` |
> | 1320px | 1140px | 960px | 720px | 540px | 100% | `.Container-sm` |
> | 1320px | 1140px | 960px | 720px | 100% | 100% | `.Container-md` |
> | 1320px | 1140px | 960px | 100% | 100% | 100% | `.Container-lg` |
> | 1320px | 1140px | 100% | 100% | 100% | 100% | `.Container-xl` |
> | 1320px | 100% | 100% | 100% | 100% | 100% | `.Container-xxl` |
> | 100% | 100% | 100% | 100% | 100% | 100% | `.Container-fluid` |
>
> در کارگاه «**طراحی بخش معرفی فروشگاه**» پهنای عنصر article در دستگاه دسکتاپ و موبایل به ترتیب 75% و 90% تعیین شد. در اینجا قصد داریم به‌جای استفاده از کدهای CSS از کلاس‌های واکنش‌گرای container استفاده کنیم. بدین منظور مراحل زیر را دنبال کنید:
>
> Use the container-sm class on the article element:
>
> ![Book image](../images/p175-01.png)
>
> Remove both styles of the article element from the file `styles.css`.
>
> Save the HTML and CSS files and check the result in the browser. With this change, the width of the article element on devices 576 pixels or wider is set by the container class, and on smaller devices the element is 100% wide.
>
> **Part 3: working with the display classes**
>
> In the workshop «**Designing the toolbar**», a toolbar was designed at the top of the page. Its «Sign up|Login» option and logo were hidden in the mobile view and put at the bottom of the page in a new bar named bottom-toolbar. The goal of this workshop is to hand control of showing/hiding the elements of the toolbar and bottom-toolbar bars to the `d-*` classes and remove their CSS code.

<!-- page 170 -->

> **Workshop (continued)**
>
> First add the classes d-flex and d-lg-none to the classes of the bottom-toolbar element:
>
> ![Book image](../images/p176-01.png)
>
> Remove display:none from the properties of the `.bottom-toolbar` element in the file `styles.css`.
>
> In the media rule, remove the selector `.bottom-toolbar`. Save the file and check the result in the browser.
>
> To hide the «Sign up|Login» element and the logo at widths below 992 pixels, add the classes d-none and d-lg-block to the signin-signup and logo elements in the toolbar element:
>
> ![Book image](../images/p176-02.png)
>
> After adding the `d-*` classes, remove the style below from the media rule.
>
> ![Book image](../images/p176-03.png)
>
> Save the file and check the result in the browser. On devices 992 pixels or wider you should see four elements, the logo, the search box, the «Login|Sign up» option, and the shopping cart; on smaller devices the logo and «Login|Sign up» should be hidden.
>
> To control the extra space around the toolbar, give the toolbar element the class p-3 and then remove the padding property from the toolbar class. Choose Responsive from the Dimension drop-down in the browser and check the result.
>
> ![Book image](../images/p176-04.png)
>
> **Part 4: creating a responsive image**
>
> The goal of this part is to add a banner above the toolbar element so that the banner image responds to the page width. For this, insert the image `top-banner.jpg` at the start of the `<header>` tag and use the img-fluid class on it:
>
> ```
> <img src="./images/top-banner.gif " class="img-fluid w-100">
> ```
>
> img-fluid is one of Bootstrap's important classes for making images responsive: it makes the image resize with its parent, never get wider than the container, and show correctly on phones, tablets, and desktops.

<!-- page 171 -->

> **Workshop (continued)**
>
> Of course, a responsive image is not just a matter of img-fluid. For images that take the full width, it is better to design another version of the image for smaller devices. In the example below, three versions of the banner image are used for phone, tablet, and desktop. The browser picks the right image based on the page width:
>
> ![Book image](../images/p177-01.png)
>
> Most modern browsers support the picture tag, so in modern browsers the images given in the `<source>` tags are shown. In old browsers such as Internet Explorer 11 and earlier, the default image appears. In the code above, the default image is given in the `<img>` tag.

> **Activity**
>
> Design three banner images at three sizes for phone, tablet, and desktop, and code how they are shown like the code above. You should get output like the figure below.
>
> ![Book image](../images/p177-02.png)

> **Attention**
>
> If the edges of the banner do not touch the edges of the browser, set the padding and margin of the header element to zero.

### اجزای رابط کاربری (User Interface Components)

Users interact with a web page through different components. These include buttons, menus, search bars, icons, forms, images, colors, fonts, and other visual elements that shape the user experience. Bootstrap has a set of ready-made classes for user interface components such as the navigation bar, forms, buttons, the accordion menu, and so on, which this part covers.

<!-- page 172 -->

**Navbar**: the navbar class is used to create a navigation bar (Navigation Bar), the menu at the top of the page. It is used with other classes such as `navbar-expand-*` to set how the navigation bar behaves and looks at different screen sizes. The Navbar classes are:

**navbar**: the main class for creating a navigation bar.

**`navbar-expand-*`**: these classes decide at what width the navigation bar is shown horizontally and at what width it collapses. The \* character can be replaced by sm, md, lg, or xl. For example, navbar-expand-sm makes the navigation bar horizontal on devices 576 pixels or wider, and on smaller devices it collapses into a hamburger button (☰).

**navbar-brand**: used to show the logo or brand name in the navigation bar.

**navbar-nav**: used to create the navigation list (Navigation list) in the navigation bar.

**nav-link**: used for the links in the navigation list.

**navbar-toggler**: used for the small menu button. This button appears in the mobile view so the user can click it to see the menu and click again to close it. (It creates a button that opens and closes the menu.)

**navbar-toggler-icon**: shows the hamburger icon (☰) on the menu button when collapsed.

**navbar-collapse**: used to group and hide the menu options on small devices.

**dropdown**: used to create drop-down menus in the navigation bar.

**navbar-light و navbar-dark**: برای تعیین رنگ محتوای نوار ناوبری استفاده می‌شود تا خوانایی عناصر درون آن حفظ شود. کلاس navbar-light موجب ایجاد یک نوار ناوبری با پس زمینه روشن و رنگ متن تیره می‌گردد و کلاس navbar-dark یک نوار ناوبری با پس‌زمینۀ تیره و متن‌های روشن ایجاد می‌کند. انتخاب صحیح این کلاس‌ها باعث افزایش خوانایی و بهبود تجربه کاربری می‌شود.
