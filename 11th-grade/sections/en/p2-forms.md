**Page 106**

Using the table tag

### Workshop

As in the image, write the tags needed to create the table and observe the result in the browser.

![Book image](../images/p112-01.png)

### Form design

Data entry forms Forms are powerful tools for collecting information from users. A data entry form receives user information and then sends it to a web server for processing and storage. Processing and storage are

![Figure 16](../images/p112-02.png)

**Figure 16**

done on the server side. An information form includes various tags for receiving user data.

These tags are as follows:

`<form>:` Used to define a form.

The general form of this tag is as follows:

```
<form action="URL" method="http_method" enctype="encoding_type">
```

The attributes of the form element are as follows:

`action:` This attribute specifies to which address (`URL`) on the server side the form data should be sent for processing.

`method:` Specifies the method of sending the form data to the server. This attribute has two values, `get` and `post`. In the `get` method, the form data are sent to the server as `URL` parameters. This method is not suitable for sending sensitive user data. In the `post` method, the form information is sent to the server in a hidden way; this method is suitable for sending sensitive data. In the table on the next page, see the comparison of the two methods of sending information in forms (Table 5).


---

**Page 107**

Table 5 Comparison of the two methods of sending information in forms

Operation `GET` method `POST` method

How data are sent

Data are sent through the browser address bar and

Data are sent in the body of the `HTTP` request and

are visible to the user as a result.

are not visible in the `URL`.

Data volume limit

Browsers have a limit when sending a request with the `GET`

method. Depending on the browser type and server

settings, the length of the string that can be sent through the address bar is between

2000 and 8000 characters.

Has little limit and can be used for sending files and

long texts.

Security

Has low security; in addition to displaying user data

in the address bar, it is possible for the address content to be stored (cached)

in the browser memory.

Is more secure than the `GET` method but does not have complete security,

unless the `HTTPS` protocol is used.

Uses

For receiving information from the server (such as search and filtering).

In this case the user does not intend to change the server data.

For sending information to the server for processing or

storage (such as registration, login, file upload)


### Example

An example of using the `GET` method

![Book image](../images/p113-03.png)

![Book image](../images/p113-04.png)

![Book image](../images/p113-05.png)

Output

### Example

An example of using the `POST` method

![Book image](../images/p113-01.png)

![Book image](../images/p113-02.png)


---

**Page 108**

A form contains a set of elements for receiving various information from users, which is shown in Table 6:

Table 6 Form elements (tags used inside the form element) and their uses Form element

Use and general form of the element

Setting labels for form elements.

```
<label>
<label for=" "> </label>
```

Receiving various information from the user. The input type is specified by the `type` attribute.

```
<input>
<input type="" name="" id="" value="" placeholder="" required >
<feildset>
```

Grouping form elements; this tag causes a box to be displayed around the group of fields.

```
<fieldset> <legend> </legend> </fieldset>
<legend>
```

The `legend` label specifies the group title.

Receiving long phrases from users; the size of the text box is specified with the `rows` and `cols` attributes.

```
<textarea>
<textarea id="" name=" " rows="" cols="" required> </textarea>
```

Creating a list or drop-down list. The list options are specified with the `<option>` tag.

```
<select id="" name="" required>
<select>
<option value=""> </option>
</select>
```

The `type` attribute on the `<input>` element determines the type of user input data. The value of this attribute is described in Table 7:

Table 7 Values of the `type` attribute on the `<input>` element

Value of the `type` attribute

### Use

```
text, password, email
```

Receiving short text values such as username, password, and email.

```
tel, number
```

Receiving a phone number and numeric values.

`radio`

Creating a list of options where the user is allowed to select only one option.

Used to create a list of options where the user can select zero, one, or more options

```
checkbox
```

.

`file`

Receiving a file from users (upload).

`submit` Creating a button to send information

`reset`

Clears the form content.


---

**Page 109**

To create a group of radio buttons, the `name` attribute must be the same for all radio buttons in the group; otherwise it is possible to select more than one element. Radio buttons are usually used when choosing one option from among several options is involved.

### Example

### Example:

![Book image](../images/p115-01.png)

```
مرد<input type="radio" name="gender" value="male">
زن<input type="radio" name="gender" value="female">
```

Creating an order form

### Workshop

Create a new page named `order_form.html` and write the order form inside it as in the figure below. Then check the result in the browser.

![Book image](../images/p115-02.png)

![Book image](../images/p115-03.png)

Output


---

**Page 110**

`name:` Sets the name of the element, which is used in server-side coding.

`id:` Sets the identifier of the form element, which must be a unique value.

`value:` Sets the default value of the form element.

`required:` Using this attribute on form elements causes an error message to appear if a field is left empty.

### Activity

Create a product return form containing first and last name, order number, product name, reason for return, and product image.

### Structuring the page with semantic elements (Semantic Elements)

Semantic elements in `HTML` are elements that clearly describe the content inside them.

Using these elements helps screen readers and search engines better understand the structure and content of the page. Semantic elements not only improve the page’s SEO, but also make organizing and maintaining the code easier. These elements are as follows:

`<main>:` Used to display the main content of the page. Each page should have only one `<main>` element.

`<header>:` Used to define the header of a document. Inside this tag it is possible to use various tags such as `<h1>`, `<p>`, `<nav>`, `<ul>`, `<img>`, and `<form>`.

`<nav>:` Used when creating navigation menus1 (Figure 17).

![Figure 17](../images/p116-01.png)

**Figure 17**

1 A navigation menu (`Navigation` `Menu`) includes a set of links that allow users to move through different pages or sections inside a website. The site navigation menu is usually placed at the top or side of a web page.


---
