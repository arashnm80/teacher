**Page 86**

### Some main concepts of web design

The web has various key concepts that awareness of them is essential for every web developer (`Web` `developer`). In the following, these concepts are explained:

Web designer (`Web` `designer`): The person or team responsible for designing the visual appearance of the website. This profession is a combination of graphic design, user experience (`UX`) design and user interface (`UI`) design, creating a `wire` `frame` and a prototype.

User experience (`UX`): The experience the user gains after visiting the website to access information, products, and services.

User interface (`UI`): Interactive elements of the page such as buttons, forms, and menus that users interact with the website by means of.

`Front-end:` The part of the website that has a direct connection with the user. Topics in the front-end section include the appearance of the web page, the user interface (`UI`), and the user experience (`UX`).

`Back-end:` The behind-the-scenes part of the website or application that includes the main program logic, data processing, and connection to the database, and with which the user has no direct interaction.

Web developer (`Web` `developer`): The person or team that turns the initial design of the website into usable web pages using programming languages. The web developer can also have the role of web designer. The main duties of a web developer include the following:

1 Client-side developer (`Front-end-developer`): Focuses on the appearance of the site and the elements that the user deals with directly.

2 Server-side developer (`Back-end-developer`): Focuses on server-side topics such as database management and processing users’ data.

Domain (`Domain`): A unique name used to access a website, such as `.google.com` Users enter a site using the domain name. The domain name is an understandable substitute for numeric `IP` addresses that makes remembering the site address easier for users.

`URL:` A unique address used to find and identify a particular resource (such as a web page, photo, video, or file) on the Internet. `URL` stands for `Uniform` `Resource` `Locator` (Figure 2).


---

**Page 87**

`Host:` Space for storing the documents of a website so that access to the site’s resources through the Internet is provided. All files of a site (including `HTML`, `CSS` files, scripts, images, and so on) must be stored on a web-server computer so that users can access its content by entering the site address.

![Figure 2](../images/p093-01.png)

**Figure 2**

`Localhost` (local host): A computer system equipped with web-server software that is used to run server-side (`Back-End`) code and to create and manage databases. A local host is used only for practice, testing, and debugging website pages. There are various web-server software programs that can turn a home system into a web server, but the important point is that all web servers that respond to users across the Internet have an Internet `IP`; therefore home systems and classroom systems that lack an Internet `IP` cannot respond to remote users.

### Note

After designing and testing the site pages on localhost, you can transfer your site’s content to a web host or web server. Access to a web server requires payment, but some companies provide the possibility of using free hosts with limited features and resources that are not suitable for a real project. The most suitable hosts for sites that do not need powerful hardware resources are shared hosts.

Shared host:

Hosting companies have various plans for offering their services, and each plan (`Plan`) has different hardware features and bandwidth. Among these plans one can mention shared host, virtual server, dedicated server, and cloud server. In a shared-host plan, the host’s hardware features such as disk space, bandwidth, `CPU`, and `RAM` memory are divided among several websites. In this way, the entire hardware power of the web server is not spent responding to the requests of the users of one site. For this reason such hosts are suitable for small sites with limited traffic.


---

**Page 88**

Responsive design (`Responsive` `Design`): A method of page design that provides automatic adaptability of the page based on the size of the display (different devices such as mobile, tablet, and desktop).

SEO (`SEO`): A set of techniques for improving a website’s ranking in search engine results. SEO includes optimizing content, `URL` structure, and the use of meta tags, and so on.

Accessibility (`Accessibility`): Designing a website so that it is accessible for all users (including people with physical or visual disabilities).

Database: Many websites use databases (`Database`) to store and manage information. Databases can include information about users, products, articles, and other content.

Version control: Version-control systems make it possible to manage code changes so that returning to previous versions is easily possible.

### Try this

1 Research the `SSL` protocol and present the result in class.

2 Research types of websites and their uses and present the result in class.

The process of site design Designing and implementing a website is a step-by-step process in which each stage plays an important role in the final success of the project. If these stages are done correctly and in the proper order, the result of the work will be a practical, beautiful, and extensible site.

Overall stages of site design The process of site design, in summary, includes the following stages:

Defining the goal and requirements Designing the site map (`site` `map`) Creating a wireframe (`wire` `frame`) Creating the structure of pages with `HTML` Designing the appearance of pages with `CSS` Adding user interactions with `JavaScript` Designing the database (such as tables for users, products, and orders) Creating a connection between the pages and the database Adding user login and registration Implementing a shopping cart and payment Testing the site’s performance Fixing errors and optimizing Publishing the site on the server


---

**Page 89**

Defining the goal and requirements: Before starting to design or write the code of the site pages, it must be clear for what purpose and for what group of users the website is being designed. Starting design without recognizing the needs and determining the mission of the website usually causes fundamental problems during project implementation and the need to redesign. For this reason, the first and most important step in designing any website is defining its goal and requirements.

Determining the project goal: In this stage the following questions must be answered:

What is the goal of creating the site?

What kind of goods or services are offered on the site?

Who are the main users of the site?

What features must exist on the site?

### Example

A team of web designers and developers intends to create a website for selling textbooks.

Most users of this site are instructors and students. Required features include user registration, displaying goods, a shopping cart, and online payment.

Analyzing requirements: In this stage, the site’s needs are examined from two aspects:

a) User requirements (`User` `Requirements`): These requirements include the features and capabilities that users need when using the site (Table 1).

**Table 1**

Explanation

User need

The user should be able to create a user account and log in to the site.

Registration and login Search

The ability to search based on the name or category of goods should exist.

Product

The user should be able to add products to the shopping cart.

Shopping cart

The purchase process should be carried out through a payment gateway.

Internet payment

The user should be able to view their previous orders.

Viewing orders


---

**Page 90**

b) Technical requirements (`Technical` `Requirements`): These requirements include markup and programming languages, the database management system, and attention to the security and extensibility of the website (Table 2).

**Table 2**

Explanation

Item `Python` (`Django`) programming language `SQLite` or `MySQL` database `HTML`, `CSS`, `Bootstrap` appearance design Encrypting users’ passwords security

The possibility of adding new products and features in the future

Extensibility

Designing the site map (`Site` `Map`): After the goal and needs of the website have been specified, designing the site map is essential. The site map specifies the structure of the pages, the connections among them, and the path of the user’s movement within the site. Correct design of the site map leads to a better understanding of the site’s structure and simplifies the process of designing and implementing it.

Stages of designing the site map

### Workshop

Stage 1: Observing and examining store sites With guidance from your instructor, examine two or three simple store sites.

For example: a mobile store, a clothing store, a digital accessories store Items that should be examined: What pages exist in the site menu? Which pages is the user directed to from the home page? How are the process of user login, selecting goods, and using the shopping cart done?

Is the appearance of the site simple or busy?

Stage 2: Identifying the main pages of the site In this stage, you need to identify and note the pages common among the sites you examined.

Examples of common pages in an online store are:

`Home`

```
Products
Product Details
```

`Cart`

```
Login / Register
User Profile
About / Contact
```


---

**Page 91**

Stage 3: Drawing the site map (`Site` `Map`) In this stage design the site map in written or graphic form

`Home`

. A simple method for drawing the map is that the home page is at the top of the map and the other pages

```
Products details
Products
```

are placed as sub-branches under the home page.

`Cart`

```
User proflie
Login/Register
```

The figure opposite is considered a written map:

In addition to the written method, the site map can be

```
Contact us
```

displayed graphically using boxes and arrows.

Stage 4: Stating the path of the user’s movement In this stage, the path of the user’s movement on the site is explained. To describe the path, pay attention to the following:

From which page does the user enter the site? How does the user select the desired product? By what path does the user reach the shopping cart?

At what stage does the user enter their user account?

The following example is a sample description of the path of the user’s movement:

The user first enters the site’s home page, then goes to the products page and selects a product. After viewing the product details, the user adds it to the shopping cart and finally logs in to their user account to place the order.

Designing the appearance of pages

**Table 3**

After the goal and requirements have been specified, it is time

Tools for designing the appearance of the site (front-end)

to design the appearance of the website pages.

The more beautiful and orderly the appearance of the site is, the more users

### In practice

Language

will be attracted to the site. On a store

Structure and elements of the page (such as text,

site, the beauty of the site can lead to attracting

`HTML`

image, table, button)

customers and more sales.

Beautifying and controlling the appearance of elements including

To create elements inside web pages the markup language

`CSS`

setting colors, fonts, sizes,

`HTML` is used, and to style the page elements the

layout, and so on

descriptive language `CSS` is used (Table 3).


---

**Page 92**

Designing a site as a team: The process of site design includes numerous stages, each of which requires specialized skills. For this reason, site design is usually done as a team and each member has a specific responsibility.

Main roles in the site design team

1 User experience designer (`UX` `Designer`): Analyzing users’ needs and optimizing the experience of using the site

2 User interface designer (`UI` `Designer`): Designing visual elements such as colors, fonts, buttons, and forms

3 Front-end developer (`Front-End` `Developer`): Implementing the visual and interactive part of the site

4 Back-end developer (`Back-End` `Developer`): Server-side programming, database management, and security

5 Content specialist (`Content` `Specialist`): Researching keywords and producing attractive text content

6 SEO specialist (`SEO` `Specialist`): Optimizing the site for search engines

Depending on the volume of project work, the budget, and the number of people on the website design and development team, each role can be assigned to one or more people. In small projects one person may take on several roles. In Table 4 the common tools used by each of the roles on the site design team are introduced. These tools help improve the quality of the project and facilitate collaboration among team members.

Table 4 Common tools in site design

Role

Tools

```
Photoshop ،InVision ،Sketch ،Adobe XD ،Figma
```

`UX` and `UI` designer Front-end developer `Bootstrap` ،`JavaScript` ،`CSS` ،`HTML`

```
توسعه‌دهندۀ بک‌اندDjango) ،Python ،Flask( ،JavaScript (Node.js)
ویرایشگر کدAtom ،Sublime Text ،Visual Studio Code
مرورگر و ابزار توسعهMicrosoft Edge ،Mozilla Firefox ،Google Chrome
```

Content management platforms and producing

```
Grammarly ،Google Docs ،WordPress
```

web-based content

```
Yoast SEO ،Moz ،SEMrush ،Google Analytics
```

SEO specialist

Other tools used by the design team `Cyberduck` ،`FileZilla`

```
GitHub ،Git
```

Version control


---
