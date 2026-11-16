<!-- page 74 -->

**Example**: build a list of motivational messages and use the random module to print a random message on each run (Figure 152).

Run the program and check the result.

![Figure 152](../images/p080-01.png)
*Figure 152*

> **Activity**
>
> Write a program that:
>
> It should generate a random number between 1 and 10. It should ask the user to guess the number. If the guess is right, it should print the message you succeeded; otherwise it should take input from the user again. It should also print the number of the user's attempts.

> **Activity**
>
> Write a program with the following features:
>
> - The program has a few predefined words.
>
> - Each time the program runs, one of the words is chosen at random.
>
> - The number of guesses allowed equals the number of letters in the chosen word.
>
> - If the user guesses the word correctly: show the word and a suitable congratulations message.
>
> - Otherwise: show a game-over message.

### The second way: importing specific parts (from ... import)

**from** module name **import** function name. In this method only the functions or variables needed are imported from a module. The code is shorter and simpler to write.

**Example**: only the sqrt and pow functions are imported from the math module (Figure 153).

![Figure 153](../images/p080-02.png)
*Figure 153*

<!-- page 75 -->

After this statement there is no need to write `math.sqrt`; you write sqrt (25) directly.

*Table 5: Widely used Python modules*

| Module | Use |
| --- | --- |
| math | Math functions |
| random | Random numbers |
| turtle | Drawing and graphics |
| datetime | Date and time |
| os | Working with the operating system |

**Example**: showing the current date and time: in this example only the `now()` function is used (Figure 154).

![Figure 154](../images/p081-02.png)
*Figure 154*

**Example**: in this example only the hour of the current time is needed, so the second way of importing is used (Figure 155).

![Figure 155](../images/p081-01.png)
*Figure 155*

<!-- page 76 -->

> **Activity**
>
> Using the datetime module, write a program that shows **the current year**.

> **Activity**
>
> (Word-guessing game) write a module that:
>
> - has a certain word. The number of guesses allowed equals the number of letters in the word.
>
> - If the user guesses the word correctly: print the word and show a congratulations message.
>
> - If the user does not succeed within the allowed tries: show a game-over message.
>
> - Use this module in the main program.

### The local module

Modules written by the programmer and imported into the program.

First create a Python file with the py extension. Then put functions and variables in it. Then you can use them in the main program with import.

**Example**: create the file `my_module.py` and write the code below in it (Figure 156).

![Figure 156](../images/p082-01.png)
*Figure 156*

Then write this code in the main program `main.py` (Figure 157).

![Figure 157](../images/p082-02.png)
*Figure 157*

**Example**: first build a file named `math_module.py` and write the functions below in it (Figure 158).

![Figure 158](../images/p082-03.png)
*Figure 158*

<!-- page 77 -->

Then use it in the main program (Figure 159).

![Figure 159](../images/p083-01.png)
*Figure 159*

> **Activity**
>
> Build a file named `random_module.py` and write the function below in it:
>
> ![Book image](../images/p083-02.png)
>
> **randint** is a ready-made function in Python's **random** module, used to produce a random integer in a given range.
>
> Then import the module you built into the main program and use it.
>
> ![Book image](../images/p083-03.png)
>
> - Run the program and explain the lines of code.

**Third-party modules**: modules that are installed with the command pip install and imported in the program. Like Django, Flask, PyGame and so on.

## The difference between a function and a method

In the earlier material you used statements such as `split()`, `append()` and `len()` without their formal definition being given. This is completely natural and very common in programming, because many concepts are first introduced through practical use and then with an exact definition.

![Figure 160](../images/p083-04.png)
*Figure 160*

<!-- page 78 -->

**Function:** an independent statement that is used to do one specific job and does not depend on a specific data type.

**Example**: counting users: the `len()` function returns the number of characters in a string (Figure 161).

![Figure 161](../images/p084-01.png)
*Figure 161*

**Example**: showing the number of users as a string (Figure 162):

![Figure 162](../images/p084-02.png)
*Figure 162*

**Method**: a kind of function that belongs to a specific class or object and is used to do operations on the data of that same object.

**The main difference** between a function and a method is how they are **used** and what they **depend on**: functions are **called independently**, but methods run through **an object** or **a data type** **using a dot** (.), and usually **have access to that object's internal data**.

The lower and upper methods: with lower and upper you can turn all the text into lowercase or uppercase English letters.

> **Activity**
>
> With your teacher's guidance, explain the lines of code opposite.
>
> ![Book image](../images/p084-03.png)
>
> ![Book image](../images/p084-04.png)

<!-- page 79 -->

The split method breaks a string into a list of words (Figure 163).

![Figure 163](../images/p085-01.png)
*Figure 163*

> **Activity**
>
> Write a function that gets a string from the input and shows how many uppercase letters, lowercase letters, and digits it has.
