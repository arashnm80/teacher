**Page 74**

Example: Build a list of motivational messages and, using the `random` module, print one random message on each run (Figure 152).

Run the program and check the result.

![Figure 152](../images/p080-01.png)

**Figure 152**

### Activity

Write a program that:

Generates a random number between 1 and 10. Asks the user to guess the number. If the guess is correct, prints the message you succeeded; otherwise, asks the user for input again. Also print how many attempts the user made.

### Activity

Write a program that meets the following conditions:

Several predetermined words exist in the program.

On each run of the program, one of the words is chosen at random.

The allowed number of guesses equals the number of letters in the chosen word.

If the user guesses the word correctly: the word is displayed and an appropriate congratulations message is shown.

Otherwise: a game-over message is displayed.

Second method: importing specific parts (`from` ... `import`):

`from` module name `import` function name In this method, only the needed functions or variables from a module are imported. In this method the code is shorter and easier to write.

Example: Only the `sqrt` and `pow` functions from the `math` module are imported into the program (Figure 153).

![Figure 153](../images/p080-02.png)

**Figure 153**


---

**Page 75**

After this statement, you do not need to write `math.sqrt`. You write `sqrt` (25) directly.

Table 5- Commonly used Python modules

Module

### In practice

`math` mathematical functions `random` generating random numbers `turtle` drawing shapes and graphics `datetime` date and time `os` working with the operating system

Example: Displaying the current date and time: In this example only the `now`() function is used (Figure 154).

![Figure 154](../images/p081-01.png)

**Figure 154**

![Book image](../images/p081-03.png)

Example: In this example, only displaying the hour of the current time is needed. Therefore the second method of importing a module is used (Figure 155).

![Figure 155](../images/p081-02.png)

**Figure 155**


---

**Page 76**

### Activity

Using the `datetime` module, write a program that displays the current year.

### Activity

(Word-guessing game), write a module that:

Has a specific word. The allowed number of guesses equals the number of letters in the word.

If the user guesses the word correctly: the word is printed and a congratulations message is displayed.

If the user does not succeed within the allowed number of attempts: a game-over message is displayed.

Use this module in the main program.

Local module (`local`):

These are modules written by the programmer and `import`ed into the program.

First create a Python file with the `py` extension. Then place functions and variables in it. Then you can `import` them in the main program.

Example: Create the file `my_module.py` and write the following code in it (Figure 156).

![Figure 156](../images/p082-01.png)

**Figure 156**

Then in the main program `main.py` write this code (Figure 157).

![Figure 157](../images/p082-02.png)

**Figure 157**

Example: First create a file named `math_module.py` and write the following functions inside it (Figure 158).

![Figure 158](../images/p082-03.png)

**Figure 158**


---

**Page 77**

Then use it in the main program (Figure 159).

![Figure 159](../images/p083-01.png)

**Figure 159**

### Activity

Create a file named `random_module.py` and write the following function inside it:

![Book image](../images/p083-02.png)

`randint` is a ready-made function in Python’s `random` module that is used to generate a random integer in a specific range.

Then in the main program `import` the module you created and use it.

![Book image](../images/p083-03.png)

![Book image](../images/p083-04.png)

Run the program and explain the lines of code.

Third-party modules (`3rd` `party`): Modules that are installed with the `pip` `install` command and are `import`ed into the program. For example `Django` ,`Flask`, `PyGame`, and so on.

### Difference between a function and a method

In earlier material, you used statements such as ,`split`() `append`() and `len`() without a formal definition of them being given.

![Book image](../images/p083-05.png)

This is completely natural and very common in programming; many concepts are first introduced through practical use and then with a precise definition.

**Figure 160**


---

**Page 78**

Function:(`function`) An independent statement used to perform a specific task and not tied to a particular data type.

Example: Counting the number of users: The `len`() function returns the number of characters in a string (Figure 161).

![Figure 161](../images/p084-01.png)

**Figure 161**

Example: Displaying the number of users as a string (Figure 162):

![Book image](../images/p084-02.png)

![Figure 162](../images/p084-03.png)

**Figure 162**

Method (`Method`): A kind of function that belongs to a specific class or object and is used to perform operations on that object’s data.

The main difference between a function and a method is how they are used and what they depend on; functions are called independently, but methods are run through an object or data type using the dot (.) operator and usually have access to that object’s internal data.

The `lower` ,`upper:` methods: Using the `lower` ,`upper` methods, you can convert all of the text to uppercase or lowercase English letters.

### Activity

With guidance from your instructor, explain the lines of code opposite.

![Book image](../images/p084-04.png)

![Book image](../images/p084-05.png)


---

**Page 79**

The `split` method breaks a string into a list of words (Figure 163).

![Figure 163](../images/p085-01.png)

**Figure 163**

### Activity

Write a function that receives a string from input and displays the count of its uppercase letters, lowercase letters, and digits.


---
