**Page 287**

### Code notes:

Line 1: the `path` function has been imported.

Line 2: the `show_temp_view` function has been imported from `views.py`.

Line 5: a `path` has been added. This `path` means that if the user opens the site’s home page, `show_temp_view` from inside the `views.py` file is run. The `name` parameter has been added to this `path`.

In Django, every address (`URL`) can have a name so that it can be referred to more easily anywhere else.

This name has no effect on the `URL` address itself and is used only for referring to it.

The `name` parameter in Django paths is like an alias for that address, which is also called a `URL` `name`.

![book image](../images/p293-01.png)

Save the file and start the Django server with `runserver`.

Open the site’s home page in the browser.

Congratulations, you have successfully created your first Django `view` (Figure 16).

Figure 16 output of the first Django `view`

### Activity

By completing the `view` and the `urls.py` file, display Tehran’s temperature information.

Getting to know the `render` function in Django: to display a `view` better, `html` files are used. Each `app` in Django can have its own `html` files separately. To do this, create a folder named `templates` in the `app` and store the `html` files in it. These `html` files are called a `template` in Django.

Look at Figure 17; the path a `request` (web request) takes in Django can be seen.

According to the image, the request sent by the user is first transferred to the Django server, then using the `url` it is sent to the appropriate `view`. Each `view`, with the help of an `html` file or the same `template`, prepares the displayable information and sends it to the user.

![Figure 17 the path a request takes in Django](../images/p293-02.png)

Figure 17 the path a `request` takes in Django


---

**Page 288**

As noted in Figure 17, the `render` function in the `view` can send information to the `html` file so that, with Django’s features, the information sent to the `html` file is combined with it and shown to the user.

Next, in two steps you can send a random number as the air temperature of the city of Hamedan, with the help of the `render` function, to an `html` file and show it to the user.

Step one: open the `views.py` file and change `show_temp_view` as shown in Figure 18.

![Figure 18 using the render function](../images/p294-01.png)

Figure 18 using the `render` function

### Code notes:

Line 1: the `render` function has been imported from the `shortcuts` module.

Line 2: the `random` module has been imported.

Line 5: a random number is chosen as the air temperature for the city of Hamedan; this information will be displayed on the site’s home page.

Line 6: a dictionary including the city name (`city`) and the city temperature (`temp`) has been created and stored in a variable named `context`.

Line 7: the `render` function has been used. Three arguments have been sent to this function. The first argument is `request`, which was received from the `view` input. The second argument is the name of the `html` file in the `templates` folder, and the third argument is a dictionary that has been sent for the `html`.

Step two: create a folder named `templates` in the `weather` `app` and create an `html` file named `show_temp.html` inside it.

The `show_temp.html` file and any other `html` file that is placed in this folder is, in other words, a `template`.


---

**Page 289**

Create the `show_temp.html` file and its content as shown in Figure 19.

![Figure 19 contents of show_temp.html](../images/p295-01.png)

```
شکل 19 محتویات show_temp.html
```

### Code notes:

Line 10: {{`city`}} and {{`temp`}} have been used to display the city name and the city temperature. The {{}} marks are used to display variables in the `template`.

These variables are the keys of the `context` dictionary that the `render` function sent for `show_temp.html`.

As is clear, you can use these variables inside `html` tags in the `template`.

Save the files. Then go into the `terminal` and with the key combination `ctrl` + `c` stop the Django web server and start it again with the `runserver` command.

![book image](../images/p295-02.png)

Now `refresh` the site’s home page. You will see the new changes (Figure 20).

Figure 20 viewing the new changes

The process of displaying the air temperature, from the moment the user’s request enters the Django server until the information is displayed with the `template`, is simulated in Figure 21.

![Figure 21 the process of displaying the air temperature](../images/p295-03.png)

Figure 21 the process of displaying the air temperature


---

**Page 290**

### Activity

Using the `render` function and creating a suitable `template` for the `view`, display the air temperature of your own city with random numbers.

### Displaying the real air temperature

To display the live air temperature of cities, you can use sites such as `https://open-meteo.com`. This site provides a tool for the programmer so they can display the air temperature of different cities.

The `open-meteo` site has a free `API` that, by receiving latitude and longitude, provides the weather information for the desired region in `JSON` format.

For example, if you open the following address in the browser to receive the weather status of the city of Hamedan, the result will be displayed in `JSON` format (Figure 22).

![Figure 22 receiving Hamedan’s temperature from an online API](../images/p296-01.png)

Figure 22 receiving Hamedan’s temperature from an online `API`

```
-meteo.com/v1/forecast?latitude=34.7981&longitude=48.5146&currenthttps://api.open
weather=true
```

An `API` is like a bridge between two programs. That is, when a program (for example a Django project) connects to the internet, through an `API` it can get data from another site.

In this project, weather information is received using the `open-meteo` service `API`. `open-meteo` returns this information as organized data in (`Json`) format, then the Django project displays it.


---

**Page 291**

Sending the `latitude` and `longitude` values to receive weather information is required.

Now, to display the current temperature of the city of Hamedan, change the `show_temp_view` function inside the `views.py` file as shown in Figure 23.

![Figure 23 changing the view to receive information from the API](../images/p297-01.png)

Figure 23 changing the `view` to receive information from the `API`

### Code notes:

Line 2: the `requests` library has been imported. This library must already be installed. With the command

```
(pip install requests)
```

Line 5: the `latitude` and `longitude` values are the same geographic latitude and longitude that have been specified for the city of Hamedan and stored in the variables `lat` and `lon`.

Lines 6 and 7: the request text has been prepared as `get` and using `lat` and `lon`.

Line 8: with `try`, possible errors have been handled; for example, if the internet is not connected, `except` on line 11 will set the value of `temp` to `None` and the site will not face a problem.

Line 9: the request has been sent to the `open-meteo.com` server and the result in `json` format has been stored in the `data` dictionary.

Line 10: the `temperature` value has been extracted from the `data` dictionary and stored in the `temp` variable.

In the `show_temp.html` file, apply changes for error handling as shown in Figure 24.

![Figure 24 changes in the template for handling possible errors](../images/p297-02.png)

Figure 24 changes in the `template` for handling possible errors


---

**Page 292**

### Code notes:

Line 10: in the `template`, the conditional `if` statement has been used. If `temp` has a value and is not `None`, the city temperature is displayed.

Line 13: if an error occurs, an appropriate message is shown to the user.

Now save the files and after making sure you are connected to the internet, `refresh` the site’s home page. The output of the site’s home page will be like Figure 25. (Obviously the air temperature may be displayed differently for you, and of course the speed at which the home page opens relates to your internet speed, because in the code you have connected to `open-meteo.com`.)

![Figure 25 displaying Hamedan’s temperature online](../images/p298-01.png)

Figure 25 displaying Hamedan’s temperature online

![book image](../images/p298-02.png)

If the connection with the site is not established, the output will be like Figure 26.

Figure 26 displaying an appropriate error to the user

### Activity

Using the `open-meteo.com` site, display the air temperature of your city on the first page of the site.


---
