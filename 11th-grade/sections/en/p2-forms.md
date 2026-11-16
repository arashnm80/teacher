<!-- page 106 -->

> **Workshop**
>
> **Using the table tag**
>
> Following the image, write the tags needed to create the table and see the result in the browser.
>
> ![Book image](../images/p112-01.png)

## Designing forms

### Data-entry forms

![Figure 16](../images/p112-02.png)
*Figure 16*

Forms are powerful tools for collecting information from users. A data-entry form takes users' information and sends it to a web server to be processed and stored. Processing and storage happen on the server side. A form contains different tags for getting users' data. These tags are:

**`<form>`**: defines a form.

The general form of this tag is:

```
<form action="URL" method="http_method" enctype="encoding_type">
```

The attributes of the form element are:

**action**: sets the address (URL) on the server to which the form's data is sent for processing.

**method**: specifies the way the form data is sent to the server. This attribute has two values, get and post. In the get method the form data is sent to the server as URL parameters. This method is not suitable for sending sensitive user data. In the post method the form information is sent to the server in a hidden way; this method is suitable for sending sensitive data. In the table on the next page, see a comparison of the two ways of sending information in forms (Table 5).

<!-- page 107 -->

*Table 5: Comparing the two ways of sending form data*

| Aspect | The GET method | The POST method |
| --- | --- | --- |
| How the data is sent | The data is sent through the browser's address bar, so the user can see it. | The data is sent in the body of the HTTP request and cannot be seen in the URL. |
| Limit on data size | Browsers have limits when sending a request with GET. Depending on the browser and the server settings, the string sent through the address bar can be 2000 to 8000 characters long. | Has few limits and can be used to send files and long texts. |
| Security | Low security: besides showing users' data in the address bar, the address may be stored (cached) in the browser's memory. | Safer than GET, but not fully secure unless the HTTPS protocol is used. |
| Uses | Getting information from the server (such as searching and filtering), when the user does not intend to change data on the server. | Sending information to the server to be processed or stored (such as signing up, logging in, uploading a file) |

> **Example**
>
> An example of using the GET method
>
> ![Book image](../images/p113-02.png)
>
> ![Book image](../images/p113-03.png)
>
> ![Book image](../images/p113-04.png)
>
> Output

> **Example**
>
> An example of using the POST method
>
> ![Book image](../images/p113-01.png)

<!-- page 108 -->

A form holds a set of elements for getting different information from users, shown in Table 6:

*Table 6: Form elements (the tags used in the form element) and their uses*

| Form element | Use and general form of the element |
| --- | --- |
| `<label>` | Sets the label of form elements. |
|  | `<label for=" ">  </label>` |
| `<input>` | Gets different kinds of information from the user. The kind of input is set by the type attribute. |
|  | `<input type="" name="" id="" value="" placeholder="" required >` |
| `<fieldset>` | Groups form elements; this tag draws a box around a group of fields. |
| `<legend>` | `<fieldset> <legend> </legend> </fieldset>`<br>The legend tag sets the title of the group. |
| `<textarea>` | Gets long text from users; the size of the text box is set with the rows and cols attributes. |
|  | `<textarea id="" name=" " rows="" cols="" required> </textarea>` |
|  | Creates a drop-down list. The options of the list are set with the `<option>` tag. |
| `<select>` | `<select id="" name="" required>`<br>`<option value=""> </option>`<br>`</select>` |

The type attribute of the `<input>` element sets the kind of data the user enters. Its values are described in Table 7:

*Table 7: The values of the type attribute of the &lt;input&gt; element*

| Value of type | Use |
| --- | --- |
| text, password, email | Gets short text values such as a username, password, and email. |
| tel, number | Gets phone numbers and numeric values. |
| radio | Creates a list of options from which the user may choose only one. |
| checkbox | Creates a list of options from which the user can choose zero, one, or several. |
| file | Gets a file from the user (upload). |
| submit | Creates a button that sends the information |
| reset | Clears the content of the form. |

<!-- page 109 -->

To create a group of radio buttons, the name attribute must be the same for all the radio buttons in the group; otherwise several of them could be selected. Radio buttons are usually used when one option must be chosen from several.

> **Example**
>
> Example:
>
> ![Book image](../images/p115-01.png)

> **Workshop**
>
> **Creating an order form**: create a new page named `order_form.html` and write the order form in it as in the figure below. Then check the result in the browser.
>
> ![Book image](../images/p115-02.png)
>
> Output

<!-- page 110 -->

**name**: sets the name of the element, which is used in server-side code.

**id**: sets the identifier of the form element, which must be unique.

**value**: sets the default value of the form element.

**required**: using this attribute in form elements shows an error message if a field is left empty.

> **Activity**
>
> Create a product-return form with first and last name, order number, product name, reason for return, and a picture of the product.

## Structuring the page with semantic elements (Semantic Elements)

Semantic elements in HTML are elements that clearly describe the content inside them. Using them helps screen readers and search engines understand the structure and content of the page better. Semantic elements not only improve the page's SEO but also make the code easier to organize and maintain. They are:

**`<main>`**: holds the main content of the page. Each page must have only one `<main>` element.

**`<header>`**: defines the header of a document. Inside this tag you can use tags such as `<h1>`, `<p>`, `<nav>`, `<ul>`, `<img>`, and `<form>`.

**`<nav>`**: used when creating navigation menus¹ (Figure 17).

![Figure 17](../images/p116-01.png)
*Figure 17*

> **Footnotes**
>
> 1. A navigation menu (Navigation Menu) is a set of links that lets users move between the pages or sections of a website. A site's navigation menu is usually at the top or the side of a web page.
