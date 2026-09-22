# Developing a web application


---

**Page 295**

## Learning unit 2

## Developing a web application

### Have you ever thought

How does a site communicate with a database?

How does a web application recognize a guest user?

How is the information that users enter in forms stored in the database?

How can a programmer prevent errors from occurring on the site?

### By the end, the student is expected to

1 be able to apply changes in the database using Django.

2 understand the concept of field and table in Django and reason about it.

3 using Django, be able to store form information in the database.

4 become familiar with the concept of `ORM` in Django and be able to write simple queries.

5 recognize common problems and bugs in web applications and be able to fix the problems in practice.

### Performance standard

The student should be able, by building a `Model` in Django and using `HTML` forms, to implement communication with the database and store and retrieve the information that users enter in tables.


---

**Page 296**

### Creating the city table in the database

Up to this stage your site only displays the temperature of cities that you have specified in the `view`, meaning in `show_temp_view` the city name is fixed and the temperature of one city will always be displayed. A better method is for the guest user to be able to choose their desired city.

To implement this capability, you need to store city information together with the latitude and longitude of each city in the database, then when the user enters the site, they see a list of cities and by clicking on the city name see the temperature of their desired city.

To implement this capability you must create a table (`table`) in the database.

Each `app` has a file named `models.py`. Django uses models (`model`) to build tables. Each model in Django corresponds to a table with the same name in the database. As a first step, inside the `models.py` file the class needed to define the table and the table columns must be created.

Open the `models.py` file in the `weather` `app`. Then change the content of this file as shown in Figure 27.

![Figure 27 creating the City model](../images/p302-01.png)

Figure 27 creating the `City` model

### Code notes:

Line 1: the `models` module has been imported from the `django.db` module. In fact with this line, the tools and classes needed to define database models (`Database` `Models`) are imported.

Line 3: the `City` class has been created to build the cities table by inheriting from `Model`. `Model` is Django’s base class for building models (database tables) and provides the facilities needed to communicate with the database.

Line 4: this command builds a field in the table for holding the city name as text, with a maximum length of 50 characters. For `CharField`, setting `max_length` is required.

Line 5: `FloatField` has been used to hold decimal numbers. Geographic latitude (`Latitude`) and geographic longitude (`Longitude`) are both decimal numbers.


---

**Page 297**

To use the `City` model, the equivalent table needs to be created in the database.

In the terminal run the `makemigrations` command as shown in Figure 28.

![Figure 28 running the makemigrations command](../images/p303-01.png)

Figure 28 running the `makemigrations` command

When you run `makemigrations`, inside the `weather` `app`, a file named `0001_initial.py` is created in the `migrations` folder. This file prepares the code needed to turn the model into a real table.

In the next step run the `migrate` command in the terminal as shown in Figure 29.

![Figure 29 running the migrate command](../images/p303-02.png)

Figure 29 running the `migrate` command


---

**Page 298**

After running `migrate`, Django’s default tables and the `city` table are created in the `db.sqlite3` database.

Viewing database tables: to view the structure and content of the tables inside the database, you can install the `SQLite` `Viewer` extension as a helper tool. To install this extension make sure the internet is connected (Figure 30).

![Figure 30 searching for the SQLite Viewer extension](../images/p304-01.png)

Figure 30 searching for the `SQLite` `Viewer` extension

After installing the mentioned extension, by clicking on the `db.sqlite3` file you will see Django’s default tables and the `city` table (Figure 31).

![Figure 31 database tables](../images/p304-02.png)

Figure 31 database tables


---

**Page 299**

As is clear in Figure 31, the `city` table has been created with the `weather` prefix. By clicking on the `weather_city` table, the list of fields is displayed on the right. At present there is no record in the `city` table.

With the `SQLite` `Viewer` extension you can only view the content and structure of the tables and there is no possibility of storing information.

To change the content of the `city` table or to add new city names to the table, you need to enter Django’s admin panel. Of course you still cannot enter city-related data into the database through the `admin` panel, because the `admin` user has not been defined yet; so in the next step it is time to define the `admin` user.

Django management panel: to enter the admin panel, a username and password are needed. Enter the following command in the terminal:

```
python manage.py createsuperuser
```

Django asks you for a username (Figure 32).

![Figure 32 running the createsuperuser command](../images/p305-01.png)

Figure 32 running the `createsuperuser` command

As is clear, it has suggested the current Windows user’s name as the username.

You can enter the username `admin` or any other username of your choice, then enter the email, password, and password confirmation in order (Figure 33).

![Figure 33 successfully creating the admin user](../images/p305-02.png)

Figure 33 successfully creating the admin user


---

**Page 300**

### Note

You can leave the email empty; also if you enter a simple password, as in Figure 34 it will warn you.

![Figure 34 warning that the admin password is simple](../images/p306-01.png)

Figure 34 warning that the admin password is simple

After creating the admin user, with the `SQLite` `Viewer` extension you can see the created user in the `auth_user` table as in Figure 35.

![Figure 35 displaying the created admin user in the database](../images/p306-02.png)

Figure 35 displaying the created `admin` user in the database


---

**Page 301**

Now to enter Django’s admin management panel, turn on the Django server and open the admin page by typing the following address in the browser’s address bar:

```
http://127.0.0.1:8000/admin/
```

Then log in with the username and password you created.

The admin panel will be displayed as in Figure 36.

![Figure 36 successfully logging into the Django admin panel](../images/p307-01.png)

Figure 36 successfully logging into the Django admin panel

In the `1Authentication` `and` `Authorization` section, using `Users` you can view and manage the site’s users.

Using the `add` button you can create a new user. To create a new user, you need to enter the username, password, and password confirmation fields and press the `save` button (Figure 37).

![Figure 37 the form for creating a new user](../images/p307-02.png)

Figure 37 the form for creating a new user

1- Authentication and authorization


---

**Page 302**

You will see a successful save message as in Figure 38. At this stage you can register additional information, such as first name, last name, email, and so on, for the created user.

![Figure 38 successfully saving the user](../images/p308-01.png)

Figure 38 successfully saving the user

To view the list of created users, click on `Users` (Figure 39).

![Figure 39 viewing the list of users](../images/p308-02.png)

Figure 39 viewing the list of users

### Activity

With your instructor’s help, create another user. Then `login` to the admin panel with different users and examine the differences between different users.

Adding the city table to the admin panel: if you have paid attention, in Figure 36 the cities table was not seen in the admin panel. By carrying out the steps that follow, you can add the `City` table to the admin panel.


---

**Page 303**

Each `app` in Django has an `admin.py` file. Open the `admin.py` file in the `weather` `app` and introduce the `City` model to Django admin as shown in Figure 40.

![Figure 40 introducing the City model to the Django admin panel](../images/p309-01.png)

Figure 40 introducing the `City` model to the Django admin panel

### Code notes:

Line 1: the `admin` module for managing the admin panel has been imported from `contrib`.

Line 2: the `City` model has been imported from the `models.py` file.

Line 4: the `City` model has been introduced to the admin panel with the `register` command.

Now save the file, then `refresh` the browser; the `city` table has been added to Django admin and the letter `s` has been added to the end of the model name (Figure 41).

![Figure 41 City being added to the admin panel](../images/p309-02.png)

Figure 41 `City` being added to the admin panel


---

**Page 304**

Entering city information: in the admin panel, click the `Add` button (next to `Citys`); you will see the city registration form (`Add` `city`) (Figure 42).

![Figure 42 the Add city form](../images/p310-01.png)

Figure 42 the `Add` `city` form

### Activity

Using the information in Table 2, store a few cities in the database with the `Add` `city` form.

Table 2 latitude and longitude of a few cities

City name

Latitude (`lat`)

Longitude (`lon`)

Minab27.1478

57.0738

Hamedan.798137

.514648

Tehran.721935

.334751

Aleshtar33.8632

.261748

Tafresh.693634

.015450

Babol36.5387

52.6765

Jahrom.517728

.574453

Tabriz.079238

46.2887

Sabzevar36.2152

.667857


---
