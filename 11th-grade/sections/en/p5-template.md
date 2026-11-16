<!-- page 287 -->

**Explanation of the code**:

**Line 1**: the function path is imported.

**Line 2**: the function `show_temp_view` is imported from `views.py`.

**Line 5**: a path is added. This path means that if the user opens the main page of the site, `show_temp_view` from inside the file `views.py` should run. The parameter name has been added to this path.

In Django each address (URL) can have a name so that it can be referred to more easily anywhere else. This name has no effect on the URL address itself and is only used for referring.

The parameter name in Django's paths is like a nickname for that address, which is also called the URL name.

![Figure 16: The output of the first Django view](../images/p293-01.png)
*Figure 16: The output of the first Django view*

Save the file and start the Django server with runserver.

Open the main page of the site in the browser.

Congratulations, you have successfully created your first Django view (Figure 16).

> **Activity**
>
> By completing the view and the file `urls.py`, show the temperature information of Tehran.

## Getting to know the render function

In Django, html files are used to show a view better. Each app in Django can have its own html files separately; to do this, create a folder named templates in the app and save the html files in it. These html files are called templates in Django.

Look at Figure 17; the path a request (a web request) goes through in Django can be seen.

According to the picture, the request sent by the user is first passed to the Django server, then, using the url, it is sent to the suitable view; each view, with the help of an html file, that is the template, prepares the displayable information and sends it to the user.

![Figure 17: The path a request takes in Django](../images/p293-02.png)
*Figure 17: The path a request takes in Django*

<!-- page 288 -->

As Figure 17 shows, the function render in the view can send information to the html file so that, with the help of Django's capabilities, the information sent to the html file is combined with it and shown to the user.

Next, in two steps you can send a random number as the air temperature of the city of Hamedan to an html file with the help of the function render and show it to the user.

**First step**: open the file `views.py` and change `show_temp_view` as in Figure 18.

![Figure 18: Using the function render](../images/p294-01.png)
*Figure 18: Using the function render*

**Explanation of the code**:

**Line 1**: the function render is imported from the module shortcuts.

**Line 2**: the module random is imported.

**Line 5**: a random number is chosen as the air temperature for the city of Hamedan; this information will be shown on the main page of the site.

**Line 6**: a dictionary including the name of the city (city) and the temperature of the city (temp) is created and stored in a variable named context.

**Line 7**: the function render is used. Three arguments are sent to this function. The first argument is request, which was received from the input of the view. The second argument is the name of the html file in the templates folder and the third argument is a dictionary that is sent to the html.

**Second step**: make a folder named templates in the weather app and create an html file named `show_temp.html` inside it.

The file `show_temp.html` and any other html file placed in this folder is, as the term goes, a template.

<!-- page 289 -->

Create the file `show_temp.html` and its content as in Figure 19.

![Figure 19: The content of `show_temp.html`](../images/p295-01.png)
*Figure 19: The content of `show_temp.html`*

**Explanation of the code**:

**Line 10**: {{city}} and {{temp}} are used to show the name of the city and the temperature of the city. The sign {{}} is used to show variables in a template.

These variables are the keys of the dictionary context, which the function render sent for `show_temp.html`.

As is clear, you can use these variables in the template inside html tags. Save the files. Then enter the terminal and stop the Django web server with the key combination ctrl + c and start it again with the command runserver. Now refresh the main page of the site. You will see the new changes (Figure 20).

![Figure 20: Seeing the new changes](../images/p295-02.png)
*Figure 20: Seeing the new changes*

![Figure 21: The process of showing the air temperature](../images/p295-03.png)
*Figure 21: The process of showing the air temperature*

The process followed to show the air temperature, from the moment the user's request enters the Django server to showing the information with the template, is simulated in Figure 21.

<!-- page 290 -->

> **Activity**
>
> Using the function render and creating a suitable template for the view, show the air temperature of your own city with random numbers.

## Showing the real air temperature

To show the instantaneous air temperature of cities you can use sites such as https://open-meteo.com. This site gives the programmer a tool to show the air temperature of different cities. The site open-meteo has a free API that, by receiving the longitude and latitude, gives the weather information of the wanted region in JSON format.

For example, if you open the following address in the browser to get the weather of the city of Hamedan, the result will be shown in JSON format (Figure 22).

![Figure 22: Getting the temperature of the city of Hamedan from an online API](../images/p296-01.png)
*Figure 22: Getting the temperature of the city of Hamedan from an online API*

-`meteo.com/v1/forecast?latitude=34.7981&longitude=48.5146&current` https://api.open `weather=true` An API is like a bridge between two programs. That is, when a program (for example the Django project) connects to the internet, it can get data from another site through the API.

In this project, weather information is received using the API of the service open-meteo. open-meteo returns this information as organised data in the (Json) format, and then the Django project shows it.

<!-- page 291 -->

Sending the values of latitude and longitude to receive the weather information is compulsory.

Now, to show the current temperature of the city of Hamedan, change the function `show_temp_view` inside the file `views.py` as in Figure 23.

![Figure 23: Change in the view to receive information from the API](../images/p297-01.png)
*Figure 23: Change in the view to receive information from the API*

**Explanation of the code**:

**Line 2**: the library requests is imported. This library must be installed beforehand. With the command (`pip install requests`)

**Line 5**: the values latitude and longitude are the geographic latitude and longitude specified for the city of Hamedan and stored in the variables lat and lon.

**Lines 6 and 7**: the request text is prepared as a get request using lat and lon.

**Line 8**: a possible error is managed using try; for example if the internet is not connected, the except in line 11 will make the value of temp None and the site does not run into trouble.

**Line 9**: the request is sent to the server `open-meteo.com` and the result in json format is stored in the dictionary data.

**Line 10**: the value of temperature is extracted from the dictionary data and stored in the variable temp.

In the file `show_temp.html` make changes to manage errors as in Figure 24.

![Figure 24: Changes in the template to manage a possible error](../images/p297-02.png)
*Figure 24: Changes in the template to manage a possible error*

<!-- page 292 -->

**Explanation of the code**:

**Line 10**: in the template the conditional statement if is used. If temp has a value and is not None, the temperature of the city is shown.

**Line 13**: if an error happens, a suitable message is shown to the user.

Now save the files and, after making sure of the internet connection, refresh the main page of the site. The output of the main page of the site will be as in Figure 25 (clearly, the air temperature may be shown differently for you, and of course the speed of opening the main page of the site depends on your internet speed, because in the code you have connected to `open-meteo.com`.)

![Figure 25: Showing the temperature of Hamedan online](../images/p298-01.png)
*Figure 25: Showing the temperature of Hamedan online*

![Figure 26: Showing a suitable error to the user](../images/p298-02.png)
*Figure 26: Showing a suitable error to the user*

If the connection with the site is not made, the output will be as in Figure 26.

> **Activity**
>
> Using the site `open-meteo.com`, show the air temperature of your own city on the first page of the site.
