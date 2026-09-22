# Creating a web application


---

**Page 276**

## Learning unit 1

## Creating a web application

### Have you ever thought

What differences does a website have from a web application?

How can you build a web application?

How does a web application interact with the user?

### By the end, the student is expected to

1 Become familiar with the advantages of Django.

2 Understand the structure of a Django project.

3 Understand Django’s process for interacting with the user and reason about it.

4 Understand the concepts of `url`, `view`, and `template` in Django.

5 Be able to implement a simple web application in practice.

### Performance standard

The student, with a correct understanding of Django’s structure, should be able to implement a simple web application on their own computer.


---

**Page 277**

What is Django?

Django (`Django`) is an open-source (`open` `source`) `framework` written in the `Python` programming language and used to build and implement the `backend` of websites (`Website`) and web applications (`Web` `Application`).

Table 1 Comparison of a website and a web application

Criterion

Website (`Website`)

```
وب اپلیکیشن (Web Application)
```

Main purpose

Informing and displaying content

Carrying out operations and processing data

User interaction

Little or almost one-way

Much and two-way

Need for login

Usually does not have

Usually has

Server-side processing

Little

Much

Dependence on the `backend`

Little or medium

Very much

Change of content by the user

Usually does not have

Has

Examples

News site, company site, blog User panel, online store, educational

system

Advantages of Django Django is a secure and fast `framework` that puts many ready-made capabilities at the programmer’s disposal.

For this reason, the speed of software development in Django is very high.

In Django projects, as the number of users increases, you can still have a fast and secure website by making only a few changes.

Another advantage of Django is the existence of comprehensive documentation (guides) as well as a large and active community of programmers. This means that if you face a problem while working with Django, with a simple search on the internet you can find many solutions and explanations from other programmers.

![Book image](../images/p283-01.png)

Another important advantage of Django is the many job opportunities in the field of Python and the Django `framework`, which makes it a suitable option for learning and entering the job market.

Large companies in the world and in Iran have

Figure 1 Companies that have used Django

used Django.


---

**Page 278**

### Try this

Research the companies mentioned.

Final project of this book At the end of this book, using Django, a real web application for displaying weather status will be designed (Figure 2).

In this project the user can select the name of a city to display the weather status and view it.

This web application receives weather information online and displays the result in real time.

The project helps you learn how Django works in practice and how a website is built.

![Figure 2 Parts of the final project](../images/p284-01.png)

Figure 2 Parts of the final project

Installing Django First make sure the latest version of Python is installed on your computer and that the computer is connected to the internet. To do this, enter the `Vscode` program; if a file or folder was already open, close it with the `Close` `Folder` command from the `File` menu, then from the `terminal` menu open a new terminal.

Then, as in Figure 3, run the commands in order in the terminal section.


---

**Page 279**

![Figure 3 Installing Django version 5.2.9](../images/p285-01.png)

Figure 3 Installing Django version 5.2.9

Displaying the message `Successfully` `installed` `Django-5.2.9` indicates that Django has been installed successfully.

If you do not see the message that Django was installed successfully, get guidance from your teacher.

You can also install the latest released version of Django; you only need to find the compatible Python version on the `pypi.org` site and the Django page.

```
وارد آدرس https://pypi.org/project/Django شوید و در بخش Programming Language نسخه‌های
```

Observe the Python versions supported by Django (Figure 4).

![Figure 4 Suitable Python versions for Django](../images/p285-02.png)

Figure 4 Suitable Python versions for Django


---
