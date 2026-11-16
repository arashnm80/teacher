<!-- page 276 -->

## Learning unit 1

## Have you ever thought about this

- What are the differences between a website and a web application?

- How can you build a web application?

- How does a web application interact with the user?

## By the end, the student is expected to

1. Get to know the advantages of Django.

2. Understand the structure of a Django project.

3. Understand and reason about how Django works to interact with the user.

4. Understand the concepts of url, view and template in Django.

5. The student can practically implement a simple web application.

## Performance standard

With the correct understanding the student has gained of the structure of Django, they must be able to implement a simple web application on their own computer.

<!-- page 277 -->

### What is Django?

Django is an open-source framework written in the Python programming language and used to build and implement the backend part of websites and web applications.

*Table 1: Comparing a website and a web application*

| Criterion | Website | Web Application |
| --- | --- | --- |
| Main purpose | Informing and showing content | Doing operations and processing data |
| User interaction | Little or almost one-way | A lot and two-way |
| Need to log in | Usually not | Usually yes |
| Server-side processing | Little | A lot |
| Dependence on the backend | Little or medium | Very much |
| Content change by the user | Usually not | Yes |
| Examples | A news site, a company site, a blog | A user panel, an online shop, an educational system |

### The advantages of Django

Django is a safe and fast framework that gives the programmer many ready-made capabilities. For this reason the speed of software development in Django is very high.

In Django projects, even as the number of users grows, with only a few changes you can still have a fast and safe website.

Another advantage of Django is the existence of comprehensive documentation (guides) and also a big and active community of programmers. This means that if you meet a problem while working with Django, with a simple internet search you can find many solutions and explanations from other programmers. Another important advantage of Django is the many job opportunities in the field of Python and the Django framework, which makes it a good choice for learning and entering the job market. Big companies in the world and in Iran have used Django.

![Figure 1: Companies that have used Django](../images/p283-01.png)
*Figure 1: Companies that have used Django*

<!-- page 278 -->

> **Curiosity**
>
> Research the companies mentioned.

### The final project of this book

At the end of this book, using Django, a real web application showing the weather will be designed (Figure 2).

In this project the user can choose the name of a city to see its weather.

This web application receives the weather information online and shows the result instantly.

The project helps you learn how Django works in practice and how a website is built.

![Figure 2: Parts of the final project](../images/p284-01.png)
*Figure 2: Parts of the final project*

### Installing Django

First make sure the latest version of Python is installed on your computer and the computer is connected to the internet. For this, open the VSCode program; if a file or folder was already open, close it with the Close Folder command from the File menu, then from the terminal menu open a new terminal.

Next, as in Figure 3, run the commands in the terminal part in order.

<!-- page 279 -->

![Figure 3: Installing Django version 5.2.9](../images/p285-01.png)
*Figure 3: Installing Django version 5.2.9*

The message Successfully installed Django-5.2.9 shows that Django was installed successfully.

If you did not see the message of successful Django installation, ask your teacher for guidance.

You can also install the latest published version of Django; you only need to find the compatible Python version on the site `pypi.org` and the Django page.

Go to the address https://pypi.org/project/Django and in the Programming Language section see the Python versions supported by Django (Figure 4).

![Figure 4: Python versions suitable for Django](../images/p285-02.png)
*Figure 4: Python versions suitable for Django*
