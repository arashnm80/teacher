<!-- page 326 -->

### Coding bug two

If the user changes the id of the city by hand in the browser's address bar and the id entered does not exist in the database, an error as in Figure 76 is shown on the main page of the site.

![Figure 76: The error when the city id is wrong](../images/p332-01.png)
*Figure 76: The error when the city id is wrong*

**The solution to the first and second bug**: to fix this flaw, change the code of `show_temp_view` as in Figure 77.

![Figure 77: Fixing the flaw in the code](../images/p332-02.png)
*Figure 77: Fixing the flaw in the code*

<!-- page 327 -->

**Explanation of the code**:

**Line 14**: instead of the function get, the functions filter and first are used. The function get gives an error if the wanted value does not exist in the database. But the function filter does not have this behaviour and will not cause an error. So it covers the **second bug**.

**Line 17**: if city has no value, the request is not sent to the weather API and `show_temp.html` is shown directly. This line also covers the first bug; before fixing the code, if there was no city in the database, the value of city would become None. So when getting lat the code would fail. With the changes made, this bug is fixed.

### A security bug

If the user is not a member of the site but has the address of the page for adding and deleting cities, they can add a city or delete a city without logging in to the site.

**The solution to the security bug**: to fix this flaw, change the code of `add_city_view` as in Figure 78.

![Figure 78: Fixing the security bug of the code](../images/p333-01.png)
*Figure 78: Fixing the security bug of the code*

**Explanation of the code**:

**Line 36**: if the user has not logged in, in the next line they will be taken to the login page. You can use the same code for `delete_city_view` too.

With these changes, if the user is not logged in but enters the address of adding a city and deleting a city in the browser, they will be taken to the login page.

> **Curiosity**
>
> Check what other things could improve this project.

<!-- page 328 -->

## Competency assessment: developing a web application

**Work performance standard**: the student can, by making a Model in Django and using HTML forms, implement the connection with the database and store and retrieve the information users enter in tables.
