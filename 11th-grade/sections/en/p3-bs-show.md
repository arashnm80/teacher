**Page 185**

Table 13 Carousel classes

Class name

### Use

Used for the main carousel container. The main container holds all the carousel

```
Carousel
```

components.

`Slide`

Enables the slide animation when the slides change.

```
carousel-inner
```

Used for the container of the slide elements.

Used for each slide in the carousel. An element that has the `carousel-item`

```
carousel-item
```

class holds the slide content (images, text, and so on).

```
active
```

Specifies which slide is currently being displayed.

```
carousel-control-prev
```

Used for the button that moves to the previous slide.

```
carousel-control-next
```

Used for the button that moves to the next slide.

Used to create indicators on the slide; small circles that show

```
carousel-indicators
```

how many slides there are and which slide is currently being displayed.

```
carousel-caption
```

Used to add text or captions to the carousel slides.

Designing the carousel at the top of the store page

### Workshop

In this workshop you will display several advertising banner images inside a carousel.

Save the advertising banner images with the names `slide1`, `slide2`, and `slide3` in the project images folder.

Enter the code in the figure below in the `index.html` file at the beginning of the `<main>` tag:

![Book image](../images/p191-01.png)


---

**Page 186**

Save the file and check the result in the browser.

At present the control buttons have not been added to the carousel, so wait 5 seconds to see the next slide.

The `"data-bs-ride="carousel` attribute is used to enable automatic movement of the carousel. This attribute tells the carousel element to change the slides after a set amount of time.

The display duration of each slide in the slider can be set with the `data-bs-interval` attribute. For this purpose, add `data-bs-interval="2000"` to the related tag.

![Book image](../images/p192-01.png)

Add the code for the “next” and “previous” buttons in the place marked in the carousel code:

![Book image](../images/p192-02.png)

`"data-bs-target="#banners:` Specifies which `Carousel` this button controls.

`"data-bs-slide="prev:` Moving to the previous slide is done with this attribute.

The `carousel-control-prev-icon` class: This class displays a left-arrow icon () for the “previous slide” button.

The `visually-hidden` class is used to hide the words `Previous` and `Next` from ordinary users, but screen readers read the content of the `<span>` element for blind users. In fact, the `<span>` element with the `visually-hidden` property is written for blind users.

The `"aria-hidden="true` attribute on the control buttons tells screen readers that this element should be ignored and is not available to blind users.

Accordion. The accordion is one of the useful Bootstrap components that lets the developer display content in sections that can open and close. By default the accordion is closed. When you click the title of each section, the related content appears, and with the next click it is hidden. This feature is very useful for organizing long content and showing information in a compact way.

An accordion can be used in designing various sections, such as a navigation and drop-down menu, showing extra information for a section, creating a frequently asked questions section, and so on.


---

**Page 187**

Various classes are used in designing an accordion. Table 14 shows the class names and the use of each one.

Table 14 Accordion classes

Class name

### Use

This class is used to create the main accordion container and holds all the accordion

```
Accordion
```

elements.

An accordion has several sections (`Item`), and each separate section uses this class.

```
Accordion-item
```

Each section includes a `header` and collapsible content.

This class is used to create the `header` in each section and usually includes a button or

```
Accordion-header
```

link that, when clicked, shows or hides the content related to that section.

```
Accordion-button
```

Sets the style of the button that is clicked.

```
Accordion-collapse
```

This class is used to set the style of the element that has collapsible content.

```
Accordion-body
```

This class is used to create the displayable content in each section (`Item`).

```
Collapse
```

Used for opening and closing the content.

`show`

This class makes the content of an element display in the open state.

The `<div>` element with the `accordion-item` class must be used once for each accordion section.


---

**Page 188**

Designing the frequently asked questions section

### Workshop

In the footer design workshop, the frequently asked questions option was placed in the first column. In this workshop you will design the page for this option.

1 Open the `index.html` file and from the `File` menu choose `Save` `As`. Set the name of the new file to

```
faq.html قرار دهید. کلمه faq مخفف Frequently Asked Questions است.
```

2 Clear the content of the `main` element completely and write the accordion code inside it according to the code below:

![Book image](../images/p194-01.png)

This accordion has two sections. Because the `show` class is used for the first section, the content of the first section will be displayed.

3 By default the arrow next to each button is shown pointing up and beside the button text.

To fix this, use the style below in the `styles.css` file:

![Book image](../images/p194-02.png)

The `accordion-button::after` selector selects the element after the button title (the arrow icon).


---

**Page 189**

### Activity

Add a third section to the accordion with the content below:

If the product is on special sale, there is a limit on the purchase quantity. Otherwise there is no limit.

You are expected to get the output below at the end:

![Book image](../images/p195-01.png)

### Activity

Link the frequently asked questions in the site footer section to the `faq.html` file.


---
