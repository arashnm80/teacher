**Page 305**

### Activity

With your instructor’s help, find the latitude and longitude of a few other cities and store them in the database.

After registering the cities, by clicking on `Citys`, the list of registered cities is displayed (Figure 43).

![Figure 43 list of registered cities](../images/p311-01.png)

Figure 43 list of registered cities

In Figure 43, `City` `object` has been used to display the title of each city. To display the city titles properly, open the `models.py` file and apply changes as shown in Figure 44 for the `City` model and save the file.

![Figure 44 adding the str method to the city model](../images/p311-02.png)

Figure 44 adding the `str` method to the city model


---

**Page 306**

If you `refresh` the admin panel, the result will be as in Figure 45.

![Figure 45 properly displaying city titles in the admin panel](../images/p312-01.png)

Figure 45 properly displaying city titles in the admin panel

### Try this

In English the plural of `City` is `Cities`, but in the Django admin panel the table title is incorrectly displayed as `Citys`. Investigate how you can change this title in the Django admin section.

### Getting to know Django’s ORM tool

Now that you have added a few records containing the names of a few cities and their coordinates to the cities table, from inside the `views.py` file you can read one of the records (for example the first record), obtain that city’s weather status, and send it to the `index.html` file for display.

For this you first need to get to know Django’s `ORM` tool.

To work with the database the `SQL` language is used; for example the `SELECT` command is one of the main commands of the `SQL` language.


---

**Page 307**

With the `SELECT` command as follows you can retrieve all cities of the `City` table from the database:

```
SELECT id, title, lat, lon FROM weather_city
```

But in Django there is a useful tool named `ORM` that makes working with the database easier. `ORM` is like a translator. It receives database-related operations in the Python language and behind the scenes translates them into `SQL` commands.

For example the equivalent of the previous query in Django’s `ORM` is as follows:

```
City.objects.all()
```

In this Python code, `City` is the model name.

Now change the `show_temp_view` code using Django’s `ORM` as shown in Figure 46.

![Figure 46 using Django’s ORM](../images/p313-01.png)

Figure 46 using Django’s `ORM`

### Code notes:

Line 3: the `City` model from `models.py` has been `import`ed in this file.

Line 6: using Django’s `ORM`, the first city stored in the cities table has been stored in the `city` variable.

Line 7: the `lat` and `lon` values from the city fetched from the table have been received and stored in the `lat` and `lon` variables.

Line 17: the city name has also been received from the database and stored inside the `context` dictionary.

Save the file and open the site’s home page. Hamedan’s temperature is displayed.


---

**Page 308**

Displaying the list of cities: up to here you have been able to store a few cities. The plan is to read these cities from the database and display them on the site as a list so that the user can click on their desired city and see that city’s temperature status.

This work will be done with the help of a `view` and a `template`.

In Django, a `view` can receive information from the database and prepare the `html` document for display to the user.

Look at Figure 47; the `request` is sent from the `url` to the `view` and the `view`, using the `model` and `template`, prepares the information for display to the user.

![Figure 47 the View receiving information from the model](../images/p314-01.png)

Figure 47 the `View` receiving information from the model

To display the list of cities on the site’s home page you can carry out four steps as follows:

1 Creating a function named `city_list_view` in `Views.py`

```
2 ساختن یک template با نام city_list.html
```

3 Changing and configuring the `urls.py` file

4 Placing a “list of cities” link on the home page Step one: create a `view` named `city_list_view` as shown in Figure 48.

![Figure 48 adding city_list_view](../images/p314-02.png)

```
شکل 48 افزودن city_list_view
```


---

**Page 309**

### Code notes:

Line 6: using Django’s `ORM` a `Query` has been run and the list of all cities has been fetched from the `City` table. Django’s `ORM` has its own commands and these commands are converted to `SQL` code and run by the database. Then the result of the command has been stored in a variable named `cities`.

Line 8: the `context` dictionary has been sent for `city_list.html`; the `value` of this dictionary, namely `cities`, was assigned on line 6.

Step two: now create an `html` file named `city_list.html` inside the `templates` folder; enter the code of this file as shown in Figure 49.

![Figure 49 adding city_list.html](../images/p315-01.png)

```
شکل 49 افزودن city_list.html
```

### Code notes:

Line 10: a loop has been run over `cities` to display the list of cities as `p` tags in the browser.

`cities` was previously defined in the `views.py` file inside a dictionary.

Line 11: using {{ }} you can access the fields of each `item`. `title` is the field that you defined for the city title in the `City` model.

Line 12: you must definitely end the `for` loop with `endfor`; otherwise you will face an error in the browser.


---

**Page 310**

Step three: change the `urls.py` file in the `weather` `app` as shown in Figure 50.

![Figure 50 adding the cities list path to urls.py](../images/p316-01.png)

Figure 50 adding the cities list `path` to `urls.py`

### Code notes:

Line 6: a new `path` has been added for using `city_list_view` and it means that the list of cities

```
در آدرس /listhttp://127.0.0.1:8000/city نمایش داده می‌شود.
```

Step four: change the `show_temp.html` code to add a link to the cities list page, as shown in Figure 51.

![Figure 51 adding a link to the cities list](../images/p316-02.png)

Figure 51 adding a link to the cities list


---

**Page 311**

### Code notes:

Line 15: on this line an `a` tag has been added and its `href` value equals the expression {% `'url` `'city_list` %}.

In this expression {% `'url` `'city_list` %} is a `Template` `Tag`. The `url` tag has been used and `city_list` is its argument. This line, using the path name `city_list`, automatically generates the address of the cities list link (Figure 52).

![Figure 52 how the url tag works in Django](../images/p317-01.png)

Figure 52 how the `url` tag works in Django

Now save the file and `refresh` the site’s home page; you will see the added link as in Figure 53.

![Figure 53 displaying the cities list link](../images/p317-02.png)

Figure 53 displaying the cities list link


---

**Page 312**

Now click the added link (list of cities); as in Figure 54, you will see the list of cities.

![Figure 54 displaying the list of cities](../images/p318-01.png)

Figure 54 displaying the list of cities

Displaying the temperature of the city selected by the user: the cities that are displayed in the cities list are not clickable; you need to apply changes so that the user can click on their desired city, so that the temperature of the selected city is displayed.

First open the `city_list.html` file and apply the desired changes as shown in Figure 55.

![Figure 55 adding a link to each city](../images/p318-02.png)

Figure 55 adding a link to each city


---
