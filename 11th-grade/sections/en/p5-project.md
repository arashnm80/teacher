**Page 280**

### Creating the weather project

In `Vscode`, from the `File` menu, click `Open` `Folder`. Then create a new folder named `meteo` in a path of your choice and open the `meteo` folder you created (Figure 5):

![Figure 5 opening the meteo folder](../images/p286-01.png)

Figure 5 opening the `meteo` folder

Open the terminal again and run the following command (Figure 6):

```
.django-admin startproject config
```

![Figure 6 creating the project](../images/p286-02.png)

Figure 6 creating the project


---

**Page 281**

The previous command creates a project folder named `Config` in the current path, which contains the `settings.py` settings file and the project’s main files. The period at the end of the command above means the current path.

Getting to know some of the project’s main files: the `settings.py` file: the project’s main settings are placed in this file.

The `urls.py` file: whenever the user goes to an address (`URL`), this file decides which page or section of the site to display.

### Try this

Research the purpose of the other files in the project.

Running the Django project: run the following command in the terminal.

```
python manage.py runserver
```

The `runserver` command starts a small virtual web server (`web` `server`) for the Django project. This web server is only for the Django programmer so they can run the Django project on their own computer (Figure 7).

![Figure 7 successfully starting the Django web server](../images/p287-01.png)

Figure 7 successfully starting the Django web server


---

**Page 282**

After you run the command, a file named `db.sqlite3` is created next to the `manage.py` file. This file is Django’s default database. Django uses this file to manage the database and tables.

As shown in Figure 7, you can view your site at the address `http://127.0.0.1:8000`.

By typing the address above in the browser’s address bar, you see the site’s home page similar to Figure 8. You may see a different image because of different Django versions.

![Figure 8 successfully running the site](../images/p288-01.png)

Figure 8 successfully running the site

The `ip` address that Django runs on is 127.0.0.1. This address is known as the `local` address. This `ip` points to the current computer, meaning the same computer on which you have run the Django server. If your computer is on a network, other computers cannot connect to your computer with this address.

### Try this

Investigate which web servers and which databases are used for projects that are in use on the internet.

Creating the first `app` in Django: a Django project can include one or more `app`s (applications). The project you created with the `startproject` command still has no `app`. In Django you can create an `app` for independent tasks.

Suppose your project is a factory in the real world. Each of the factory’s production units can be like an `app`. For example, the unit responsible for painting cars can operate independently of the other units. It is enough to deliver a car to this unit and specify the requested color. This unit does its work and delivers the painted car.

Each `app` performs a specific task and should be created so that it is reusable, meaning you can use an `app` in another project and it performs the same task well.


---

**Page 283**

To create an `app`, the `startapp` command is used. First stop the Django server (with `ctrl` + `c`) and then run the following command.

```
python manage.py startapp weather
```

A folder named `weather` is created. The `weather` folder is in fact a Django `app` whose task is to display the weather for the desired city.

After creating the `weather` `app`, the project structure will be like Figure 9.

![Figure 9 contents of the weather app](../images/p289-01.png)

Figure 9 contents of the `weather` `app`

Introducing the created `app` to Django in `settings.py`: at this stage, you need to introduce the created `app` to Django. To do this, open the `settings.py` file and add `weather` to the end of the `INSTALLED_APPS` list as shown in Figure 10.

![Figure 10 adding weather to installed_apps](../images/p289-02.png)

Figure 10 adding `weather` to `installed_apps`


---

**Page 284**

Creating the first `view`: each `view` in the `views.py` file interacts with the user according to its task, so to display a city’s temperature, a `view` must be created.

`View` files in Django are responsible for responding to user requests, meaning they receive the user’s `Request` after routing and give that request a correct response.

Step one: open the `views.py` file. Add a function named `show_temp_view` as shown in Figure 11:

![Figure 11 creating a view named show_temp_view](../images/p290-01.png)

Figure 11 creating a `view` named `show_temp_view`

### Code notes:

Line 1: the `HttpResponse` class has been imported from the `http` module.

Line 3: a function named `show_temp_view` has been created. Every `view` in Django is a function that must have the `request` parameter.

Line 4: an `object` of type `HttpResponse` has been created. `HttpResponse` holds the final content sent to the browser and determines what the user receives from the server.

The `show_temp_view` function in the `views.py` file will display only a simple text.

Save the file and start the Django server with `python` `manage.py` `runserver`.

Enter the home page address; you still see the welcome page. So you need to make changes so that on the site’s home page, instead of the welcome message, the text “Hamedan 27 degrees Celsius” is displayed.

Open the `urls.py` file in the `config` folder (Figure 12).


---

**Page 285**

![Figure 12 the urls.py file](../images/p291-01.png)

Figure 12 the `urls.py` file

After creating the project, the `urls.py` file is also created next to `settings.py`. Whenever the user goes to an address (`URL`), this file decides which page or section of the site to display.

### Code notes:

Line 4: Django uses a list named `urlpatterns` to manage the site’s page addresses.

Line 5: each member of `urlpattrns` is a `path` that corresponds to the address of a page on the site. By default there is a `path` for Django’s admin panel page with the value `/admin`, which corresponds to the address `http://127.0.0.1:8000/admin` in the browser.

Open the address `http://127.0.0.1:8000/admin` in the browser. The admin panel login page, as in Figure 13, asks you for a username and password. Later you will learn how to create a username and password.

![Figure 13 the admin panel login page](../images/p291-02.png)

Figure 13 the admin panel login page


---

**Page 286**

Step two: go back into the `urls.py` file and apply changes as shown in Figure 14.

![Figure 14 adding a new path](../images/p292-01.png)

Figure 14 adding a new `path`

### Code notes:

Line 2: the `include` module has been imported.

Line 6: a new `path` has been added. The first argument of the `path` function in this command is only an empty string, and it means that if in the address (`URL`) that reaches the Django server, no expression was entered after the site address, use the `include` module to go to the `urls.py` file in the `weather` `app` and continue from there. In fact this line sends home page requests to the `weather` `app`.

Step three: go into the `weather` folder and create a `urls.py` for the `weather` `app` as shown in Figure 15.

Each `app` can have its own `urls.py`.

![Figure 15 creating the urls.py file for the app](../images/p292-02.png)

Figure 15 creating the `urls.py` file for the `app`


---
