<!-- page 192 -->

## Learning unit 2

## Have you ever thought about this

- Which programming language is used to react to a click, mouse movement or pressing keyboard keys?

- Which language builds simple games, image sliders and drop-down menus?

- How can an action be run by clicking a button?

- Is it possible to reach the elements of a page and change their content and properties?

- Can the content of a page be changed without reloading the page?

- How can the validity of the information entered in a form be checked before sending it?

- How are numeric calculations and the processing of the user's input strings done?

## By the end, the student is expected to

- Implement the logic the program needs by using variables, operators and control structures.

- Know how to define repeated tasks in the form of functions and use JavaScript's built-in functions to do jobs faster.

- Using DOM selectors, change the content and properties of HTML elements in response to the user's events.

- Validate the user's inputs in forms and, if there is an error, show a suitable message.

## Performance standard

Be able to add dynamic and interactive behaviours to web pages with JavaScript in an optimised and safe way, and run the final output in different browsers.

<!-- page 193 -->

## Defining JavaScript

In the second module, parts of the first page of an online shop were designed with HTML and CSS. These parts are static by nature and have no ability to interact with the user; that means they cannot give a suitable reaction (such as showing a message or changing content) to the user's inputs (such as a click or typing). In fact HTML defines the structure and content of the web page and CSS decides the display style of the page's elements. To turn the static structure and look of the page into a dynamic user experience, defining the behaviour and logic of the page is necessary. By providing the needed platform for handling events and processing data, the JavaScript programming language makes direct interaction with the user and dynamic change of the page's content possible without needing to reload. Put simply, JavaScript is responsible for responding to the user's actions and making the behaviour of the page's elements dynamic.

![Figure 1](../images/p199-01.png)
*Figure 1*

JavaScript is a client-side (Front-End) programming language, which means that no web server is needed to run its scripts and its code is run by the browser. However JavaScript can also run on the server with the help of `Node.js`. JavaScript is an interpreted language; the JavaScript interpreter is a piece of software that parses the code written in JavaScript and then reads and runs it line by line. JavaScript interpreters work as part of web browsers. As the main client-side language, JavaScript, with the ability to directly manipulate the Document Object Model (DOM), makes it possible to change the structure and content of the page's elements in response to the user's actions. By supporting object-oriented and event-driven programming patterns, this language allows developers to implement complex logic, form validation and asynchronous communication with the server. Also, the widening of the range of uses of this language through runtime environments such as `Node.js` has made it a multi-purpose tool for developing full-fledged web applications.

JavaScript can add various features to a web page, among which the following can be mentioned:

**Dynamic shopping cart**: the ability to add, remove or change the number of products in the cart without reloading the page, and automatic calculation of the total price.

**Form validation**: checking the correctness of the information entered in a sign-up or purchase form (such as the phone number, postal code and email) before final submission.

<!-- page 194 -->

**Dynamic display of products**: filtering products by category, price or brand and sorting the list of products instantly.

**Slider and image gallery**: creating automatic or manual movement of product images to show different angles of a product.

**Responsive menu**: opening and closing the mobile menu with the user's click and suitable display on different devices.

**Sending a message (Notification)**: showing success messages (such as "the product was added to the cart") or errors as a pop-up

**Date and time**: showing the Jalali date or the current time to inform the user.

**Temporary storage**: keeping the user's sign-in information or settings in the browser (cookies) for an easier shopping experience in later visits.

### Development Environment

To start programming with JavaScript, a suitable development environment is needed that makes it possible to write the code, test it and debug it. The steps of preparing the JavaScript development environment are as follows:

**Choosing and installing an editor**: to code with JavaScript, various editors such as VSCode, Sublime Text, Atom and Notepad++ can be used. These editors have features such as code colouring, code auto-completion and debugging tools, which help improve efficiency and the programming experience.

**Choosing and installing a web browser**: all today's modern browsers such as Google Chrome, Mozilla Firefox, Microsoft Edge and Safari can run JavaScript code by default. In addition, these browsers have developer tools that give the web programmer more facilities. These tools, which are activated with the F12 key, include the console, the Elements section (containing the HTML elements and the style of the elements), Sources (the project's resources) and so on (Figure 2).

![Figure 2](../images/p200-01.png)
*Figure 2*

<!-- page 195 -->

### Adding JavaScript to a web page

To put JavaScript code in a web page, the tag `<script></script>` is used. This tag can be used in the `<head>` or the `<body>` section. Where the JavaScript code is written depends on the type of the code and the special needs of the project. However it is recommended that this code be written **before** the tag `</body>` as far as possible. By doing this, the content of the page is first fully loaded and shown to the user, then the scripts run, and as a result the page's loading time becomes shorter. JavaScript code can be written in an external file with the extension js. In that case the js file must be attached to the html file. More explanation about the above methods is given in the next section.

![Figure 3](../images/p201-01.png)
*Figure 3*

### Writing JavaScript code

A JavaScript code contains a set of instructions. Each instruction defines a separate operation and is separated from the next statement by a semicolon (;). One of the simplest and most used JavaScript statements is the method `console.log()`, which is used to show the output of the code in the browser console. The correct way of using this statement is as follows:

```
console.log (رشته ثابت یا متغیر);
```

> **Note**
>
> It is recommended to use the semicolon (;) at the end of JavaScript statements to announce the end of the statement, but using it is not compulsory.

> **Workshop**
>
> **Coding with the JavaScript language**
>
> ![Book image](../images/p201-02.png)
>
> 1. To start, create a new folder titled JavaScript and create the workshop files inside it.
>
> 2. In the JavaScript folder, create a file named `workshop1.html` and write a script similar to the picture opposite inside the `<body>` section.
>
> ![Book image](../images/p201-03.png)
>
> 3. Run the file `workshop1.html` and, to see the output of the code, press the F12 key in the browser so that the Developer Tools appear. Then click the Console button to see the result of the script.

<!-- page 196 -->

> **Workshop (continued)**
>
> ![Book image](../images/p202-01.png)
>
> 4. Add a similar script to the `<head>` section and save the file. The result in the console is expected to be similar to the picture opposite:
>
> ![Book image](../images/p202-02.png)
>
> The web browser first runs the script of the `<head>` section and then the script of the `<body>` section. That is why the phrase Second Statement is shown earlier.
>
> 5. Create a file named `script.js` inside the JavaScript folder and write the following statement in it:
>
> ![Book image](../images/p202-03.png)
>
> ![Book image](../images/p202-04.png)
>
> 6. Then save the content of the file.
>
> 7. In the `<head>` section of the file `workshop1.html`, attach the file `script.js` to the web page. Put the attaching statement exactly before the tag `</head>`:
>
> ![Book image](../images/p202-05.png)
>
> 8. See the output of the code in the browser console and write the results in the blank, in the order the phrases are shown.
>
> ............................................................................................................................................
>
> 9. Move the code that attaches the JavaScript file to before `</body>` and write the result of this change in the blank.
>
> ............................................................................................................................................

<!-- page 197 -->

> **Workshop (continued)**
>
> 10. To show a phrase in the browser (not in the console section) the statement `document.Write` can be used. This statement replaces the current content of the page with the phrase inside the parentheses. Add the statement opposite to the file `workshop1.html`:
>
> ![Book image](../images/p203-01.png)
>
> ![Book image](../images/p203-02.png)
>
> Save the HTML file and show the result in the main page of the browser. The phrase Enjoy JavaScript appears in size h2 inside the browser page.
>
> If the web page has content, the statement `document.write()` makes the current content disappear and be replaced with the content inside the parentheses. Based on this, using this statement is fine for some small exercises, but it must be used with caution in a project.

> **Curiosity**
>
> Research the advantages of writing scripts in an external file and present the results in class.

**Comments**: JavaScript makes single-line and multi-line comments possible with the signs // and /\* \*/. Writing comments is necessary to clarify the purpose, function and logic of the code. Comment signs are also used to cancel the running of some code temporarily in order to debug the program.

![Figure 4](../images/p203-03.png)
*Figure 4*

**Variables**: JavaScript has two keywords, let and var, for defining variables. The keyword var is used when support for old browsers is necessary. This keyword was used to define variables until 2015. Since 2015 the keyword let was introduced to create variables.

> **Example**
>
> The following example shows how to define the variables x and y with different values:
>
> ```
> let x = 10;
> var y = 15.75;
> ```
