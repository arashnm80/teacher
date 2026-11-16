<!-- page 57 -->

## The Quiz game project

![Figure 117](../images/p063-01.png)
*Figure 117*

In this game a menu of question types is shown first. The user picks the kind of question they like and answers the questions; a correct answer earns one point, otherwise the answer is shown, and when the questions are over the user's score is shown.

**Step 1**: in this step create a menu of question types. To start, put two kinds of questions in the menu. In the menu dictionary each number is assigned to a kind of question. If the number 3 is chosen, the user leaves the game (Figure 118).

![Figure 118](../images/p063-02.png)
*Figure 118*

**Step 2**: write the questions for each kind. Two dictionaries, `math_quiz` for math questions and `geo_quiz` for questions about geographical places, each have three elements made of a question and its answer (Figure 119).

![Figure 119](../images/p063-03.png)
*Figure 119*

<!-- page 58 -->

**Step 3**: in this step write the statements that show the menus.

After the welcome message and the title menu: are shown, for each element of the dictionary the menu number and its text are shown separated by a "-" sign, so that the user can choose one of them (Figure 120).

![Figure 120](../images/p064-01.png)
*Figure 120*

![Figure 121](../images/p064-02.png)
*Figure 121*

**Step 4**: in this step write the statements for choosing from the menu (Figure 121).

<!-- page 59 -->

> **Note**
>
> Wherever \\n is written, the output moves to the next line at that point.

**Step 5**: in this step write the statements that show the points earned. The user's score is shown when option "1" or "2" is chosen (Figure 122).

![Figure 122](../images/p065-01.png)
*Figure 122*

**Step 6**: write the code and run the program!

> **Activity**
>
> Add new Quiz sections (for example Sport, Science).
>
> For a wrong answer, give an explanatory message.
>
> Add the option to choose several sections one after another.

> **Curiosity**
>
> Learn the exact pronunciation of words by looking them up in reference dictionaries.
>
> ```
> https://dictionary.cambridge.org/dictionary/english/tuple
> ```

## Tuples (Tuple)

A tuple in Python is an ordered sequence of data that cannot be changed. With tuples you can store several values of different data types in one variable and work with them. Use this data structure when you want the data not to be changed by accident during the program, by you or by other programmers on your team.

![Figure 123](../images/p065-02.png)
*Figure 123*

### Creating a tuple

```
 tuple_name = (data1, data2, data3,…)
```
