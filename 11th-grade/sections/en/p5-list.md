<!-- page 305 -->

> **Activity**
>
> With the help of your teacher, find the longitude and latitude values of some other cities and save them in the database.

After the cities are registered, by clicking on Citys the list of registered cities is shown (Figure 43).

![Figure 43: The list of registered cities](../images/p311-01.png)
*Figure 43: The list of registered cities*

In Figure 43, City object is used to show the title of each city. To show the titles of the cities suitably, open the file `models.py`, make changes like Figure 44 for the model City and save the file.

![Figure 44: Adding the str method to the city model](../images/p311-02.png)
*Figure 44: Adding the str method to the city model*

<!-- page 306 -->

If you refresh the admin panel, the result will be as in Figure 45.

![Figure 45: Suitable display of the titles of the cities in the admin panel](../images/p312-01.png)
*Figure 45: Suitable display of the titles of the cities in the admin panel*

> **Curiosity**
>
> In English the plural of City is Cities, but in Django's admin panel the title of the table is wrongly shown as Citys. Check how this title can be changed in Django's admin section.

## Getting to know Django's ORM tool

Now that you have added several records containing the names of some cities and their coordinates to the table of cities, you can read one of the records (for example the first record) from inside the file `views.py`, get the weather of that city and send it to the file `index.html` for display.

For this you first need to know Django's ORM tool.

To work with the database the SQL language is used; for example the SELECT statement is one of the main statements of the SQL language.

<!-- page 307 -->

With the SELECT statement you can get all the cities of the table City from the database as follows:

`SELECT id, title, lat, lon FROM weather_city` But in Django there is a useful tool named ORM that makes working with the database easier. ORM is like a translator. It receives the operations related to communicating with the database in the Python language and, behind the scenes, translates them into SQL statements.

For example the statement equivalent to the previous query in Django's ORM is as follows:

```
City.objects.all()
```

In this Python code, City is the name of the model.

Now change the code of `show_temp_view` using Django's ORM as in Figure 46.

![Figure 46: Using Django's ORM](../images/p313-01.png)
*Figure 46: Using Django's ORM*

**Explanation of the code**:

**Line 3**: the model City is imported from `models.py` in this file.

**Line 6**: using Django's ORM, the first city saved in the table of cities is stored in the variable city.

**Line 7**: the values lat and lon are taken from the city fetched from the table and stored in the variables lat and lon.

**Line 17**: the name of the city is also taken from the database and stored in the dictionary context.

Save the file and open the main page of the site. The temperature of the city of Hamedan is shown.

<!-- page 308 -->

### Showing the list of cities

So far you were able to save some cities. These cities are to be read from the database and shown inside the site as a list so that the user, by clicking on the city they like, can see the temperature of that city.

This will be done with the help of a view and a template.

In Django, a view can get information from the database and prepare the html document for showing it to the user. Look at Figure 47: the request is sent from the url to the view and the view, using the model and the template, prepares the information for display to the user.

![Figure 47: Getting information from the model by the View](../images/p314-01.png)
*Figure 47: Getting information from the model by the View*

To show the list of cities on the main page of the site you can do four steps as follows:

1. Making a function named `city_list_view` in `Views.py`

2. Making a template named `city_list.html`

3. Changing and setting the file `urls.py`

4. Putting the link "List of cities" on the main page

**First step**: create a view named `city_list_view` as in Figure 48.

![Figure 48: Adding `city_list_view`](../images/p314-02.png)
*Figure 48: Adding `city_list_view`*

<!-- page 309 -->

**Explanation of the code**:

**Line 6**: using Django's ORM a Query is run and the list of all the cities is fetched from the table City. Django's ORM has its own statements, and these statements are turned into SQL code and run by the database. Then the result of the statement is stored in a variable named cities.

**Line 8**: the dictionary context is sent for `city_list.html`; the value of this dictionary, that is cities, was given its value in line 6.

**Second step**: now create an html file named `city_list.html` inside the templates folder and enter the code of this file as in Figure 49.

![Figure 49: Adding `city_list.html`](../images/p315-01.png)
*Figure 49: Adding `city_list.html`*

**Explanation of the code**:

**Line 10**: a loop is run over cities to show the list of cities as p tags in the browser. cities was defined earlier in the file `views.py` inside a dictionary.

**Line 11**: using {{ }} you can reach the fields of each item. title is the field you defined in the model City for the title of the city.

**Line 12**: you must end the for loop with endfor; otherwise you will meet an error in the browser.

<!-- page 310 -->

**Third step**: change the file `urls.py` in the weather app as in Figure 50.

![Figure 50: Adding the city list path to `urls.py`](../images/p316-01.png)
*Figure 50: Adding the city list path to `urls.py`*

**Explanation of the code**:

**Line 6**: a new path is added to use `city_list_view`, and it means that the list of cities is shown at the address http://127.0.0.1:8000/city/list.

**Fourth step**: change the code of `show_temp.html` to add a link to the page of the list of cities, as in Figure 51.

![Figure 51: Adding a link to the list of cities](../images/p316-02.png)
*Figure 51: Adding a link to the list of cities*

<!-- page 311 -->

**Explanation of the code**:

**Line 15**: in this line the a tag is added and its href value equals the expression {% `url 'city_list'` %}.

The expression {% `url 'city_list'` %} is a Template Tag. The url tag is used and `city_list` is its argument. This line, using the name of the path `city_list`, automatically makes the address of the link to the list of cities (Figure 52).

![Figure 52: How the url tag works in Django](../images/p317-01.png)
*Figure 52: How the url tag works in Django*

Now save the file and refresh the main page of the site; you will see the added link as in Figure 53.

![Figure 53: Showing the link to the list of cities](../images/p317-02.png)
*Figure 53: Showing the link to the list of cities*

<!-- page 312 -->

Now click on the added link (the list of cities); as in Figure 54, you will see the list of cities.

![Figure 54: Showing the list of cities](../images/p318-01.png)
*Figure 54: Showing the list of cities*

### Showing the temperature of the city chosen by the user

The cities shown in the list of cities cannot be clicked; you must make changes so that the user can click on the city they want, so that the temperature of the chosen city is shown.

First open the file `city_list.html` and make the wanted changes as in Figure 55.

![Figure 55: Adding a link to each city](../images/p318-02.png)
*Figure 55: Adding a link to each city*
