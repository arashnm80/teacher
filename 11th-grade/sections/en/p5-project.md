<!-- page 280 -->

## Creating the weather project

In VSCode, click the Open Folder option from the File menu. Then create a new folder named meteo at a path of your choice and open the meteo folder you made (Figure 5):

![Figure 5: Opening the meteo folder](../images/p286-01.png)
*Figure 5: Opening the meteo folder*

Open the terminal again and run the following command (Figure 6):

django-admin startproject config .

![Figure 6: Creating the project](../images/p286-02.png)
*Figure 6: Creating the project*

<!-- page 281 -->

The previous command creates the project folder named Config in the current path, which contains the settings file `settings.py` and the main files of the project. The dot at the end of the command above means the current path.

### Getting to know some of the project's main files

**The file `settings.py`**: the main settings of the project are in this file.

**The file `urls.py`**: whenever the user enters an address (URL), this file decides which page or part the site shows.

> **Curiosity**
>
> Research the use of the other files in the project.

### Running the Django project

Run the following command in the terminal.

`python manage.py runserver` The command runserver sets up a small virtual web server for the Django project; this web server is only for the Django programmer so that they can run the Django project on their own computer (Figure 7).

![Figure 7: Successful start of the Django web server](../images/p287-01.png)
*Figure 7: Successful start of the Django web server*

<!-- page 282 -->

After running the command, a file named `db.sqlite3` is made next to the file `manage.py`. This file is Django's default database. Django uses this file to manage the database and tables.

As is shown in Figure 7, you can see your site at the address http://127.0.0.1:8000.

By typing the address above in the browser's address bar, you see the main page of the site similar to Figure 8. You may see a different picture because of different versions of Django.

![Figure 8: Successful run of the site](../images/p288-01.png)
*Figure 8: Successful run of the site*

The IP address on which Django runs is 127.0.0.1. This address is known as the local address. This IP points to the current computer, that is, the very computer on which you ran the Django server. If your computer is on a network, other computers cannot connect to your computer with this address.

> **Curiosity**
>
> Check what web servers and databases are used for the projects that are in use on the internet.

### Making the first app in Django

A Django project can include one or several apps (applications). The project you created with the startproject command has no app yet. In Django you can create an app for independent tasks.

Suppose your project is a factory in the real world; each of the factory's production units can be like an app. For example, the unit responsible for painting cars can work independently of the other units. It is enough that a car is delivered to this unit and the requested colour is specified. This unit does its job and delivers the car painted.

Each app does a specific job and must be created in a way that can be reused, that is, an app can be used in another project and do the same job well.

<!-- page 283 -->

To make an app, the startapp command is used; first stop the Django server (with ctrl + c) and then run the following command.

`python manage.py startapp weather` A folder named weather is made. The weather folder is in fact a Django app that is responsible for showing the weather of the wanted city.

After making the weather app the structure of the project will be like Figure 9.

![Figure 9: The content of the weather app](../images/p289-01.png)
*Figure 9: The content of the weather app*

**Introducing the created app to Django in `settings.py`**

At this step, the app that was made must be introduced to Django. For this open the file `settings.py` and add weather to the end of the list `INSTALLED_APPS` as in Figure 10.

![Figure 10: Adding weather to `installed_apps`](../images/p289-02.png)
*Figure 10: Adding weather to `installed_apps`*

<!-- page 284 -->

### Making the first view

Each view that is in the file `views.py` interacts with the user according to its job, so to show the temperature of a city, a view must be made.

View files in Django are responsible for answering the users' requests, that is, they take the user's Request after routing and give that request a correct response.

**First step**: open the file `views.py`. Add a function named `show_temp_view` as in Figure 11:

![Figure 11: Creating a view named `show_temp_view`](../images/p290-01.png)
*Figure 11: Creating a view named `show_temp_view`*

**Explanation of the code**:

**Line 1**: the class HttpResponse is imported from the http module.

**Line 3**: a function named `show_temp_view` is created. Every view in Django is a function that must have the parameter request.

**Line 4**: an object of the type HttpResponse is created. HttpResponse holds the final content sent to the browser and specifies what the user gets from the server.

The function `show_temp_view` in the file `views.py` will only show a simple text.

Save the file and start the Django server with `python manage.py runserver`.

Enter the address of the main page; you still see the welcome page. So you need to make changes so that, on the main page of the site, instead of the welcome the text "Hamedan 27 degrees Celsius" is shown. Open the file `urls.py` in the config folder (Figure 12).

<!-- page 285 -->

![Figure 12: The file `urls.py`](../images/p291-01.png)
*Figure 12: The file `urls.py`*

After the project is created, the file `urls.py` is also created next to `settings.py`. Whenever the user enters an address (URL), this file decides which page or part the site shows.

**Explanation of the code**:

**Line 4**: Django uses a list named urlpatterns to manage the addresses of the pages of the site.

**Line 5**: each member of urlpatterns is a path that is equal to the address of a page in the site. By default there is a path for the page of Django's admin panel with the value /admin, which is equal to the address http://127.0.0.1:8000/admin in the browser.

Open the address http://127.0.0.1:8000/admin in the browser. The admin panel sign-in page, as in Figure 13, asks you for a username and password. Next you will learn how to create a username and password.

![Figure 13: The admin panel sign-in page](../images/p291-02.png)
*Figure 13: The admin panel sign-in page*

<!-- page 286 -->

**Second step**: enter the file `urls.py` again and make changes as in Figure 14 in the file.

![Figure 14: Adding a new path](../images/p292-01.png)
*Figure 14: Adding a new path*

**Explanation of the code**:

**Line 2**: the module include is imported.

**Line 6**: a new path is added. The first argument of the function path in this statement is only an empty string, which means that if in the address (URL) that reached the Django server nothing was written after the address of the site, then, using the module include, go to the file `urls.py` in the weather app and continue the work from there. In fact this line sends the requests of the main page to the weather app.

**Third step**: enter the weather folder and create a `urls.py` for the weather app as in Figure 15. Each app can have its own `urls.py`.

![Figure 15: Creating the file `urls.py` for the app](../images/p292-02.png)
*Figure 15: Creating the file `urls.py` for the app*
