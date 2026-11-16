<!-- page 111 -->

**`<section>`**: divides the content of the page into sections (Figure 18).

![Figure 18](../images/p117-01.png)
*Figure 18*

![Book image](../images/p117-03.png)

**`<article>`**: holds a self-contained, complete piece of content, such as blog posts (each post in an article tag), news (each item in an article tag), user comments (each comment in a separate article), and product cards (with an image, title, and price).

![Figure 19](../images/p117-02.png)
*Figure 19*

![Book image](../images/p117-04.png)

<!-- page 112 -->

**`<aside>`**: holds side content related to the main content of the page, such as links, comments, and ads (Figure 20).

![Figure 20](../images/p118-02.png)
*Figure 20*

**`<footer>`**: defines the end part of a document or section; CSS is used to set how these elements look. This part holds information such as the copyright, the names of the author and designer, contact links, the site's policies, and links to social networks. (Figure 21)

![Figure 21](../images/p118-01.png)
*Figure 21*

### Non-semantic elements

Non-semantic elements in HTML are elements used only to group and hold content; they say nothing special about their content. Two important examples are created with the `<div>` and `<span>` tags. They are used to organize the parts of a page, but because they have no particular meaning, overusing them can make the page harder for search engines and accessibility tools to understand.

- The `<div>` tag creates a block-level element, which means its content starts on a new line. It is used to build complex structures in pages and divide content into sections.

- The `<span>` tag creates an inline element whose content does not start on a new line. It is used to group and style small parts of text within a line.

- The `<div>` and `<span>` tags have no visual effect of their own; CSS is used to style them.

<!-- page 113 -->

> **Workshop**
>
> **Using semantic and non-semantic elements**
>
> Open the file `test.html` and use semantic elements as in the image below:
>
> ![Book image](../images/p119-01.png)
>
> ![Book image](../images/p119-02.png)
>
> Save the file and see the result in the browser.
>
> \* **All rights to this site belong to My Shop**
>
> ### توضیحات (Comments)
>
> Comments in HTML are a useful tool for documenting code and taking notes in it. They let the developer add explanations, notes, or extra information. The browser does not interpret comments, so users do not see them.
>
> Comments are also used for debugging code (Debugging): by temporarily disabling part of the code, you can check its effect on how the program runs.
>
> In HTML a comment is written with the `<!-- -->` marks:
>
> ```
> <!-- this is a comment -->
> <p> This is a paragraph </p>
> ```
