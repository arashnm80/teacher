<!-- page 180 -->

Bootstrap has a set of ready-made classes for laying out all kinds of forms. With them you can build responsive, attractive forms quickly and with very little code. Table 12 contains some of the form classes in Bootstrap 5.

*Table 12: Form classes*

| Class name | Use |
| --- | --- |
| `form-control` | Styles input fields such as input, textarea, and select |
| `form-label` | Styles form labels |
| `form-check` | Styles check boxes and radio buttons |
| `form-check-label` | Used for the text next to a check box or radio button. |
| `form-check-input` | For styling a check box and radio button |
| `form-text` | Used to show a help text under a form field. |

> **Learn more**
>
> **Designing a sign-up form**
>
> ![Book image](../images/p186-02.png)
>
> In this workshop you will design a sign-up form like the one opposite with Bootstrap classes.
>
> 1. Create a web page named `signup-form.html` and write the basic code of an HTML document in it. Then add the charset, viewport, and title meta tags and the Bootstrap CDN link to the `<head>` part. Also set the direction of the page to rtl.
>
> ![Book image](../images/p186-01.png)

<!-- page 181 -->

> **Learn more (continued)**
>
> 2. The page `signup-form.html` shows only one form. It must appear in the middle of the page horizontally and vertically. So set the properties of the body tag as below:
>
> ![Book image](../images/p187-01.png)
>
> - vh is a CSS unit of measurement, short for Viewport Height. The viewport is the part of the page the user can see. 1vh equals 1% of the viewport height. So height:100vh means the `<body>` element must be 100% of the viewport height; in other words, it must take the full height of the page.
>
> - The d-flex and align-items-center classes put the content of the body in the middle of the page.
>
> 3. Inside the body element, create a container with the content in the figure below:
>
> ![Book image](../images/p187-02.png)
>
> 4. The width of the form must be controlled on different devices. For this it is best to use grid classes, so that the width of the form's container changes with the device size. In the code above, a container with the class row is created, with only one column in it holding the form and its title. Since the form is inside a grid column, its width changes with the width of the column.
>
> The justify-content-center class puts the content of the container in the middle of the page.
>
> The classes col-10, col-md-6, and col-lg-5 set the width of the grid column on phones, tablets, and desktops.

<!-- page 182 -->

> **Learn more (continued)**
>
> 5. Add the content of the form, following the code in the figure below, at the marked place in the code above:
>
> ![Book image](../images/p188-01.png)
>
> Save the file and check the result in the browser.
>
> 6. Change the color of the form title to blue and the color of the labels to gray, using Bootstrap classes.
>
> 7. Remove the underline of the «Login» link at the bottom of the page with a Bootstrap class.

> **Learn more**
>
> **Modal**: a modal is a user interface shown as a floating dialog box on top of the page that makes the user interact with it before going back to the web page. It is usually used to show extra information, confirmations, forms, or other interactions with the user. Pressing Esc, clicking the close button, or clicking outside the modal window closes the dialog box.
>
> A modal window has three parts: header, body, and footer. They are created with the classes `modal-header`, modal-body, and modal-footer. These three parts sit together inside a container with the class modal-content.
>
> A modal depends on JavaScript, so adding Bootstrap's JavaScript file before `</body>` is essential.
>
> To show the dialog box, a triggering element such as a button is needed.

<!-- page 183 -->

> **Learn more (continued)**
>
> ![Book image](../images/p189-03.png)
>
> ### The complete structure of a modal in Bootstrap

> **Workshop**
>
> **Showing a «product added to cart» message with a Modal**
>
> In earlier workshops you designed the product information page (`product-details.html`). In some shopping sites, when the user clicks «Add to cart», a message saying «The product has been added to your cart» is shown. In this workshop we will change the page `product-details.html` in the same way.
>
> Open the file `product-details.html` and change the add-to-cart button as in the code in the figure below:
>
> ![Book image](../images/p189-01.png)
>
> Clicking this button shows the dialog box (modal) with the ID addTocartMsg.
>
> btn: gives the `<button>` element the style of a Bootstrap button.
>
> `data-bs-toggle="modal"`: says that this button opens a modal.
>
> `data-bs-target="#addToCartMsg"`: says which modal opens.
>
> Add the modal code to the page after the `</button>` tag:
>
> ![Book image](../images/p189-02.png)

<!-- page 184 -->

> **Workshop (continued)**
>
> ![Book image](../images/p190-01.png)
>
> tabindex sets the order in which the focus moves between elements when the Tab key is used. `tabindex=-1` means the modal cannot get focus with the Tab key. btn-close styles the close button of the modal window as a cross.
>
> `data-bs-dismiss="modal"`: sets the behavior of the close button, so that the modal closes when the user clicks it.
>
> By default, the close button at the top of the modal window appears on the right of the window. That is why the classes d-flex, justify-content-end, and ms-0 are used to position it.
>
> After clicking the «View cart» button, the page `shopping-cart.html` must open. For this, use the button's onclick attribute and set its value to a JavaScript statement as in the figure below:
>
> ![Book image](../images/p190-02.png)

### Carousel

A carousel is a JavaScript-based tool used to create a set of slides or a horizontal image gallery. It lets several pieces of content or images be shown in a limited space, and users can see the next ones with the control buttons or by swiping (swipe). In a shopping site, carousels or sliders show a set of products or promotional content in rotation. Carousels give users a better experience. To create a Bootstrap carousel, the carousel class and its child classes are used. Table 13 lists the class names and what they do:
