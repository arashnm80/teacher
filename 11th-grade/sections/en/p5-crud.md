**Page 320**

Stage three: In the `views.py` file, add the `add_city_view` function as in Figure 66.

![Figure 66 creating a view for adding a city](../images/p326-01.png)

Figure 66 creating a `view` for adding a city

### Code notes:

Line 1: The `redirect` method has been `import`ed into this file.

Line 4: The `CityForm` class from the `forms.py` file has been `import`ed into this file.

Line 33: If the user enters the form information on the “Add city” page and clicks the “Save new city” button, a `request` of type `post` is sent to `add_city_view`; in this line the type of `request` is checked with `if`.

Line 34: A form from `CityForm` is created based on the type of request the user sent and is stored in the variable `form` so that, with its help, the information the user sent through that form can be saved.

Line 35: The `is_valid` function checks the fields the user entered. In the user’s submitted `request`, the required fields must have values and the field types must also be correct.

Line 36: If the request is valid, the information will be stored in the `city` table.

Line 37: After the city information is saved successfully, the user will be taken to the city list page.

Line 39: When the user enters this page’s address in the browser, a request of type `GET` has occurred; in this case, the type of `request` is something other than `POST`, so a new form from `CityForm` is created and stored in the variable `form` so that the add-city form can be shown to the user.


---

**Page 321**

Line 41: The form that was built is placed in the `context` dictionary and on the next line is sent to `add_city.html`.

Stage four: In the `urls.py` file for the `weather` `app`, add a new `path` as in Figure 67.

![Figure 67 adding a new path for adding a city](../images/p327-01.png)

Figure 67 adding a new `path` for adding a city

### Code notes:

A new `path` for adding a city has been added.

Stage five: In the `show_temp.html` file, add a link for adding a city on line 10 as in Figure 68.

![Figure 68 creating a link to the add-city page](../images/p327-02.png)

Figure 68 creating a link to the add-city page


---

**Page 322**

Now save all the files and `refresh` the site’s home page.

With the [Log in to the site] button, `login`. The add-city link will be shown to you (Figure 69).

![Figure 69 showing the link after the user login](../images/p328-01.png)

Figure 69 showing the link after the user `login`

Click the “Add city” link, then as in Figure 70 enter the information for your chosen city and click the Save new city button. If this form is saved successfully, the user will be taken to the city list page and the added city will be appended to the end of the list.

![Figure 70 form for adding a new city](../images/p328-02.png)

Figure 70 form for adding a new city

Deleting a city with a site member user In this project you can give member users of the site the ability to delete cities; you can do this in three stages.


---

**Page 323**

Stage one: Create a new `view` named `delete_city_view` in `views.py` as in Figure 71.

![Figure 71 building a view for deleting cities](../images/p329-01.png)

Figure 71 building a `view` for deleting cities

### Code notes:

Line 49: The `delete` statement uses Django’s `ORM` and deletes the selected city from the database.

Line 50: After deleting the city, it takes the user to the city list.

Stage two: Add a new `path` for `delete_city_view` in `urls.py` as in Figure 72.

![Figure 72 adding a new path for deleting cities](../images/p329-02.png)

Figure 72 adding a new `path` for deleting cities


---

**Page 324**

Stage three: Change the `city_list.html` file as in Figure 73.

![Figure 73 adding a delete button to city_list.html](../images/p330-01.png)

Figure 73 adding a delete button to `city_list.html`

![book image](../images/p330-02.png)

### Code notes:

Line 13: This statement causes the city delete button to be shown only for a user who is `login`.

Line 14: A form with a method of type `POST` has been created. In this form’s `action`, `city_delete` is referred to, meaning the delete request will be sent to the city-delete `view`.

Line 17: The city’s id has been added as a hidden field (`hidden`). The city’s id will not be shown in the output.

Save the files and open the city list page. The output will be as in Figure 74.

Figure 74 delete button in the city list


---

**Page 325**

By clicking the delete link next to each city, the chosen city is deleted and the city list is updated.

If the user is a guest, they will not see the delete link.

### Activity

With the knowledge you gained from the previous modules, make the site’s appearance attractive with `html` and `css` and `bootstrap`.

### Optimizing and securing the project

In this stage, to optimize the project, the project’s flaws and security bugs are reviewed.

Coding bug number one:

If no city exists in the `City` table or all cities have been deleted, an error like Figure 75 will be seen on the site’s home page.

![Figure 75 error when the cities table is empty](../images/p331-01.png)

Figure 75 error when the cities table is empty


---
