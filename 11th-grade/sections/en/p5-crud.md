<!-- page 320 -->

**Third step**: in the file `views.py` add the function `add_city_view` as in Figure 66.

![Figure 66: Creating a view to add a city](../images/p326-01.png)
*Figure 66: Creating a view to add a city*

**Explanation of the code**:

**Line 1**: the method redirect is imported in this file.

**Line 4**: the class CityForm is imported from the file `forms.py` in this file.

**Line 33**: if the user, on the "Add city" page, enters the form's information and clicks the "Save new city" button, a request of the post type is sent to `add_city_view`; in this line the type of the request is checked with if.

**Line 34**: a form is created from CityForm based on the type of the user's sent request and stored in the variable form so that, with its help, the information the user has sent with that form is saved.

**Line 35**: the function `is_valid` checks the fields entered by the user. In the user's sent request, the compulsory fields must have received values and the types of the fields must be correct.

**Line 36**: if the request is valid, the information will be saved in the table city.

**Line 37**: after the city's information is saved successfully, the user will be taken to the page of the list of cities.

**Line 39**: when the user enters the address of this page in the browser, a request of the GET type has happened; in this case the type of the request is something other than POST, so a new form is created from CityForm and stored in the variable form so that the form for adding a city is shown to the user.

<!-- page 321 -->

**Line 41**: the form that was made is put in the dictionary context and in the next line is sent to `add_city.html`.

**Fourth step**: in the file `urls.py` of the weather app add a new path as in Figure 67.

![Figure 67: Adding a new path for adding a city](../images/p327-01.png)
*Figure 67: Adding a new path for adding a city*

**Explanation of the code**:

A new path for adding a city is added.

**Fifth step**: in the file `show_temp.html` add a link for adding a city, in line 10 as in Figure 68.

![Figure 68: Creating a link to the add city page](../images/p327-02.png)
*Figure 68: Creating a link to the add city page*

<!-- page 322 -->

Now save all the files and refresh the main page of the site.

Log in with the \[Sign in\] button. The link for adding a city will be shown to you (Figure 69).

![Figure 69: Showing the link after the user's login](../images/p328-01.png)
*Figure 69: Showing the link after the user's login*

Click on the link "Add city", then, as in Figure 70, enter the information of the city you want and click the button Save new city. If this form is saved successfully, the user is taken to the page of the list of cities and the added city is added to the end of the list.

![Figure 70: The form for adding a new city](../images/p328-02.png)
*Figure 70: The form for adding a new city*

### Deleting a city with a member user of the site

In this project you can give the member user of the site the ability to delete cities; you can do this in three steps.

<!-- page 323 -->

**First step**: create a new view named `delete_city_view` in `views.py` as in Figure 71.

![Figure 71: Making a view to delete cities](../images/p329-01.png)
*Figure 71: Making a view to delete cities*

**Explanation of the code**:

**Line 49**: the statement delete uses Django's ORM and deletes the chosen city from the database.

**Line 50**: after deleting the city, it takes the user to the list of cities.

**Second step**: add a new path for `delete_city_view` in `urls.py` as in Figure 72.

![Figure 72: Adding a new path to delete cities](../images/p329-02.png)
*Figure 72: Adding a new path to delete cities*

<!-- page 324 -->

**Third step**: change the file `city_list.html` as in Figure 73.

![Figure 73: Adding a delete button to `city_list.html`](../images/p330-01.png)
*Figure 73: Adding a delete button to `city_list.html`*

![Figure 74: The delete button in the list of cities](../images/p330-02.png)
*Figure 74: The delete button in the list of cities*

**Explanation of the code**:

**Line 13**: this statement makes the delete-city button shown only to a logged-in user.

**Line 14**: a form with a POST-type method is created. In the action of this form, `delete_city` is pointed to, that is, the delete request will be sent to the delete-city view.

**Line 17**: the id of the city is added as a hidden field. The id of the city will not be shown in the output. Save the files and open the page of the list of cities. The output will be as in Figure 74.

<!-- page 325 -->

By clicking the delete link opposite each city, the wanted city is deleted and the list of cities is updated. If the user is a guest, they will not see the delete link.

> **Activity**
>
> With the knowledge you have gained from the earlier modules, make the look of the site beautiful with html, css and bootstrap.

## Optimising and securing the project

At this step, to optimise the project, the flaws and security bugs of the project are checked.

**Coding bug number one**:

If there is no city in the table City or all the cities have been deleted, an error as in Figure 75 will be seen on the main page of the site.

![Figure 75: The error when the table of cities is empty](../images/p331-01.png)
*Figure 75: The error when the table of cities is empty*
