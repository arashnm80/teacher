# Designing the structure of web pages with HTML


---

**Page 84**

## Learning unit 1

## Designing the structure of web pages with HTML

### Have you ever thought

What stages does the process of designing a website have?

In what form is the initial design of a website presented?

How can different elements such as text, image, video, menu, and so on be displayed on a web page?

How is a link between pages created?

How are data-entry forms designed?

What role does `CSS` play in designing and beautifying web pages?

How is responsive design of a web page relative to the width of the device done?

### By the end, the student is expected to

1 Create the site’s home page (`index.html`) with a standard structure.

2 Use the page’s top-level tags correctly.

3 Create the page’s navigation menu using the `<nav>` tag and a list element, inside the semantic `<header>` element.

4 Create the main content of the page inside the semantic `<main>` element and be able to use the `<section>` tag to create sections of the page.

5 Use the `<div>` element to hold the content of sections of the page.

6 Use the comment tag (`<!-- -->`) to document some of the code.

### Performance standard

The ability to create a standard structure for a web page by correctly using `HTML5` tags, so that the structure and content of the page are understandable for search engines and screen reader (`Screen` `reader`) tools, and also so that the page language settings and the direction of content display in the browser are done correctly.


---

**Page 85**

### How the web works

The web (`World` `Wide` `Web`) was created in 1989 by Tim Berners-Lee at the European Organization for Nuclear Research (`CERN`). Its initial goal was to make sharing information among researchers easier. The first website was launched in 1991 and from then on expanded rapidly and became an essential part of people’s daily lives.

The web works by means of specific protocols such as `HTTP` and `HTTPS`. These protocols define methods for sending and receiving information between browsers and servers.

When a user enters a web address in their browser, the following steps occur:

1 Translating the domain name: The browser connects to a 1 `DNS` system to convert the domain name (for example `www.chap.sch.ir`) into an `IP` address. The `IP` address received will belong to the intended web server2.

2 Sending a request (`HTTP` `Request`): After receiving the `IP` address, the browser sends an `HTTP` request to the destination web server that includes information about the type of content and the user’s request.

3 Server response (`HTTP` `Response`): The server processes the request, if necessary obtains information from a database (`Database`), and then sends the content as an `HTTP` response to the user’s browser. This content can include `HTML`, `CSS`, `JavaScript` files and images.

4 Displaying the content: The browser interprets the received content and displays it as a web page for the user (Figure 1).

![Book image](../images/p091-01.png)

```
(www.chap.sch.ir)
```

37.228.138.195

**Figure 1**

1 `DNS` is responsible for converting a website’s domain name into a numeric `IP` address. Browsers need the destination web server’s `IP` address in order to send the user’s request to that server. Because remembering the `IP` addresses of websites is difficult for users, users use a domain name when communicating with the browser (such as `chap.sch.ir`), but the browser sends the domain address to `DNS` to obtain the `IP` address related to the destination web server.

2 A web server is a hardware system that hosts the documents of a website (such as `HTML` files, images, videos, databases, and so on). This hardware, using specific software, is responsible for storing and managing the website’s information. Web servers receive users’ requests indirectly through the browser and then send response pages to the user’s browser.


---
