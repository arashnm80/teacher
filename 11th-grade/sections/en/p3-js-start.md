# Designing Interactive Web Pages with JavaScript


---

**Page 192**

## Learning Unit 2

## Designing Interactive Web Pages with JavaScript

### Have you ever thought

What programming language handles reactions to clicks, mouse movement, or pressing keyboard keys?

What language are simple games, image sliders, and drop-down menus built with?

How can you run an action by clicking a button?

Is it possible to access page elements and change their content and properties?

Can you change a page’s content without reloading it?

How can you check the validity of information entered in a form before it is sent?

How are numerical calculations and processing of the user’s input strings done?

### By the end, the student is expected to

Implement the logic the program needs using variables, operators, and control structures.

Know how to define repeated tasks as functions and use JavaScript’s built-in functions to get work done faster.

Using `DOM` selectors, change the content and properties of `HTML` elements in response to user events.

Validate user inputs in forms and, if there is an error, display an appropriate message.

### Performance standard

Be able to use `Java` `Script` optimally and securely to add dynamic, interactive behaviors to web pages and run the final output in different browsers.


---

**Page 193**

### Defining JavaScript

In Module 2, parts of the first page of an online store were designed using `HTML` and `CSS`.

These parts are static in nature and have no ability to interact with the user; that is, they cannot provide an appropriate response (such as showing a message or changing content) to user inputs (such as a click or typing). In fact, `HTML` defines the structure and content of the web page, and `CSS` determines how the page elements are displayed.

![Book image](../images/p199-01.png)

To turn the page’s static structure and appearance into a dynamic user experience, defining the page’s behavior and logic is necessary. The JavaScript programming language, by providing what is needed to manage events and process data, makes direct interaction with the user and dynamic changes to the page content possible without reloading.

Simply put, JavaScript is responsible for responding to the user’s actions and making the behavior of page elements dynamic.

**Figure 1**

JavaScript is a client-side (`Front-End`) programming language, meaning that running its scripts does not require a web server and its code is executed by the browser. However, JavaScript can also run on the server with the help of `Node.js`. JavaScript is an interpreted language; the JavaScript interpreter is software that parses code written in JavaScript, then reads and runs it line by line. JavaScript interpreters work as part of web browsers.

As the main client-side language, JavaScript, with the ability to manipulate the Document Object Model (`DOM`) directly, makes it possible to change the structure and content of page elements in response to the user’s actions. With support for object-oriented and event-driven programming patterns, this language lets developers implement complex logic, form validation, and asynchronous communication with the server. Also, extending the language’s range of use through runtimes such as `Node.js` has turned it into a versatile tool for developing full-featured web applications.

JavaScript can add various capabilities to a web page, including the following:

Dynamic shopping cart: Adding, removing, or changing the quantity of products in the cart without reloading the page, and automatically calculating the total price.

Form validation: Checking that information entered in a registration or purchase form (such as phone number, postal code, and email) is correct before final submission.


---

**Page 194**

Dynamic product display: Filtering products by category, price, or brand and sorting the product list in real time.

Image slider and gallery: Creating automatic or manual movement of product images to show different angles of a product.

Responsive menu (`Responsive`): Opening and closing the mobile menu with a user click and displaying it appropriately on different devices.

Sending a message (`Notifciation`): Showing success messages (such as “Product added to cart”) or errors as a pop-up (`pop` `up`) Date and time: Displaying the solar (Persian) calendar date or the current time to inform the user.

Temporary storage: Keeping login information or user settings in the browser (cookies) for an easier shopping experience on later visits.

```
محیط توسعه (Development Environment)
```

To start programming with JavaScript, you need a suitable development environment that lets you write, test, and debug code. The steps for preparing a JavaScript development environment are as follows:

Choosing and installing an editor: For coding with JavaScript you can use various editors such as `VSCode`, `Sublime` `Text`, `Atom`, and `++Notepad`. These editors have features such as syntax highlighting, code completion, and debugging (`Debug`) tools that help improve efficiency and the programming experience.

Choosing and installing a web browser: All modern browsers today, such as `Google` `Chrome`, `Mozilla` `Firefox`, `Microsoft` `Edge`, and `Safari`, can run JavaScript code by default.

In addition, these browsers have developer tools (`Developer` `tools`) that give the web programmer more capabilities. These tools, which are activated with the `F12` key, include the console, the `Element` section (containing `HTML` elements and element styles), `Sources` (project resources), and more (Figure 2).

![Figure 2](../images/p200-01.png)

**Figure 2**


---

**Page 195**

Adding JavaScript to a web page To insert JavaScript code into a web page, the `<script></script>` tag is used. This tag can be used in the `<head>` or `<body>` section. Where you write the JavaScript code depends on the type of code and the specific needs of the project. However, it is recommended that, as much as possible, this code be written before the `<body/>` tag. By doing this, the page content is fully loaded and shown to the user first, and then the scripts run, so the page load time is shorter. JavaScript code can also be written in an external file with the `js` extension. In that case, the `js` file must be attached to the `html` file. More explanation of the methods above is given in the next section.

![Figure 3](../images/p201-01.png)

**Figure 3**

Writing JavaScript code A piece of JavaScript code contains a set of instructions. Each instruction defines a separate operation and is separated from the next instruction by a semicolon (;). One of the simplest and most widely used JavaScript statements is the `console.log`() method, which is used to display the code’s output in the browser console. The correct way to use this statement is as follows:

`console.log`(literal string or variable);

### Note

It is recommended that you use a semicolon (;) at the end of JavaScript statements to mark the end of the statement, but using it is not required.

Coding in the JavaScript language

### Workshop

![Book image](../images/p201-02.png)

1 To get started, create a new folder named `JavaScript` and create the workshop files inside it.

2 In the `JavaScript` folder, create a file named `workshop1.html` and write a script similar to the image on the right inside the `<body>` section.

![Book image](../images/p201-03.png)

3 Run the `workshop1.html` file and, to see the code output, press the `F12` key in the browser so the developer tools (`Developer` `Tools`) appear. Then, to see the script result, click the `Console` button.


---

**Page 196**

![Book image](../images/p202-01.png)

4 Add a similar script to the `<head>` section and save the file. The result in the console is expected to look like the image on the right:

![Book image](../images/p202-02.png)

The web browser runs the script in the `<head>` section first and then the script in the `<body>` section. That is why the phrase `Second` `Statement` appears earlier.

5 Create a file named `script.js` inside the `JavaScript` folder and write the following statement in it:

![Book image](../images/p202-03.png)

![Book image](../images/p202-04.png)

6 Then save the file contents.

```
7 در بخش <head> فایل workshop1.html،
```

Attach the `script.js` file to the web page. Place the attach statement exactly before the `<head/>` tag:

![Book image](../images/p202-05.png)

8 View the code output in the browser console and write the results in the blank in the order the phrases are displayed.

............................................................................................................................................

9 Move the statement that attaches the JavaScript file to before `<body/>` and write the result of this change in the blank.

............................................................................................................................................


---

**Page 197**

10 To display a phrase in the browser (not in the `console` section), you can use the `document.Write` statement. This statement replaces the current page content with the phrase inside the parentheses. Add the statement on the right to the file

![Book image](../images/p203-01.png)

![Book image](../images/p203-02.png)

```
workshop1.html اضافه کنید:
```

Save the `HTML` file and display the result on the browser’s main page. The phrase `Enjoy` `JavaScript` appears on the browser page at size `h2`.

If the web page already has content, the `document.write`() statement causes the current content to disappear and be replaced by the content inside the parentheses. Accordingly, using this statement for some small exercises is fine, but you should be careful when using it in a project.

### Try this

Research the advantages of writing scripts in an external file and present the results in class.

Comments (`comments`): JavaScript lets you create single-line and multi-line comments with the // and /* */ marks. Writing comments is necessary to clarify the purpose, behavior, and logic of the code. Comment marks are also used to temporarily cancel the execution of some code for debugging the program.

![Figure 4](../images/p203-03.png)

**Figure 4**

Variables (`Variables`): JavaScript has two keywords, `let` and `var`, for defining variables. The `var` keyword is used when support for older browsers is necessary. This keyword was used to define variables until 2015. From 2015, the `let` keyword was introduced for creating variables.

### Example

The following example shows how to define the variables `x` and `y` with different values:

```
;let x = 10
;var y = 15.75
```


---
