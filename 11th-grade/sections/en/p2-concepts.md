<!-- page 86 -->

## Some key concepts of web design

The web has several key concepts that every web developer (Web developer) needs to know. They are described below:

**Web designer**: a person or team responsible for designing the visual look of the website. This profession is a combination of graphic design, user experience (UX) design and user interface (UI) design, and creating wireframes and prototypes.

**User experience (UX)**: the experience a user gets after visiting a website in accessing information, products and services.

**User interface (UI)**: the interactive elements of a page, such as buttons, forms and menus, with which users interact with the website.

**Front-end**: the part of a website that deals directly with the user. Front-end topics include the look of the web page, the user interface (UI), and the user experience (UX).

**Back-end**: the behind-the-scenes part of a website or app, which includes the main program logic, data processing, and the connection to the database; the user does not interact with it directly.

**Web developer**: a person or team that turns the initial design of a website into usable web pages using programming languages. A web developer can also play the role of the web designer. The main duties of a web developer include the following:

1. **Front-end developer**: focuses on the look of the site and the elements the user deals with directly.

2. **Back-end developer**: focuses on server-side matters such as managing the database and processing the users' data.

**Domain**: a unique name used to reach a website, such as `google.com`. Users enter a site by using the domain name. The domain name is an understandable substitute for numeric IP addresses, which makes remembering the address of a site easy for users.

**URL**: a unique address used to find and identify a particular resource (such as a web page, image, video, or file) on the internet. URL stands for Uniform Resource Locator (Figure 2).

<!-- page 87 -->

**Host**: a place for storing the documents of a website so that the site's resources can be reached over the internet. All the files of a site (including HTML files, CSS files, scripts, images and so on) must be stored on one web-server computer so that users can reach its content by entering the site's address.

![Figure 2](../images/p093-01.png)
*Figure 2*

**Localhost**: a computer system equipped with web-server software that is used for running server-side (Back-End) code and for creating and managing databases. A localhost is only useful for practising, testing and debugging the pages of a website. There are various web-server programs that can turn a home system into a web server, but the important point is that all the web servers that answer users on the internet have an internet IP; therefore home and classroom systems that have no internet IP cannot answer remote users.

> **Note**
>
> After designing and testing the site's pages on localhost, you can move your site's content to a web host or web server. Using a web server costs money, but some companies offer free hosting with limited features and resources, which is not suitable for a real project. The most suitable hosting for sites that do not need powerful hardware is shared hosting.

### Shared hosting

Hosting companies offer different plans, each (Plan) with different hardware and bandwidth. Among these plans are shared hosting, virtual servers, dedicated servers, and cloud servers. In a shared hosting plan, the host's hardware, such as disk space, bandwidth, CPU, and RAM, is divided among several websites, so the web server's full power is not spent on answering the users of one site. That is why such hosts suit small sites with limited traffic.

<!-- page 88 -->

**Responsive Design**: a method of page design that lets the page adapt automatically to the size of the screen (different devices such as mobile, tablet and desktop).

**SEO**: a set of techniques to improve a website's rank in the results of search engines. SEO includes optimising the content, the URL structure, the use of meta tags and so on.

**Accessibility**: designing a website so that it can be reached by all users (including people with physical or visual disabilities).

**Database**: many websites use databases (Database) to store and manage information. Databases can hold information about users, products, articles, and other content.

**Version control**: version control systems manage changes to code so that you can easily go back to earlier versions.

> **Curiosity**
>
> 1. Research the SSL protocol and present your findings in class.
>
> 2. Research the kinds of websites and their uses and present your findings in class.

### The site design process

Designing and building a website is a step-by-step process in which every step matters for the final success of the project. If the steps are done correctly and in the right order, the result is a useful, attractive site that can grow.

### The overall steps of site design

In short, the site design process includes these steps:

- Define the goal and the requirements

- Design the site map (site map)

- Create a wire frame (wire frame)

- Build the page structure with HTML

- Design the look of the pages with CSS

- Add user interaction with JavaScript

- Design the database (such as tables of users, products, and orders)

- Connect the pages to the database

- Add user login and sign-up

- Build the shopping cart and payment

- Test how the site works

- Fix errors and optimize

- Publish the site on a server

<!-- page 89 -->

**Define the goal and requirements**: before starting the design or writing the code of the site's pages, you must decide what the website is for and which group of users it serves. Starting the design without knowing the needs and the website's mission usually causes serious problems during the project and the need to redesign. So the first and most important step in designing any website is defining its goal and requirements.

**Setting the project goal**: in this step these questions must be answered:

- What is the purpose of the site?

- What kind of goods or services does the site offer?

- Who are the site's main users?

- What features must the site have?

> **Example**
>
> A team of web designers and developers plans to build a website for selling textbooks. Most of its users are teachers and students. The features needed are user sign-up, showing the products, a shopping cart, and online payment.

**Analyzing the requirements**: in this step the site's needs are examined from two sides:

**a) User Requirements**: these requirements include the features and facilities users need when using the site (Table 1).

*Table 1*

| Description | User need |
| --- | --- |
| The user can create an account and log in to the site. | Sign-up and login |
| Products can be searched by name or category. | Product search |
| The user can add products to the shopping cart. | Shopping cart |
| Purchases are paid through a payment gateway. | Online payment |
| The user can see their previous orders. | Viewing orders |

<!-- page 90 -->

**b) Technical Requirements**: these requirements include the markup and programming languages, the database management system, and attention to the security and extensibility of the website (Table 2).

*Table 2*

| Description | Item |
| --- | --- |
| `Python (Django)` | Programming language |
| SQLite or MySQL | Database |
| HTML, CSS, Bootstrap | Look and design |
| Encrypting users' passwords | Security |
| The ability to add new products and features in the future | Extensibility |

**Designing the site map**: after the goal and needs of the website are clear, designing the site map is essential. The site map shows the structure of the pages, the connections between them and the user's path inside the site. A correct site map gives a better understanding of the structure of the site and simplifies the process of designing and implementing it.

> **Workshop**
>
> **Steps for designing the site map**
>
> **Step 1**: look at and examine shopping sites
>
> With your teacher's guidance, examine two or three simple shopping sites.
>
> **For example**: a phone shop, a clothing shop, a digital equipment shop
>
> What to check: which pages are in the site's menu? Which pages does the home page lead the user to? How do logging in, choosing a product, and using the shopping cart work? Is the site's look simple or cluttered?
>
> **Step 2**: identify the site's main pages
>
> In this step, identify and note the pages the sites you examined have in common. Some common pages of an online shop are:
>
> - Home
>
> - Products
>
> - Product Details
>
> - Cart
>
> - Login / Register
>
> - User Profile
>
> - About / Contact

<!-- page 91 -->

> **Workshop (continued)**
>
> **Step 3**: drawing the site map (Site Map). In this step design the site map in writing or as a drawing. A simple way to draw it is to put the home page at the top of the map and the other pages as branches under the home page.
>
> ![Book image](../images/p097-01.png)
>
> The figure opposite is a written map. Besides the written form, a site map can be drawn with boxes and arrows.
>
> **Step 4**: describe the user's path
>
> In this step the user's path through the site is described. To describe the path, think about the following:
>
> Which page does the user enter the site from? How do they choose the product they want? Along which path do they reach the shopping cart?
>
> At what point do they log in to their account?
>
> The **example** below describes a user's path:
>
> The user first enters the site's home page, then goes to the products page and chooses a product. After seeing the product details, they add it to the shopping cart, and finally log in to their account to place the order.

### Designing the look of the pages

*Table 3*

**Tools for designing the look of a site (front-end)**

| Use | Language |
| --- | --- |
| The structure and elements of the page (such as text, images, tables, buttons) | HTML |
| Beautifying and controlling the look of the elements, including adjusting colours, fonts, sizes, layout and so on. | CSS |

Once the goal and requirements are clear, it is time to design **the look of the website's pages**. The more attractive and orderly a site looks, the more users it attracts. In a shopping site, a beautiful site can bring in more customers and more sales.

The HTML markup language is used to create the elements of web pages, and the CSS style language is used to style them (Table 3).

<!-- page 92 -->

**Designing a site as a team**: the site design process has many steps, each of which needs special skills. That is why sites are usually designed by a team in which each member has a clear responsibility.

**The main roles in a site design team**

1. **UX Designer**: analysing the users' needs and optimising the experience of using the site

2. **UI Designer**: designing visual elements such as colours, fonts, buttons and forms

3. **Front-End Developer**: implementing the visual and interactive part of the site

4. **Back-End Developer**: server-side programming, database management and security

5. **Content Specialist**: researching keywords and producing attractive text content

6. **SEO Specialist**: optimising the site for search engines

Depending on the size of the project, the budget, and the number of people in the design and development team, each role can be given to one or more people. In small projects one person may take on several roles. Table 4 lists the tools commonly used by each role in a site design team. These tools help improve the quality of the project and make teamwork easier.

*Table 4: Common tools in site design*

| Role | Tools |
| --- | --- |
| UX and UI designer | Photoshop, InVision, Sketch, Adobe XD, Figma |
| Front-end developer | Bootstrap, JavaScript, CSS, HTML |
| Back-end developer | <span dir="ltr">JavaScript (Node.js), (Flask, Python, Django)</span> |
| Code editor | Atom, Sublime Text, Visual Studio Code |
| Browser and developer tools | Microsoft Edge, Mozilla Firefox, Google Chrome |
| Content management and web content platforms | Grammarly, Google Docs, WordPress |
| SEO specialist | Yoast SEO, Moz, SEMrush, Google Analytics |
| Other tools the design team uses | Cyberduck, FileZilla |
| Version control | GitHub, Git |
