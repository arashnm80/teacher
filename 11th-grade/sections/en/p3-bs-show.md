<!-- page 185 -->

*Table 13: Carousel classes*

| Class name | Use |
| --- | --- |
| Carousel | Used for the main container of the carousel, which holds all its parts. |
| Slide | Turns on the slide animation when the slides change. |
| `carousel-inner` | Used for the container of the slide elements. |
| `carousel-item` | Used for each slide of the carousel. The element with the class `carousel-item` holds the slide's content (images, text, and so on). |
| active | Marks which slide is being shown now. |
| `carousel-control-prev` | Used for the button that goes to the previous slide. |
| `carousel-control-next` | Used for the button that goes to the next slide. |
| `carousel-indicators` | Used to create the indicators on the slide: small circles that show how many slides there are and which one is being shown. |
| `carousel-caption` | Used to add text or captions to the carousel slides. |

> **Workshop**
>
> **Designing a carousel at the top of the shop page**
>
> In this workshop you will show several promotional banner images in a carousel.
>
> Save the promotional banner images as slide1, slide2, and slide3 in the project's images folder. Enter the code in the figure below in the file `index.html` at the start of the `<main>` tag:
>
> ![Book image](../images/p191-01.png)

<!-- page 186 -->

> **Workshop (continued)**
>
> Save the file and check the result in the browser.
>
> The control buttons have not been added to the carousel yet, so wait 5 seconds to see the next slide.
>
> The attribute `data-bs-ride="carousel"` turns on the carousel's automatic movement. It tells the carousel element to change slides after a certain time. How long each slide is shown can be set with the data-bs-interval attribute: for this, add `data-bs-interval="2000"` to the relevant tag.
>
> ![Book image](../images/p192-01.png)
>
> Add the code of the «Next» and «Previous» buttons at the marked place in the carousel code:
>
> ![Book image](../images/p192-02.png)
>
> `data-bs-target="#banners"`: says which Carousel this button controls.
>
> `data-bs-slide="prev"`: this attribute moves to the previous slide.
>
> The carousel-control-prev-icon class shows the left arrow icon () for the «previous slide» button.
>
> The visually-hidden class is used to hide the words Previous and Next from sighted users, but screen readers read the content of the `<span>` element to blind users. In fact, the `<span>` element with visually-hidden is written for blind users.
>
> The attribute `aria-hidden="true"` on the control buttons tells screen readers to ignore this element; it is not available to blind users.

### Accordion

The accordion is one of Bootstrap's useful components; it lets the developer show content in sections that open and close. The accordion is closed by default. Clicking the title of a section shows its content, and clicking again hides it. This is very useful for organizing long content and showing information compactly.

Accordions can be used in many parts of a design, such as navigation and drop-down menus, showing extra information about a section, building a frequently asked questions section, and so on.

<!-- page 187 -->

Several classes are used to design an accordion. Table 14 shows the class names and what each one does.

*Table 14: Accordion classes*

| Class name | Use |
| --- | --- |
| Accordion | Creates the main container of the accordion, which holds all its elements. |
| `Accordion-item` | An accordion has several sections (Item), each of which uses this class. Each section has a header and collapsible content. |
| `Accordion-header` | Creates the header of each section; it usually holds a button or link that shows or hides the content of that section when clicked. |
| `Accordion-button` | Sets the style of the button that is clicked. |
| `Accordion-collapse` | Used to style the element that holds the collapsible content. |
| `Accordion-body` | Creates the content shown in each section (Item). |
| Collapse | Used to open and close the content. |
| show | Shows the content of an element open. |

There must be one `<div>` element with the class accordion-item for each section of the accordion.

<!-- page 188 -->

> **Workshop**
>
> **Designing a frequently asked questions section**
>
> In the footer workshop, a frequently asked questions option was put in the first column. In this workshop you will design the page for this option.
>
> 1. Open the file `index.html` and choose Save As from the File menu. Name the new file `faq.html`. faq stands for Frequently Asked Questions.
>
> 2. Delete the whole content of the main element and write the accordion code inside it, following the code below:
>
> ![Book image](../images/p194-01.png)
>
> This accordion has two parts. Since the class show is used for the first part, the content of the first part will be shown.
>
> 3. By default the arrow next to each button is shown pointing up and next to the text of the button. To fix this, use the following style in the file `styles.css`:
>
> ![Book image](../images/p194-02.png)
>
> The selector accordion-button::after selects the element after the title of the button (the arrow icon).

<!-- page 189 -->

> **Activity**
>
> Add the third part to the accordion with the following content:
>
> If the item is on special sale, it includes a limit on the number of purchases. Otherwise there is no limit at all.
>
> It is expected that at the end you get the following output:
>
> ![Book image](../images/p195-01.png)

> **Activity**
>
> Link the frequently asked questions in the footer of the site to the file `faq.html`.
