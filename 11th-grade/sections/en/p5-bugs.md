**Page 326**

Coding bug two:

If the user manually changes the city’s `id` in the browser address bar and the entered `id` does not exist in the database, an error like Figure 76 is shown on the site’s home page.

![Figure 76 error when the city id is wrong](../images/p332-01.png)

Figure 76 error when the city id is wrong

Solution for bugs one and two: To fix this flaw, change the `show_temp_view` code as in Figure 77.

![Figure 77 fixing the code flaw](../images/p332-02.png)

Figure 77 fixing the code flaw


---

**Page 327**

### Code notes:

Line 14: Instead of using the `get` function, the `filter` and `first` functions have been used. The `get` function raises an error if the desired value does not exist in the database. But the `filter` function does not have this behavior and will not cause an error. So it covers bug two.

Line 17: If `city` has no value, the request is not sent to the weather `API` and `show_temp.html` is displayed directly. This line also covers bug one; before the codes were corrected, if no city existed in the database, the value of `city` became `None`. So when getting `lat` the code hit an error. With the changes that were applied, this bug has been fixed.

Security bug:

If the user is not a site member, but has the address of the add-city and delete-cities pages, without a `login` on the site they can add a city or delete a city.

Solution for the security bug: To fix this flaw, change the `add_city_view` code as in Figure 78.

![Figure 78 fixing the code security bug](../images/p333-01.png)

Figure 78 fixing the code security bug

### Code notes:

Line 36: If the user has not `login`, on the next line they will be taken to the `login` page. You can use the same code for `delete_city_view` as well.

With these changes, if the user is not `login` but enters the add-city and delete-city addresses in the browser, they will be taken to the `login` page.

### Try this

Examine what other things could improve this project.


---

**Page 328**

### Assessment of web application development competency

Performance standard for the work: The student should be able, by building a `Model` in Django and using `HTML` forms, to implement connection with the database and store and retrieve the information that users enter in the tables.

Score

Conditions for doing the work (tools, materials, equipment,

Tools

Results

Row

### Steps

Standard (indicators / judging / scoring)

Earned

time, place, and …)

### Assessment

Made possible

Explain the difference between the structure of a database and its tables. Describe the role and importance of `ORM` in Django.

Recognize the main parts of the Django admin panel and their use. Success in correctly defining the `City` model with the needed fields (such as city name, temperature, and …). Working with `ORM:` writing

3

simple queries with `ORM` to read data (for example `City.objects.all`()).

Success in registering `City` in the admin panel and being able to view, add, and edit data through it Entering a few sample records (a few cities) into the table through the admin panel.

Observation Carry out the Try this tasks Do the work with several practical methods

```
DE: VS Code PostgreSQL فریم‌ورک
```

Database, `ORM`, and admin

Question

1

Success in correctly defining the `City` model with the needed fields (such as city name, temperature, and

Django Personal computer or laptop with operating system

panel

Written …). Working with `ORM:` writing simple queries with `ORM` to read (for example

Time 25 minutes Place computer site

Test

```
City.objects.all()) داده‌ها.
```

Oral

2

Success in registering `City` in the admin panel and being able to view, add, and edit data through it Entering a few sample records (a few cities) into the table through the admin panel.

Explain the difference between the structure of a database and its tables. Describe the role and importance of `ORM` in Django.

1

Recognize the main parts of the Django admin panel and their use Recognize the role of `views` in processing requests and sending responses. Understand how data is sent from the `view` to the `template` (`HTML` template) Become familiar with basic ideas of user interaction (such as clicking a link). Create a `view` and a `template` to display a list of city names that have been read from the database. Implement

3

a city-selection mechanism (for example with a link or a form). Create a `view` that receives the selected city. Display the temperature related to the selected city on the page.

Observation Define suitable `URL`s for access to these features.

```
DE: VS Code PostgreSQL
```

Practical

Working with data and displaying

Django framework Personal computer or laptop with Question

2

Create a `view` and a `template` to display a list of city names that have been

information

operating system Time 25 minutes Place computer site Written

read from the database. Implement a city-selection mechanism (for example with a link or

computer

Test form). Create a `view` that receives the selected city.

2

Oral Display the temperature related to the selected city on the page. Define suitable `URL`s for access to these features.

Explain the role of `views` in processing requests and sending responses Explain how data is sent from the `view` to the `template` (`HTML` template) Explain basic ideas of

1

user interaction (such as clicking a link).

Explain the authentication process (`Login/Logout`) in Django Explain the idea of access levels (`Permissions`) and how to apply them Recognize the security risks of unauthorized access Correctly set up the user login system.

3

Make sure that the add-city and delete-city pages are accessible only for signed-in users (site members) Success in implementing the ability to add a new city Observation and delete an existing city, only by signed-in users Carry out the Try this tasks Practical

```
DE: VS Code PostgreSQL فریم‌ورک
```

Authentication and managing

Question

3

Django Personal computer or laptop with operating system

access

Written

Time 25 minutes Place computer site

Make sure that the add-city and delete-city pages are accessible only for signed-in users (site members) Test

2

Success in implementing the ability to add a new city and delete an existing city, only Oral by signed-in users.

Explain the authentication process (`Login/Logout`) in Django. Explain the idea of access levels (`Permissions`) and how to apply them. Explain security

1

risks and unauthorized access Correctly set up the user login system.


---

**Page 329**

Identify types of coding bugs (logical, runtime) Understand basic principles of web security (such as preventing code injection, `CSRF` attacks, and …).

Become familiar with basic ideas of code and performance optimization.

Fix bug 1 (empty table): Implement correct logic in the `view` or `template` to handle the case when the `City` table is empty, without causing an error. Fix bug 2 (changing the `ID` in the `URL`): Implement checking that the city’s `id` is valid

3

in the `view` before trying to display its information, in order to prevent an error or showing incorrect information.

Fix the security bug (unauthorized access): Make completely sure that no user without a `Login` can gain access to the add/delete city pages and Observation carry out the operations.

Practical

```
DE: VS Code PostgreSQL فریم‌ورک
```

Present cleaner and more efficient code (if possible, depending on the two level

Fixing flaws and optimization

Question

4

Django Personal computer or laptop with operating system

security

Written Fix bug 1 (empty table): Implement correct logic in the `view` or `template`

Time 30 minutes Place computer site

Test to handle the case when the `City` table is empty, without causing an error Fix Oral bug 2 (changing the `ID` in the `URL`): Implement checking that the city’s `id` is valid in the `view` before trying to display its information, in order to prevent an error or showing

2

incorrect information.

Fix the security bug (unauthorized access): Make completely sure that no user without a `Login` can gain access to the add/delete city pages and carry out the operations.

Identify types of coding bugs (logical, runtime) Understand basic principles of web security (such as preventing code injection, `CSRF` attacks, and …).

1

Become familiar with basic ideas of code and performance optimization.

Non-technical competencies, safety,

Achieve all non-technical competencies2

hygiene, environmental considerations, and attitude:

Failing to achieve any of the non-technical competencies1 Yes

Work assessment (competency in doing the work)

No

### Explanation:

1 Criterion for competency in doing the work:

Earn at least score 2 from stages 2 and 3 (critical stages) Earn at least score 2 from the non-technical competencies, safety, hygiene, environmental considerations, and attitude section Earn at least an average of 2 from the work stages

2 Definition of competency levels: Regardless of the level of professional qualification at which a work task is performed, in every workplace a certain quality of doing each job may be expected. The level of competency in doing the work is the basic criterion of assessment.

Skill (level three): Skilled and able to train and guide others, able to plan and analyze, accountable for their own work, dealing with a wide range of jobs and activities Mastery (level four): Expertise in doing the work and training others, creating innovation, adapting, troubleshooting, leading and guiding others.
