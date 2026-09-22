**Page 313**

### Code notes:

Line 10: So that city names can be clicked, an `a` tag has been created inside a `p` tag, and the variable {{ `item.title` }} is used to show the link title. The link address (`href`) points to the home page, and the variable {{ `item.id` }} has been assigned to the `id` parameter.

This code adds `id` to the `GET` request and sends it to the home page. For example, if the selected city’s id is 11, the user is taken to the following address:

```
    10|http://127.0.0.1:8000/?id=11
```

In the next step, open `views.py` and change `show_temp_view` as in Figure 56.

![Figure 56 using id to select a city](../images/p319-01.png)

Figure 56 using `id` to select a city

### Code notes:

Line 11: The value of the `id` parameter that was sent through the `GET` method in the address bar is stored in the variable `city_id`.

If the `id` parameter is not in the address bar, the `get`(`'id'`) function used after `GET` will store the value of `city_id` as `None`.

Line 13: If `city_id` has a value, using Django’s `ORM`, the city selected by the user is stored as an object (`object`) in the variable `city`.

Line 15: If `city_id` is equal to `None` (`id` is not in the address bar), the first city is fetched from the database.


---

**Page 314**

Now save all the files and `refresh` the city list page. All cities have links.

Whichever city you click, you will see that city’s air temperature on the new page (Figure 57).

![Figure 57 showing the temperature of a clicked city](../images/p320-01.png)

Figure 57 showing the temperature of a clicked city

Logging in to the site (`login`) At present, the home page and the city list page can be viewed by a guest user and by an admin user.

But any site can have pages that need a `login` (signing in to the site) to be viewed. For example, to see the Django admin panel, you must `login` with the admin username and password.

You can grant access to the part for adding city names only to users who sign in to the site with their own username and password.

Django itself has built-in features for managing users so that you can run `login` and `logout` operations inside the site. You only need to create the required `template` file, namely `login.html`, in the appropriate folder and add a new `path` in the project’s main `urls` file (in the `config` folder).

Stage one: Change the project’s main `urls.py` file as in Figure 58.

![Figure 58 adding a new path for login and logout](../images/p320-02.png)

Figure 58 adding a new `path` for `login` and `logout`


---

**Page 315**

### Code notes:

Line 7: A new `path` has been added, and as a result Django’s user-management `App` (`auth`) will display the `login.html` file with the help of the default `urls` and `views`. To manage user authentication in a Django project, the `django.contrib.auth` module is used.

By adding this line of code to the `urls.py` file, the ability to log in, log out, and change the password on the site is added.

All of these features are managed by the `django.contrib.auth` module, and you do not need to define another `path` by hand.

Stage two: In the `templates` folder of the `weather` `app`, create a new folder named `registration`, then inside it create a file named `login.html` as in Figure 59.

![Figure 59 adding the login.html file](../images/p321-01.png)

Figure 59 adding the `login.html` file

### Code notes:

Line 10: A form with a method of type `post` has been created.

Line 11: The `csrf_token` field has been added to the form. In Django, `csrf_token` is a security value that is placed inside forms so that it can be sure the submitted request really came from the same site and from an authorized user.

This token prevents a `Cross-Site` `Request` `Forgery` attack.

Line 12: It displays the form fields as `<p>` tags in `HTML`.

Line 13: A button of type `submit` has been added to send the information to the Django server.

### Try this

Research and study `csrf_token` and the `Cross-Site` `Request` `Forgery` attack.


---

**Page 316**

Stage three: In the `settings.py` file, make the needed settings for after the `login` and `logout` operations finish, as in Figure 60.

![Figure 60 login and logout settings in settings.py](../images/p322-01.png)

Figure 60 `login` and `logout` settings in `settings.py`

### Code notes

Line 125: After a successful `login`, the user will be redirected to the `home` page. `home` is the same name that was defined for the home page address in `urls.py`.

Line 126: After a successful `logout`, the user will be redirected to the `home` page.

Stage four: In the `show_temp.html` file, add the login and logout buttons as in Figure 61.

![Figure 61 adding login and logout buttons to the home page](../images/p322-02.png)

Figure 61 adding login and logout buttons to the home page


---

**Page 317**

### Code notes:

Line 9: This statement checks whether the user is signed in to the system or not. If `user.is_authenticated` has the value `True`, it means the user has been authenticated and the statements inside this condition will run.

Line 10: In this line an `HTML` form is defined that sends the request with the `POST` method to the account logout address.

Line 14: `else` has been used, and it means what should be shown to the user if the user is not `login`.

Line 15: In this line a form with the `GET` method is defined that directs the user to the site login page, namely the `login` page.

Now save the files and stop and restart the Django server. Then `refresh` the site’s home page. If the user has not `login`, they will see the site login button (Figure 62).

![Figure 62 showing the login button for a guest user](../images/p323-01.png)

Figure 62 showing the login button for a guest user

By clicking the site login button, the user is taken to the `login` page (Figure 63).

![Figure 63 site login form](../images/p323-02.png)

Figure 63 site login form


---

**Page 318**

After a successful login to the site, the user is taken to the site’s home page, and this time the site logout button is shown to the user.

If the user clicks the site logout button, they will leave the site and will immediately be taken to the home page.

Registering a new city with a site member user Until now you could only register cities in the admin panel and with the `admin` user. But it is possible for member users of the site to register a new city without going to the admin panel.

To do this, you can add this feature to the site by using Django forms and carrying out the four stages below.

1 Create `forms.py` to build the new-city registration form

2 Build a simple `template` for the form

3 Build the `add_city_view` function to display the form

4 Add a special `path` for the form in the `urls.py` file

5 Place the “Add city” link on the home page Stage one: Create a new file in the `weather` folder named `forms.py` and complete it as in Figure 64.

![Figure 64 creating CityForm](../images/p324-01.png)

Figure 64 creating `CityForm`


---

**Page 319**

### Code notes:

Line 1: The `forms` module has been `import`ed into this file. This module supports all work related to forms.

Line 2: The `City` class from the `model` file has been `import`ed into this file. `City` is the same cities model that we defined previously.

Line 4: A class named `CityForm` has been created that inherits from `ModelForm`.

Line 5: To specify the model and the fields you want to display, you must use a `Meta` class inside the main class and specify the model and fields in it.

Line 6: The `City` class has been set as the `model`.

Line 7: The list of fields you want to display has been set.

Stage two: Create the `add_city.html` file as in Figure 65.

![Figure 65 adding add_city.html](../images/p325-01.png)

```
شکل 65 افزودن add_city.html
```

### Code notes:

A form with a method of type `post` has been created. This form takes the latitude and longitude as well as the city name from the user and sends them to the Django server to be stored in the database.


---
