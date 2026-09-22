**Page 98**

### Activity

Look at the content of the address bar in the two output display methods. What difference is there between them? Discuss it in class.

### Text elements on a web page

A web page contains various kinds of text elements, and each one is marked up with a specific tag. This section introduces the text elements of a web page.

Heading tags `<h1>` …`<h6>:`

Web pages contain different kinds of content. On a web page that holds a scientific or literary article, different headings are used to organize the content. Such headings appear less often on a store page, but they are useful for particular parts of the page.

![Book image](../images/p104-01.png)

To mark up headings on a web page, the tags `<h1>` through `<h6>` are used. The `<h1>` tag is used for the main topic of the page. The `<h2>` tag is used for headings under the main topic; these headings define the categories of the topics covered on the page, so they are highly important. The tags `<h3>` through `<h6>` are used for headings with more detailed topics.

**Figure 9**

General form of the heading tags

`</h1>` main page heading `<h1>` `</h2>` level `h2>` 2< heading `</h3>` level `h3>` 3< heading The `<h1>` heading is very important for search engines because it tells them the topic of the page. This heading should contain the keywords of the page topic. It is recommended that this heading be used only once on the page.

In general, the tags `<h1>` through `<h6>` define the hierarchy of topics on the page. By using these elements correctly, users can read the page content more easily and find the topics they want among the available content. In addition, search engines can more easily recognize the topics covered on the page and can store the web page information better in their database.

Proper heading of content has a significant effect on the web page’s ranking in search results.


---

**Page 99**

Applying the heading tags on the `test.html` page as in the figure below, apply the heading tags and

### Workshop

observe the result in the browser.

![Book image](../images/p105-01.png)

![Book image](../images/p105-02.png)

Network and software textbooks grade 10 textbooks computer systems maintenance computer services provider foundational technical knowledge computer technical drafting

The `<p>:` tag This tag is used to mark up paragraphs. Content placed between `<p>` and `<p/>` is separated from the content before and after it and is displayed on a new line. Inside `<p>` you can use plain text, a link `<a>`, bold `<b>` or `<strong>`

![Figure 10](../images/p105-03.png)

**Figure 10**

and so on.

The `<strong>` and `<b>:` tags To display a word in bold, you can use the two tags `<b>` and `<strong>`. The web browser displays the content of these two tags the same way, but search engines interpret them differently. If a phrase is marked up with the `<strong>` tag, it means that the content of this element is highly important and is related to the topic of the page. Screen reader tools (`Screen` `reader`) also read the content of the `<strong>` tag in a louder voice, whereas with the `<b>` tag they do not change their tone, because the `<b>` tag does not convey a particular meaning.

The `<em>` and `<i>:` tags To display a word in italics, the two tags `<em>` and `<i>` are used.

Although web browsers display the content of these two tags in a similar way, their meaning in `HTML` and their effect on search engines and content accessibility are different.


---

**Page 100**

The `<em>` tag: short for `Emphasis`, meaning emphasis. Using the `<em>` tag causes a phrase to be displayed differently and increases the readability of the text. This helps improve the user experience and as a result has a positive effect on the page’s SEO. Screen reader tools, when they encounter the `<em>` tag, change the tone of their voice to announce the importance of the tag’s content to blind users.

The `<i>:` tag which is short for `italic`, is used mostly for visual and aesthetic purposes, and search engines do not pay special attention to it. Screen reader devices also do not change their tone when they encounter the `<i>` tag.

Using the `<i>` and `<em>:` tags

![Book image](../images/p106-01.png)

Figure 11

The expression `"dir` `="trl` in the `<html>` tag is used to set the content display direction from right to left.

The code output will be as in Figure 12:

![Book image](../images/p106-02.png)

Figure 12


---

**Page 101**

List tags: List tags are used to organize and display information. These tags make it possible to view content in an orderly and understandable way. Using lists to organize content improves readability and makes the content more appealing to users, and as a result improves the user experience and ranking in search results.

![Book image](../images/p107-01.png)

Figure 13

Three types of list can be marked up in `HTML`: ordered, unordered, and description lists.

These lists are created with the tags `<ul>`, `<ol>`, and `<dl>`.

The `<ul>:` tag is short for `Unordered` `list`. This tag is used to create a bulleted list.

To mark up list items, the `<li>` tag is used.

Using the list tag:

### Workshop

Create a new file named `services.html`. Enter the code below in the `<body>` section and observe the result in the browser.

Create the file `products.html`, replace the `<ul>` tag with the `<ol>` tag, and write the list phrases from the figure below inside it. Save the file and observe the result in the browser.

![Book image](../images/p107-02.png)

![Book image](../images/p107-03.png)

Our services

Fast order shipping the most up-to-date bookstore shipping nationwide 24-hour support

The `<ol>:` tag is short for `Ordered` `list`. The `<ol>` tag is used to create numbered lists.


---

**Page 102**

![Book image](../images/p108-02.png)

![Book image](../images/p108-03.png)

Network and computer software field textbooks

With the highest discount, an enjoyable online shopping experience awaits you.

1 General courses

2 Foundation courses

3 Non-technical competency courses

4 Technical competency courses

Links (`links`): Links are like bridges between pages that guide users to the pages and resources they want.

![Book image](../images/p108-01.png)

To create a connection between pages, the `<a>` tag is used. This tag is short for `anchor` and means “anchor.” The `<a>` tag can guide the user to a web page, an image, a `pdf` file, and other items.

Figure 14

To create a link, the following general structure is used:

```
<a href="Resource address" target="target" title=" description"> anchor Text </a>
```

In the `href` attribute, the address of the destination page or file is written. The expression `href` is short for `Hypertext` `reference`.

The expression `anchor` `text` refers to the link text—what the user sees and clicks on.

If the user clicks the link text, they are guided to the resource address specified in the `href` attribute.

By default, the destination page of links opens in the current web page; as a result, the previous content of the page disappears.

To open the destination page in a new browser tab, the `target` attribute with the value `_blank` is used.

The default value of the `target` attribute is `_self`; this means that if the `target` attribute is not specified in the `<a>` tag, the link destination opens in the same page.

The `title` attribute contains a description about the link. This attribute is optional.

### Example

The following examples are samples of links to different resources:

`</a>` Ministry of Education website `<a` `href` = `"https://medu.ir">`

```
دانلود کتاب طراحی صفحات >"target="_blank "a href = "./pdfs/books/web-design.pdf<
```

`</a>` Web


---

**Page 103**

The destination of a link can be another point on the current page. In this case, the identifier (`ID`) of the destination element is written in the `href` attribute.

Make the following changes in the `test.html` page and observe the result in the browser.

### Workshop

![Book image](../images/p109-01.png)

![Book image](../images/p109-03.png)

New Reference

Provider of the latest edition of textbooks

### Adding images to a web page

Images are one of the important elements in the content of a page and can have deep effects on the appeal, communicability, and effectiveness of the page content. Using images on web pages can attract users’ attention so that they stay longer on the page. In addition, images play an important role in explaining and clarifying textual content, because they can convey information visually.

![Book image](../images/p109-02.png)

Figure 15

To display an image on a web page, the `<img>` tag is used. The general form of this tag is as follows:

```
<img src="URL" alt="Description" title=" " width="value" height="value" />
```

`src:` This attribute sets the address of the image.

`alt:` The word `alt` is short for `Alternative` `text`. The value of this attribute specifies the alternative text for the image.

This text is displayed if the image fails to load. In addition, the `Alt` value conveys the meaning and content of the image for the user and for search engines.


---
