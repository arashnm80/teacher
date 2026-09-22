**Page 142**

### Media query (Media query)

A media query is a `CSS` technique that lets you set element properties based on various device features (such as screen size, resolution, orientation, and so on). This capability lets the developer optimize websites and web applications for different devices (such as mobile, tablet, and desktop).

Media queries are written with the `media@` directive in `CSS` and have the following structure:

```
{ (condition) media media-type and@
CSS rules
```

}

Using a media query to change the state of elements in the mobile view

### Workshop

Add the following styles to the end of the styles in the `index.html` file. Save the file and check the result in the browser.

```
{)max-width:600px( media@
```

![Book image](../images/p148-01.png)

```
{ .top-menu ul
```

Change the menu element layout from horizontal to

```
;flex-direction: column
```

vertical

```
;%width: 100
```

Take the full width for each list item

```
;text-align: center
```

Center the option text

}

```
{ .top-menu ul li
```

![Book image](../images/p148-02.png)

```
;margin-bottom: 10px
```

Set the vertical spacing between menu options

}

![Book image](../images/p148-03.png)

```
{ .user-actions
```

Hide the `user-action` area

```
;display: none
```

}

```
{ .services-grid
```

![Book image](../images/p148-04.png)

```
;grid-template-columns: 1fr
```

Create a single column

```
;gap: 30px
```

Increase the vertical spacing between options

}

```
{ .service-item
```

![Book image](../images/p148-05.png)

```
;max-width: 300px
```

Place the service items in the middle of the row

```
;margin: 0 auto
```

}

```
{.chat-widget
```

![Book image](../images/p148-06.png)

```
;display: none
```

Hide the chat widget logo

}

{

### Activity

To check how the media query works, move the right edge of the browser as far left as possible.

When the window width gets smaller, the menu options are arranged vertically. The `user-actions` area disappears and the special service images are arranged in a column.


---

**Page 143**

Competency assessment for styling web page appearance with `CSS`

Work performance standard: Using `CSS` methods, implement the appearance and complex layouts of websites according to standards and specified visual designs.

Score

Work conditions (tools, materials, equipment,

Tools

Results

Row

Steps

Standard (indicators/judgment/scoring)

Earned

time, place, and so on)

### Assessment

Possible

Correct use of all three methods (`External`, `Internal`, `Inline`) diagnosing and correcting

3

style conflicts following the standard order and priority correctly applying appearance changes to the intended element doing the work in several ways doing Try this activities observing installation by

Familiarity with methods of adding

a working computer or laptop, a code editor (`VS` `Code` or the student,

Correct use of all three methods (`External`, `Internal`, `Inline`) diagnosing and

1

`CSS`, managing them

similar), an up-to-date web browser, time 25 minutes,

Practical exercise

correcting style conflicts following the standard order and priority correctly applying appearance

2

visual observation on the intended element coding incomplete or incorrect performance of any of the work steps1 correctly perform text formatting using the related property.

Use the properties related to setting element appearance to set text color, background

3

color, background image, background image control, opacity, and element borders correctly doing the work in several ways doing Try this activities

a working computer or laptop, a code editor

Observing the written

2 Text formatting

code (`VS` `Code` or similar), an up-to-date web browser,

code

Correctly perform text formatting using the related property.

time 25 minutes

Coding

Use the properties related to setting element appearance to set text color, background

2

color, background image, background image control, opacity, and element borders correctly.

Incorrect or incomplete performance of any of the work steps1 setting page element styles based on the parent–child relationship between them using simple selectors correctly setting element styles based on their special states and properties using pseudo-class selectors ability

3

to select elements based on their properties using combined selectors doing the work in several ways doing Try this activities observing

Computer, browser for testing time 15 minutes, performance run

3

Working with selectors in `CSS`

Work in a practical class or computer lab.

Template, exercise

Setting page element styles based on the parent–child relationship between them as a group using simple selectors correctly setting element styles based on special

2

states and properties using pseudo-class selectors ability to select elements based on their properties using a combined selector using simple selectors1

```
عناصر معنایی (header, main, footer, section, article, nav) درست
```

be used correctly have a standard `HTML5` page do Try this activities do the work with other methods3 observing

Computer, browser for testing time 30 minutes, performance

4 Working with box models

run

Work in a practical class or computer lab.

```
عناصر معنایی (header, main, footer, section, article, nav) درست
```

template be used correctly have a standard `HTML5` page.2 incomplete performance of any of the steps1 side elements (`aside` `caption`) be added correctly images with captions be displayed correctly create a table with 2 rows and 2

3

columns create data-entry forms do Try this activities do the work by asking about other

methods

Element display models

Written

on the page

Computer browser for testing time 30 minutes,

Practical test

5

```
Flexbox-gride model
```

Work in a practical class or computer lab.

Observing side elements (`aside` `caption`) be added correctly images with captions be displayed correctly create data-entry forms 2

```
disply -
```

Instructor performance incomplete performance of any of the steps1


---

**Page 144**

Appropriate use of `div` and `span` for structuring explanations and documentation the code be complete explain the advantages of using semantic tags (such as `article`, `section`) observing

3

for SEO and accessibility do Try this activities do the work

Documentation

with other methods

Computer browser

and explanations

Completing the structure with

reference resources for code documentation

written

6

Appropriate use of `div` and `span` for structuring comments and documentation

non-semantic elements and documentation

15 minutes

Running the code be complete.2 page and correctness of the final display incomplete performance of any of the steps explain the advantages of using semantic tags (such as

1

`article`, `section`) for SEO and accessibility.

Meeting all non-technical competencies2

Non-technical competencies, safety, health, environmental considerations, and attitude:

Failure to meet any of the non-technical competencies1 Yes

Work assessment (competency to perform the work)

No

### Explanation:

1 Criterion for competency to perform the work:

Earn at least a score of 2 from steps 1, 2, 3, 4, and 5 (critical steps) Earn at least a score of 2 from the non-technical competencies, safety, health, environmental considerations, and attitude section Earn at least an average of 2 from the work steps

2 Definition of competency levels: Regardless of the level of professional qualification at which a work task is performed, in every workplace a certain quality of work may be expected. The competency level for performing the work is the basic assessment criterion.

Skill (level three): skilled and able to train and guide others, ability to plan and analyze, accountable for one’s own work, dealing with a wide range of tasks and activities Mastery (level four): expertise in performing the work and training others, creating innovation, adaptability, troubleshooting, guiding and advising others.
