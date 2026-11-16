<!-- page 98 -->

> **Activity**
>
> Look at the address bar in the two ways of viewing the output. What is the difference? Discuss it in class.

## Text elements in a web page

A web page has different kinds of text elements, and each is marked up with a certain tag. This part introduces the text elements of a web page.

### Headings: the tags `<h1> …<h6>`

Web pages have many kinds of content. A page holding a scientific or literary article uses different headings to organize its content. Such headings are less common on a shopping page, but they are useful for certain parts of the page.

![Figure 9](../images/p104-01.png)
*Figure 9*

Headings of a web page are marked up with the tags `<h1>` to `<h6>`. The `<h1>` tag is used for the main topic of the page. The `<h2>` tag is used for the headings under the main topic, which group the topics on the page, so they are very important. The `<h3>` to `<h6>` tags are used for headings of more detailed topics.

### The general form of the heading tags

```
<h1> تیتر اصلی صفحه </h1>
<h2> 2 تیتر درجه  </h2>
<h3> 3 تیتر درجه  </h3>
```

The `<h1>` heading is very important to search engines, because it tells them the topic of the page. It should contain the keywords of the page's topic. It is recommended to use it only once per page.

In general, the `<h1>` to `<h6>` tags set the hierarchy of the page's topics. Used properly, they let users read the page more easily and find the topics they want among the content. Search engines also easily understand the topics of the page and can store the page's information better in their databases. Good headings have a noticeable effect on a page's rank in search results.

<!-- page 99 -->

> **Workshop**
>
> Using heading tags: in the page `test.html`, apply the heading tags as in the figure below and see the result in the browser.
>
> ![Book image](../images/p105-01.png)

**The `<p>` tag**: used to mark up paragraphs. The content between `<p>` and `</p>` is separated from the content before and after it and shown on a new line. Inside `<p>` you can use plain text, links `<a>`, emphasis `<b>` or `<strong>`, and so on.

![Figure 10](../images/p105-02.png)
*Figure 10*

**The `<strong>` and `<b>` tags**: to show a word in bold you can use either `<b>` or `<strong>`. Browsers show the content of the two tags the same way, but search engines interpret them differently. Marking a phrase with `<strong>` means its content is very important and related to the topic of the page. Screen readers (Screen reader) also read the content of `<strong>` louder, while they do not change their tone for `<b>`, because `<b>` carries no special meaning.

**The `<em>` and `<i>` tags**: to show a word in italics, the `<em>` and `<i>` tags are used. Although browsers show the content of the two tags the same way, their meaning in HTML and their effect on search engines and accessibility are different.

<!-- page 100 -->

**The `<em>` tag**: short for Emphasis. Using `<em>` makes a phrase look different and the text easier to read. This improves the user experience and so has a positive effect on the page's SEO. Screen readers also change their tone for `<em>`, telling blind users that its content is important.

**The `<i>` tag**: short for italic; it is used mostly for appearance and looks, and search engines pay no special attention to it. Screen readers do not change their tone when they meet `<i>`.

### Using the `<i>` and `<em>` tags

![Figure 11](../images/p106-01.png)
*Figure 11*

The attribute `dir="rtl"` in the `<html>` tag is used to show the content from right to left. The output of the code will be as in Figure 12:

![Figure 12](../images/p106-02.png)
*Figure 12*

<!-- page 101 -->

**List tags**: list tags are used to organize and present information. They let content be seen in an orderly, understandable way. Using lists to organize content makes it more readable and attractive for users, which improves the user experience and the rank in search results.

![Figure 13](../images/p107-01.png)
*Figure 13*

**HTML can mark up three kinds of lists**: ordered, unordered, and description lists.

These lists are created with the tags `<ul>`, `<ol>`, and `<dl>`.

- **The `<ul>` tag**: short for Unordered list. This tag creates a bulleted list. The `<li>` tag is used to mark the items of the list.

> **Workshop**
>
> **Using the list tag**:
>
> Create a new file named `services.html`. Type the code below in the `<body>` part and see the result in the browser.
>
> Create the file `products.html`, replace the `<ul>` tag with the `<ol>` tag, and write the list items from the figure below inside it. Save the file and see the result in the browser.
>
> ![Book image](../images/p107-02.png)

- **The `<ol>` tag**: short for Ordered list. The `<ol>` tag is used to create numbered lists.

<!-- page 102 -->

> **continued**
>
> ![Book image](../images/p108-02.png)

**پیوندها (links)**: پیوندها همانند پل ارتباطی میان صفحات هستند که کاربران را به صفحات و منابع مورد نظرشان هدایت می‌کنند.

![Figure 14](../images/p108-01.png)
*Figure 14*

- The `<a>` tag is used to link pages. Its name is short for anchor. The `<a>` tag can take the user to a web page, an image, a pdf file, and more.

- A link is created with the general structure below:

```
<a href="Resource address" target="target" title=" description"> anchor Text </a>
```

- The href attribute holds the address of the destination page or file. href stands for Hypertext reference.

- The anchor text is the text of the link, the part the user sees and clicks. When the user clicks the link text, they are taken to the address given in the href attribute.

- By default, the destination of a link opens in the current page, so the page's previous content disappears.

- To open the destination in a new browser tab, the target attribute is used with the value `_blank`. The default value of target is `_self`; that is, if target is not set in the `<a>` tag, the link opens in the same page.

- The title attribute holds a description of the link. It is optional.

> **Example**
>
> The examples below link to different resources:
>
> ```
> <a href = "https://medu.ir"> تارنمای وزارت آموزش و پرورش </a>
> ```
>
> `<a href = "./pdfs/books/web-design.pdf " target="_blank">` Download the web page design book `</a>`

<!-- page 103 -->

- The destination of a link can be another point in the current page. In that case the ID (ID) of the target element is written in the href attribute.

> **Workshop**
>
> Make the following changes in the page `test.html` and see the result in the browser.
>
> ![Book image](../images/p109-01.png)

## Adding images to a web page

Images are one of the important elements of a page's content and can strongly affect how attractive, engaging, and effective the content is. Images on web pages catch users' attention so that they stay on the page longer. Images also play an important role in explaining text content, because they can carry information visually.

![Figure 15](../images/p109-02.png)
*Figure 15*

- The `<img>` tag is used to show an image in a web page. Its general form is:

```
<img src="URL" alt="Description" title=" " width="value" height="value" />
```

**src**: sets the address of the image.

**alt**: alt stands for Alternative text. Its value is the replacement text of the image, which is shown if the image does not load. The Alt value also tells users and search engines what the image means and shows.
