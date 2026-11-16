<!-- page 295 -->

## Learning unit 2

## Have you ever thought about this

- How does a site communicate with the database?

- How does a web application recognise a guest user?

- How is the information that users enter in forms stored in the database?

- How can a programmer prevent errors from happening in a site?

## By the end, the student is expected to

1. Be able to make changes in the database using Django.

2. Understand and reason about the concepts of field and table in Django.

3. Be able to save the information of forms in the database using Django.

4. Get to know the concept of ORM in Django and be able to write simple queries.

5. Know the common problems and bugs in web applications and be able to fix the problems practically.

## Performance standard

The student can, by making a Model in Django and using HTML forms, implement the connection with the database and store and retrieve the information users enter in tables.

<!-- page 296 -->

## Making the city table in the database

Up to this step your site shows only the temperature of the cities you specified in the view; that is, in `show_temp_view` the city name is fixed and the temperature of one city is always shown. A better way is for the guest user to be able to choose the city they want.

To implement this feature, you need to store the information of the cities, together with the latitude and longitude of each city, in the database; then when the user enters the site, they see a list of cities and, by clicking on the name of a city, see the temperature of the city they want.

To implement this feature you must create a table in the database.

Each app has a file named `models.py`. Django uses models to make tables. Each model in Django is equal to a table, with the same name, in the database. In the first step, the class needed to define the table and the columns of the table must be created inside the file `models.py`.

Open the file `models.py` in the weather app. Then change the content of this file as in Figure 27.

![Figure 27: Making the City model](../images/p302-01.png)
*Figure 27: Making the City model*

**Explanation of the code**:

**Line 1**: the module models is imported from the module `django.db`. In fact with this line the tools and classes needed to define database models are imported.

**Line 3**: the class City is created, inheriting from Model, to make the table of cities. Model is Django's base class for making models (database tables) and provides the facilities needed to communicate with the database.

**Line 4**: this statement makes a field in the table to hold the city name as text, with a maximum length of 50 characters. For CharField, setting `max_length` is compulsory.

**Line 5**: FloatField is used to hold decimal numbers. The latitude and the longitude are both decimal numbers.

<!-- page 297 -->

To use the model City, the matching table must be made in the database.

In the terminal run the command makemigrations as in Figure 28.

![Figure 28: Running the command makemigrations](../images/p303-01.png)
*Figure 28: Running the command makemigrations*

When you run makemigrations, a file named `0001_initial.py` is created inside the weather app in the migrations folder. This file prepares the code needed to turn the model into a real table. In the next step run the command migrate in the terminal as in Figure 29.

![Figure 29: Running the command migrate](../images/p303-02.png)
*Figure 29: Running the command migrate*

<!-- page 298 -->

After running migrate, Django's default tables and the table city are made in the database `db.sqlite3`.

### Viewing the database tables

To see the structure and content of the tables inside the database, you can install the SQLite Viewer extension as a helper tool. To install this extension make sure the internet is connected (Figure 30).

![Figure 30: Searching for the SQLite Viewer extension](../images/p304-01.png)
*Figure 30: Searching for the SQLite Viewer extension*

After installing the mentioned extension, by clicking on the file `db.sqlite3` you will see Django's default tables and the table city (Figure 31).

![Figure 31: The database tables](../images/p304-02.png)
*Figure 31: The database tables*

<!-- page 299 -->

As is shown in Figure 31, the table city was made with the prefix weather. By clicking on the table `weather_city`, the list of fields is shown on the right. At the moment there is no record in the table city.

With the SQLite Viewer extension you can only see the content and structure of the tables and there is no ability to save information.

To change the content of the table city or to add the names of new cities to the table, you need to enter Django's admin panel. Of course, you still cannot enter the data of the cities into the database through the admin panel, because the admin user has not been defined yet; so in the next step it is the turn of defining the admin user.

### Django's admin panel

To enter the admin panel, a username and password are needed. Enter the following command in the terminal:

`python manage.py createsuperuser` Django asks you for a username (Figure 32).

![Figure 32: Running the command createsuperuser](../images/p305-01.png)
*Figure 32: Running the command createsuperuser*

As is clear, it has suggested the current Windows user name as the username.

You can enter the username admin or any other username you like, then enter in order the email, the password and the repeat of the password (Figure 33).

![Figure 33: Successful creation of the admin user](../images/p305-02.png)
*Figure 33: Successful creation of the admin user*

<!-- page 300 -->

> **Note**
>
> You can leave the email empty, and also if you enter a simple password, it will warn you as in Figure 34.

![Figure 34: The warning about a simple admin password](../images/p306-01.png)
*Figure 34: The warning about a simple admin password*

After creating the admin user, with the SQLite Viewer extension you can see the created user in the table `auth_user` as in Figure 35.

![Figure 35: Showing the created admin user in the database](../images/p306-02.png)
*Figure 35: Showing the created admin user in the database*

<!-- page 301 -->

Now, to enter Django's admin management panel, turn on the Django server and open the admin page by typing the following address in the browser's address bar:

http://127.0.0.1:8000/admin/ then sign in with the username and password you made.

The admin panel will be shown as in Figure 36.

![Figure 36: Successful sign-in to Django's admin panel](../images/p307-01.png)
*Figure 36: Successful sign-in to Django's admin panel*

In the Authentication and Authorization¹ section, using Users you can see and manage the users of the site.

With the add button a new user can be created. To create a new user, you must enter the fields username, password and repeat of the password and press the save button (Figure 37).

![Figure 37: The form for creating a new user](../images/p307-02.png)
*Figure 37: The form for creating a new user*

> **Footnotes**
>
> 1- Authentication and authorization

<!-- page 302 -->

You will see a successful save message as in Figure 38. At this step you can record additional information, such as the first name, last name, email and so on, for the created user.

![Figure 38: Successful saving of the user](../images/p308-01.png)
*Figure 38: Successful saving of the user*

To see the list of created users, click on Users (Figure 39).

![Figure 39: Viewing the list of users](../images/p308-02.png)
*Figure 39: Viewing the list of users*

> **Activity**
>
> With the help of your teacher, create another user. Then sign in to the admin panel with different users and check the difference between the different users.

### Adding the city table to the admin panel

If you noticed, in Figure 36 the table of cities was not seen in the admin panel; by doing the steps that follow, you can add the table City to the admin panel.

<!-- page 303 -->

Each app in Django has a file `admin.py`. Open the file `admin.py` in the weather app and introduce the model City to Django's admin as in Figure 40.

![Figure 40: Introducing the model City to Django's admin panel](../images/p309-01.png)
*Figure 40: Introducing the model City to Django's admin panel*

**Explanation of the code**:

**Line 1**: the module admin for managing the admin panel is imported from contrib.

**Line 2**: the model City is imported from the file `models.py`.

**Line 4**: the model City is introduced to the admin panel with the statement register.

Now save the file, then refresh the browser; the table city has been added to Django's admin and the letter s has been added to the end of the model's name (Figure 41).

![Figure 41: City added to the admin panel](../images/p309-02.png)
*Figure 41: City added to the admin panel*

<!-- page 304 -->

### Entering the information of cities

In the admin panel, click the Add button (opposite Citys); you will see the city registration form (Add city) (Figure 42).

![Figure 42: The Add city form](../images/p310-01.png)
*Figure 42: The Add city form*

> **Activity**
>
> Using the information in Table 2, save a few cities in the database with the Add city form.

*Table 2: The longitude and latitude of some cities*

| City name | Latitude (lat) | Longitude (lon) |
| --- | --- | --- |
| Minab | 27.1478 | 57.0738 |
| Hamedan | 37 .7981 | 48 .5146 |
| Tehran | 35 .7219 | 51 .3347 |
| Aleshtar | 33.8632 | 48 .2617 |
| Tafresh | 34 .6936 | 50 .0154 |
| Babol | 36.5387 | 52.6765 |
| Jahrom | 28 .5177 | 53 .5744 |
| Tabriz | 38 .0792 | 46.2887 |
| Sabzevar | 36.2152 | 57 .6678 |
