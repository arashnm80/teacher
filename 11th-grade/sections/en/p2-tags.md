**Page 93**

Designing page structure with `HTML` On a website, there are numerous web pages such as the following:

![Book image](../images/p099-01.png)

Home page (`index.html`) Products page (`products.html`) Shopping cart page (`cart.html`) Login/registration page (`login.html`)

**Figure 3**

The first step in designing these pages is creating the initial structure of the pages and placing the page elements inside them. This section introduces how to insert elements into web pages.

Marking up elements in an `HTML` document: `HTML` stands for `Hypertext` `Markup` `Language`, meaning hypertext markup language. `HTML` is not a programming language; rather, it is a markup language for creating and structuring various elements on web pages. Laying out different parts of the page such as the header, menu, main content area, sidebar, and footer is done by `HTML`.

![Book image](../images/p099-02.png)

In addition, various elements such as text, image, video, audio, and so on are inserted into different parts of the page by `HTML` code.

**Figure 4**

![Book image](../images/p099-03.png)

Introducing the tag (`Tag`): A web page includes various elements such as headings, paragraphs, links, images, lists, and so on. Each of the elements on web pages is created by tags defined in the `HTML` markup language. `HTML` tags can be used in various subjects.

**Figure 5**


---

**Page 94**

The general form of a tag is as follows:

```
<TagName Attribute=""> Content </TagName>
```

Most `HTML` tags come in pairs. That is, they have an opening tag and a closing tag. The closing tag begins with a slash (/). Some tags are also self-closing or `self-closing` and do not have a closing tag.

### Example

For example the `p` tag is written as a pair and the `img` tag is self-closing:

```
<p> This is a paragraph </p>
<img src="./flower.jpg" />
```

The word `Content` refers to the content inside the `HTML` tag. The set of opening tags, closing tags, and the content between them forms a web element.

The word `Attribute` refers to a property of an element. For example the `<img>` tag has the attributes `width`, `height`, and `src` for setting the width, height, and address of the image:

```
<img src="flower.jpg" width="200px" height="150px">
```

Creating a simple web page

### Workshop

To create a web page, a standard structure must be used; otherwise various problems arise regarding display of the page by different browsers, accessibility of content for blind people, loading speed, and so on. The initial structure of a web page includes the tags (labels) in the figure opposite:

```
<DOCTYPE html!>
<html lang="fa">
```

![Book image](../images/p100-01.png)

```
<head>
<meta charset="UTF-8">
</title> عنوان صفحه <title>
</head>
<body>
</body>
</html>
```


---

**Page 95**

The `<!DOCTYPE html>` tag: At the beginning of a web page the `<!DOCTYPE

![Book image](../images/p101-01.png)

html>` tag is used. This tag announces to browsers and search engines that this document is of type `html5`.

**Figure 6**

The `<html>` tag: `<html>` is the root tag of the `HTML` document. All content of a web page is placed inside this tag. This tag has an important attribute named `lang` that specifies the language of the page for the browser, screen-reader tools, and search engines. The `<html>` tag has another attribute named `dir` that specifies the direction of content display and has two values `rtl` and `ltr` meaning right to left and left to right.

![Figure 7](../images/p101-02.png)

**Figure 7**

The `<head>` tag: This tag must be written before the `<body>` tag. In this section meta information, the page title, linking `CSS` files, and other non-display resources are placed. This information is important for the browser and search engines.

The `<title>` tag: This tag specifies the title of the page, which is displayed in the browser’s title bar and in search results.

`<meta>` tags: These tags provide information about the web page. Some of the most common meta tags are:

The `Charset` meta tag: Specifies the character encoding type of the web page for the browser. This tag tells browsers how to interpret the page’s characters so that the page content is displayed correctly.

The `viewport` meta tag: Is used to optimize the display of the web page on mobile and tablet devices:

```
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

### Try this

Research this meta tag and present the result with several images about the effect of using this tag on the layout of page elements on different devices.

![Book image](../images/p101-03.png)

The `<body>` tag: Includes the content visible to users.

All display elements such as text, images, videos, and so on are placed in this section.

**Figure 8**


---

**Page 96**

Creating a simple web page

### Workshop

`HTML` code is stored inside a text file with the `html` extension. To write this code you can use simple text editors such as `Notepad` or professional editors such as `VScode`.

Among the capabilities of the `VScode` program one can mention colored display of code, automatic code completion, the possibility of quickly running program code, and adding various extensions.

Creating an `HTML` file For the set of exercises create a folder named `Web` in the `Document` path or on one of the drives so that the `HTML` files are stored inside that folder. In the `VScode` program from the `file` menu choose the `Open` `folder` option and then select the `Web` folder so that while you work on the project the folder contents are visible and accessible on the left side of the window.

![Book image](../images/p102-01.png)

Then click the `New` `file` button, type the file name according to the image above in the text box, and press the `Enter` key so that the file is created.

Write the initial `HTML` code together with a simple text according to the image below and save it by pressing the `Ctrl+S` keys.

Displaying the web page in the browser:

First method: To see the output of the code, press the `Win+E` keys and open the `Web` folder from your desired path. Then open the `index.html` file with your preferred browser. After making any change in the `Html` file you need to refresh (`Refresh`) the page content in the browser. This can be done with the `F5` key or by clicking the button at the top of the page.

![Book image](../images/p102-02.png)

Computer accessories store


---

**Page 97**

Second method: To see the output, use the `Go` `Live` capability in the `VScode` program; in this mode, viewing the output does not require refreshing the page. To use the `Go` `Live` capability you need to install the `Live` `Server` extension in the `Vscode` program.

For this purpose click the `Extensions` button on the left side of the program window and then search for and install the `live` `server` extension.

![Book image](../images/p103-01.png)

After installing the extension, to see the program output it is enough to click the `Go` `live` button at the bottom of the window.

![Book image](../images/p103-02.png)

In this way the browser page appears as follows:

![Book image](../images/p103-03.png)

![Book image](../images/p103-04.png)

Output

After making any new change in the page code, save the file with the `Ctrl+S` keys, then go to the browser page with the `Alt+Tab` key combination. The new output appears without needing a refresh.


---
