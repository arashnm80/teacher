<!-- page 93 -->

### Building the page structure with HTML

![Figure 3](../images/p099-01.png)
*Figure 3*

A website has several web pages, such as:

- The home page (`index.html`)

- The products page (`products.html`)

- The shopping cart page (`cart.html`)

- The login/sign-up page (`login.html`)

The first step in designing these pages is to create their basic structure and place the page elements in it. This part shows how to put elements into web pages.

**Marking up elements in an HTML document:** HTML stands for Hypertext Markup Language. HTML is not a programming language; it is a markup language for creating and structuring the elements of web pages. HTML places the different parts of a page, such as the header, the menu, the main content area, the sidebar, and the footer. It also puts elements such as text, images, video, and sound into the different parts of the page.

![Figure 4](../images/p099-02.png)
*Figure 4*

![Figure 5](../images/p099-03.png)
*Figure 5*

**معرفی تگ (Tag)**: یک صفحۀ وب شامل عناصر مختلفی مانند تیترها، پاراگراف‌ها، پیوندها، تصاویر، لیست و غیره است. هر یک از عناصر موجود در صفحات وب توسط تگ‌ها یا تگ‌های تعریف‌شده در زبان نشانه‌گذاری HTML ایجاد می‌شود. تگ‌های HTML در موضوعات مختلف قابل استفاده هستند.

<!-- page 94 -->

The general form of a tag is:

```
<TagName Attribute=""> Content </TagName>
```

Most HTML tags come in pairs: they have an opening tag and a closing tag. The closing tag starts with a slash (/). Some tags are self-closing (self-closing) and have no closing tag.

> **Example**
>
> For example, the p tag is written as a pair and the img tag is self-closing:
>
> ```
> <p> This is a paragraph </p>
> <img src="./flower.jpg" />
> ```

Content means the content inside the HTML tag. The opening tag, the closing tag, and the content between them together make a web element.

An Attribute is a property of an element. For example, the `<img>` tag has the attributes width, height, and src for the width, height, and address of the image:

```
<img src="flower.jpg" width="200px" height="150px">
```

> **Workshop**
>
> **Creating a simple web page**
>
> A web page must follow a standard structure; otherwise there will be problems with how different browsers show the page, with accessibility for blind people, with loading speed, and so on. The basic structure of a web page is made of the tags in the image opposite:
>
> ```
> <DOCTYPE html!>
> <html lang="fa">
> <head>
>    <meta charset="UTF-8">
>    <title> عنوان صفحه </title>
> </head>
> <body>
> ```
>
> ![Book image](../images/p100-01.png)
>
> ```
> </body>
> </html>
> ```

<!-- page 95 -->

- **The `<!Doctype html>` tag**: the `<!Doctype html>` tag is used at the very start of a web page. It tells browsers and search engines that the document is html5.

![Figure 6](../images/p101-01.png)
*Figure 6*

- **The `<html>` tag**: the root tag of an HTML document. All the content of a web page goes inside this tag. It has an important attribute named lang that tells browsers, screen readers, and search engines the language of the page. The `<html>` tag has another attribute named dir that sets the direction of the content, with two values, rtl and ltr, meaning right-to-left and left-to-right.

![Figure 7](../images/p101-02.png)
*Figure 7*

- **The `<head>` tag**: this tag must be written before the `<body>` tag. It holds meta information, the page title, links to CSS files, and other resources that are not displayed. This information matters to browsers and search engines.

- **The `<title>` tag**: sets the page title, which is shown in the browser's title bar and in search results.

- **The `<meta>` tags**: these tags give information about the web page. Some of the most common meta tags are:

**The Charset meta tag**: tells the browser the character encoding of the web page, so that the browser interprets the page's characters correctly and shows the content properly.

**The viewport meta tag**: used to optimize how the web page is shown on phones and tablets: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

> **Curiosity**
>
> Research this meta tag and show, with a few images, how using it affects the layout of page elements on different devices.

![Figure 8](../images/p101-03.png)
*Figure 8*

- **The `<body>` tag**: holds the content users can see. All visible elements, such as text, images, videos, and so on, go in this part.

<!-- page 96 -->

> **Workshop**
>
> **Creating a simple web page**
>
> HTML code is saved in a text file with the html extension. You can write it with a simple text editor such as Notepad or a professional editor such as VScode. VScode features include colored code, automatic code completion, running the code quickly, and adding all kinds of extensions.
>
> **Creating an HTML file**
>
> For your exercises, create a folder named Web in Documents or on one of the drives, and save your HTML files in it. In VScode choose Open folder from the file menu and then choose the Web folder, so that the folder's contents stay visible and available on the left of the window while you work on the project.
>
> ![Book image](../images/p102-01.png)
>
> Then click the New file button, type the file name in the text box as in the image above, and press Enter to create the file.
>
> Write the basic HTML code with some simple text, as in the image below, and save it with Ctrl+S.
>
> ### Viewing the web page in a browser
>
> - **Method 1**: to see the output of the code, press Win+E and open the Web folder where you saved it. Then open the `index.html` file with any browser. After each change to the Html file you need to refresh (Refresh) the page in the browser, with F5 or the button at the top of the window.
>
> ![Book image](../images/p102-02.png)

<!-- page 97 -->

> **Workshop (continued)**
>
> - **Method 2**: use VScode's Go Live feature, which shows the output without refreshing the page. To use Go Live, install the Live Server extension in VScode.
>
> To do this, click the Extensions button on the left of the program window, then search for the live server extension and install it.
>
> ![Book image](../images/p103-01.png)
>
> After installing the extension, just click the Go live button at the bottom of the window to see the program's output.
>
> ![Book image](../images/p103-02.png)
>
> The browser window then looks like this:
>
> ![Book image](../images/p103-03.png)
>
> After each new change to the page code, save the file with Ctrl+S, then switch to the browser with Alt+Tab. The new output appears without refreshing.
