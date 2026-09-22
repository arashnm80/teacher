**Page 57**

### Quiz game project

![Book image](../images/p063-01.png)

In this game, a menu that includes types of questions is displayed first, and the user chooses their preferred question type and then answers the questions. If the answer is correct, they receive one point; otherwise a reply message is shown, and when the questions are finished, the user’s score is displayed.

**Figure 117**

Step 1: In this step you must create a menu that includes types of questions. To start, put two types of questions in the menu. In the `menu` dictionary, each number is assigned a type of question. If the number 3 is chosen, the user exits the game (Figure 118).

![Figure 118](../images/p063-02.png)

**Figure 118**

Step 2: Write the questions related to each question type. Two dictionaries, `math_quiz` for math questions and `geo_quiz` for questions about geographic places, each with three elements that include a question and its answer (Figure 119).

![Figure 119](../images/p063-03.png)

**Figure 119**


---

**Page 58**

Step 3: In this step write statements that display the menus.

After displaying the welcome message and displaying the title `:menu`, for each of the elements inside the dictionary, the `menu` number and its text are separated by a "-" and displayed so that the user can choose one of them (Figure 120).

![Figure 120](../images/p064-01.png)

**Figure 120**

![Book image](../images/p064-02.png)

Step 4: In this step write the statements related to menu selection (Figure 121).

**Figure 121**


---

**Page 59**

### Note

Wherever `\n` is written, the output goes to the next line from that point.

Step 5: In this step write statements that display the points earned. The user’s score is displayed if option "1" or "2" is chosen (Figure 122).

![Figure 122](../images/p065-01.png)

**Figure 122**

Step 6: Write the code and run the program!

### Activity

Add new `Quiz` sections (for example `Sport` ,`Science`).

For a wrong answer, give an explanatory message.

Add the ability to choose several sections one after another.

### Try this

By referring to reference dictionaries, learn the exact pronunciation of words.

```
https://dictionary.cambridge.org/dictionary/english/tuple
```

### Tuple (Tuple)

A tuple in Python is a sequence of ordered, unchangeable data. With tuples you can store several values of different data types in one variable and perform operations on them. Use this data structure when you want the data not to be changed accidentally during the program by you or by other programmers on your team.

![Figure 123](../images/p065-02.png)

**Figure 123**

Creating a `Tuple:`

```
tuple_name = (data1, data2, data3,…)
```


---
