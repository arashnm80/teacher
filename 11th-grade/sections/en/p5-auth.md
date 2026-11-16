<!-- page 313 -->

**Explanation of the code**:

**Line 10**: so that the city names can be clicked, an a tag is created inside the p tag and, to show the title of the link, the variable {{ `item.title` }} is used. The address of the link (href) points to the main page and the variable {{ `item.id` }} gives a value to the parameter id.

This code adds the id to the GET request and sends it to the main page. For example, if the id of the chosen city is 11, the user is taken to the following address:

```
http://127.0.0.1:8000/?id=11
```

In the next step, open `views.py` and change `show_temp_view` as in Figure 56.

![Figure 56: Using id to choose the city](../images/p319-01.png)
*Figure 56: Using id to choose the city*

**Explanation of the code**:

**Line 11**: the value of the parameter id that was sent through the GET method in the address bar is stored in the variable `city_id`.

If the parameter id is not in the address bar, the function `get('id')` used after GET will store the value of `city_id` as None.

**Line 13**: if `city_id` has a value, using Django's ORM, the city chosen by the user is stored as an object in the variable city.

**Line 15**: if `city_id` is None (id is not in the address bar), the first city is fetched from the database.

<!-- page 314 -->

Now save all the files and refresh the page of the list of cities. All the cities have a link.

Whichever city you click on, the air temperature of that city is seen on the new page (Figure 57).

![Figure 57: Showing the temperature of a clicked city](../images/p320-01.png)
*Figure 57: Showing the temperature of a clicked city*

### Signing in to the site (login)

At the moment, the main page and the page of the list of cities can be seen by the guest user and the admin user. But every site can have pages that need login (signing in to the site) to be seen. For example, to see Django's admin panel, you must log in with the admin's username and password. You can give the ability to reach the part for adding the names of cities only to users who enter the site with their own username and password.

By default Django itself has facilities for managing users so that you can do the login and logout operations inside the site. It is enough to make the needed template file, that is `login.html`, in a suitable folder and add a new path in the main urls file of the project (in the config folder).

**First step**: change the main `urls.py` file of the project as in Figure 58.

![Figure 58: Adding a new path for login and logout](../images/p320-02.png)
*Figure 58: Adding a new path for login and logout*

<!-- page 315 -->

**Explanation of the code**:

**Line 7**: a new path is added and, as a result, it will make Django's user management App (auth), with the help of the default urls and views, show the file `login.html`. To manage the user's authentication in a Django project, the module `django.contrib.auth` is used.

By adding this line of code to the file `urls.py`, the ability to sign in, sign out and change the password is added to the site. All these capabilities are managed by the module `django.contrib.auth` and you do not need to define another path by hand.

**Second step**: in the templates folder of the weather app, create a new folder named registration, then inside it make a file named `login.html` as in Figure 59.

![Figure 59: Adding the file `login.html`](../images/p321-01.png)
*Figure 59: Adding the file `login.html`*

**Explanation of the code**:

**Line 10**: a form with a post-type method is created.

**Line 11**: the field `csrf_token` is added to the form. `csrf_token` in Django is a security value placed inside forms to make sure the request sent really came from the same site and by an authorised user. This token prevents the Cross-Site Request Forgery attack.

**Line 12**: shows the fields of the form as `<p>` tags in HTML.

**Line 13**: a button of the submit type is added to send the information to the Django server.

> **Curiosity**
>
> Research and look into `csrf_token` and the Cross-Site Request Forgery attack.

<!-- page 316 -->

**Third step**: in the file `settings.py`, make the needed settings for after the login and logout operations finish, as in Figure 60.

![Figure 60: The login and logout settings in `settings.py`](../images/p322-01.png)
*Figure 60: The login and logout settings in `settings.py`*

**Explanation of the code**

**Line 125**: after a successful login the user will be taken to the home page. home is the very name that was defined for the address of the main page in `urls.py`.

**Line 126**: after a successful logout the user will be taken to the home page.

**Fourth step**: in the file `show_temp.html`, add the sign-in and sign-out buttons as in Figure 61.

![Figure 61: Adding the sign-in and sign-out buttons to the main page](../images/p322-02.png)
*Figure 61: Adding the sign-in and sign-out buttons to the main page*

<!-- page 317 -->

**Explanation of the code**:

**Line 9**: this statement checks whether the user has signed in to the system or not. If `user.is_authenticated` has the value True, that is, the user is authenticated, the statements inside this condition will run.

**Line 10**: in this line an HTML form is defined that sends the request with the POST method to the address for signing out of the user account.

**Line 14**: else is used, and it means what should be shown to the user if they are not logged in.

**Line 15**: in this line a form with the GET method is defined that guides the user to the sign-in page of the site, that is, the login page.

Now save the files, stop the Django server and start it again. Then refresh the main page of the site. If the user has not logged in, they see the sign-in button (Figure 62).

![Figure 62: Showing the sign-in button for a guest user](../images/p323-01.png)
*Figure 62: Showing the sign-in button for a guest user*

By clicking the sign-in button, the user is taken to the login page (Figure 63).

![Figure 63: The sign-in form of the site](../images/p323-02.png)
*Figure 63: The sign-in form of the site*

<!-- page 318 -->

After a successful sign-in to the site, the user is taken to the main page of the site and this time the sign-out button is shown to the user.

If the user clicks the sign-out button, they are signed out of the site and taken immediately to the main page.

### Registering a new city with a member user of the site

So far you could register cities only in the admin panel and with the admin user. But it is possible for member users of the site to also register a new city without going to the admin panel.

For this you can add this feature to the site by using Django's forms and doing the following four steps.

1. Creating `forms.py` to build the form for registering a new city

2. Making a simple template for the form

3. Making the function `add_city_view` to show the form

4. Adding the path for the form in the file `urls.py`

5. Putting the link "Add city" on the main page

**First step**: create a new file named `forms.py` in the weather folder and complete it as in Figure 64.

![Figure 64: Creating CityForm](../images/p324-01.png)
*Figure 64: Creating CityForm*

<!-- page 319 -->

**Explanation of the code**:

**Line 1**: the module forms is imported in this file. This module supports everything related to forms.

**Line 2**: the class City is imported from the model file in this file. City is the model of the cities that we defined earlier.

**Line 4**: a class named CityForm is made that inherits from ModelForm.

**Line 5**: to set the model and the fields you want to be shown, a Meta class must be used in the main class and the model and the fields are specified in it.

**Line 6**: the class City is set as the model.

**Line 7**: the list of fields you want to be shown is set.

**Second step**: create the file `add_city.html` as in Figure 65.

![Figure 65: Adding `add_city.html`](../images/p325-01.png)
*Figure 65: Adding `add_city.html`*

**Explanation of the code**:

A form with a post-type method is created. This form takes the longitude and latitude and also the name of the city from the user and sends them to the Django server to be saved in the database.
