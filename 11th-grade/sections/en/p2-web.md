<!-- page 84 -->

## Learning unit 1

## Have you ever thought about this

- What are the stages of designing a website?

- In what form is the first draft of a website presented?

- How can different elements such as text, images, video, menus, and so on be shown on a web page?

- How are links between pages created?

- How are data-entry forms designed?

- What role does CSS play in designing and styling web pages?

- How is a web page made responsive to the width of the device?

## By the end, the student is expected to

1. Create the site's home page (`index.html`) with a standard structure.

2. Use the top-level tags of the page correctly.

3. Create the page's navigation menu with the `<nav>` tag and a list element, inside the semantic `<header>` element.

4. Put the main content of the page inside the semantic `<main>` element, and be able to use the `<section>` tag to create parts of the page.

5. Use the `<div>` element to hold the content of parts of the page.

6. Use the comment tag (`<!-- -->`) to document some of the code.

## Performance standard

Be able to create a standard structure for a web page by using HTML5 tags correctly, so that the structure and content of the page can be understood by search engines and screen readers (Screen reader), and set the page language and the text direction in the browser correctly.

<!-- page 85 -->

## How the web works

The web (World Wide Web) was created in 1989 by Tim Berners-Lee at the European Organization for Nuclear Research (CERN). Its original goal was to make sharing information between researchers easier. The first website went online in 1991, and since then the web has spread quickly and become an essential part of people's daily lives.

The web works through special protocols such as HTTP and HTTPS. These protocols define how information is sent and received between browsers and servers.

When a user enters a web address in their browser, the following steps happen:

1. **Translating the domain name**: the browser connects to a DNS¹ system to turn the domain name (for example www.chap.sch.ir) into an IP address. The IP address it gets belongs to the web server² in question.

2. **ارسال درخواست (HTTP Request)**: پس از دریافت آدرس IP، مرورگر یک درخواست HTTP به وب‌سرور مقصد ارسال می‌کند که شامل اطلاعاتی درباره نوع محتوا و درخواست کاربر است.

3. **پاسخ‌دهی سرور (HTTP Response)**: سرور درخواست را پردازش می‌کند، در صورت لزوم اطلاعاتی را از پایگاه داده (Database) دریافت می‌کند و سپس محتوا را به صورت یک پاسخ HTTP به مرورگر کاربر ارسال می‌کند. این محتوا می‌تواند شامل فایل‌های HTML، CSS، JavaScript و تصاویر باشد.

4. **Showing the content**: the browser interprets the content it received and shows it to the user as a web page (Figure 1).

![Figure 1](../images/p091-01.png)
*Figure 1*

> **Footnotes**
>
> 1. DNS turns a website's domain name into a numeric IP address. To send the user's request to the destination web server, browsers need that server's IP address. Since IP addresses of websites are hard for users to remember, users work with domain names in the browser (such as `chap.sch.ir`), and the browser sends the domain to DNS to get the IP address of the destination web server.
>
> 2. A web server is a hardware system that hosts a website's documents (such as HTML files, images, videos, databases, and so on); using certain software, it keeps and manages the website's information. Web servers receive users' requests through the browser and then send the response pages back to the user's browser.
