**Page 267**

Now if you create the file `alice.txt` and place it in the appropriate folder, this time the `try` block will run.

The program finds the file and enters the `else` block.

Enter the text of Alice in Wonderland; Python treats the file text as one long string.

To produce a list of all the words in the book, use the string method that by default splits a string wherever it finds a space.

To count the number of these words, use `len`().

![Book image](../images/p273-02.png)

![Book image](../images/p273-01.png)

![Figure 45](../images/p273-03.png)

**Figure 45**


---

**Page 268**

Working with several files Working with several files is an important skill, because almost no real program works with only one file.

Working with several files means the program can, without repeating code:

read several files one after another and perform a similar operation on all of them. So you need to define a function, and errors must also be managed and then the results stored.

To do this, add more books for analysis.

To make running the analysis on several different books simpler and more organized, it is better to move the main part of the program into a function named `count_word`. If you compare the code with the previous program, you notice that the changes include fixing indentation and moving it into the body of the function.

Line 2: The function `def` `count_words`(`path`) takes one input named `path`, which is the path of a text file.

Line 11: This line of code stores the file names as text strings (`String`) in a list named `filenames`.

```
]'filenames = ['alice.txt','moby_dick.txt','little_women.txt
```

Line 12: In this line a `for` loop is used to examine each file in the list one by one and obtain the number of words in the file text.

Line 13: The file name is turned into an object of type `Path`.

Line 14: The `count_words` function is run for that file.

And if a file does not exist, the program does not give an error and displays an appropriate message.

![Book image](../images/p274-01.png)

![Figure 46](../images/p274-02.png)

**Figure 46**


---

**Page 269**

Ignoring errors (Failing Silently) In the previous example, the user was told that one of the files was not available. Even so, not every program needs to display every error that occurs to the user.

![Book image](../images/p275-01.png)

In this case, an error occurs, but no message is displayed to the user and the program continues running without interruption.

To implement this case, a `try-except` structure is used. The difference is that in the `except` section the Python interpreter is explicitly told to do nothing. So remove the `print` statement after `except` so that the error message is not displayed, and instead add the `pass` statement.

**Figure 47**

In the Python programming language, the `pass` statement is used to leave a block of code empty and perform no action.

![Book image](../images/p275-02.png)

![Book image](../images/p275-03.png)

If the file does not exist, an error occurs, but no message is displayed, the program does not stop, and execution of the program continues.

**Figure 48**

### Activity

As you saw in the division-by-zero program, an error message informed the user of the division-by-zero error. Change this program so that whenever the denominator of a division is zero, without stopping the program, no message is displayed either.

Storing data In most programs, such as a user’s preferred settings for a game or data for displaying a chart, information is received from users. Regardless of their type, the entered information is stored in data structures such as lists and dictionaries. But when the program is closed, this data is lost. To keep the information for later runs of the programs, you can store it in a file. One of the simplest methods for this is to use `JSON` files, which help store Python data as text and read it again in the next run of the program. This format is not specific to Python and is also used in other programming languages. In Python, the `json` module is used to work with `JSON`.

![Figure 49](../images/p275-04.png)

**Figure 49**


---

**Page 270**

`json.dump`() converts data to the `JSON` format, and `json.loads`() turns the stored data back into Python structures.

`JSON` files, because of their simplicity, readability, and wide use, are one of the important methods of storing data in programming.

Storing a list in a `JSON` file Code explanation:

Line 2 The `json` module has been imported into the program.

Line 3 A list of mobile phone brands has been created for storage.

Line 5 Using the `dump` function, the desired data has been converted to the `JSON` format. The output of this function is a text string that represents the data as `json`

![Figure 50](../images/p276-01.png)

**Figure 50**

Line 6 This text string is stored inside the file using the `write-text` method.

This program has no output on the display, but if you open the file `mobiles_brand.json` you will see that the data has been stored in a form that is very similar to the structure of data in Python.

![Figure 51](../images/p276-02.png)

**Figure 51**

Reading data from a `JSON` file To bring the information stored in a `JSON` file back into memory, another program must be written.

![Book image](../images/p276-03.png)

![Figure 52](../images/p276-04.png)

**Figure 52**


---

**Page 271**

Code explanation:

Line 2 First the `json` module has been imported into the program.

Line 3 Then the contents of the `JSON` file have been read and stored as a text string.

Line 4 Since a `JSON` file is essentially a text file with a specific format, it has been read using the `read_text`() method.

Line 5 Next, using the `loads` function, this text string has been converted to an appropriate data structure in Python. In this program, the data is stored in memory again as a list of numbers.

After this step, you can use the data like other Python lists. In this way, information that was previously stored in a `JSON` file will be usable again in the next run of the program.

Example: Write a program that defines the technical specifications of a smartphone (including brand, model, amount of RAM, and warranty status) in the form of a dictionary. Then this program must:

using the `json` library and the `Path` class from the `pathlib` library, store this dictionary in a file named

```
mobile_specs.json ذخیره کند.
```

Next, open the file, read the content, and print only the “model” and “amount of RAM” of the phone in the output.

### Activity

Explain the lines of the program code with the help of your teacher.

![Book image](../images/p277-01.png)

![Book image](../images/p277-02.png)


---

**Page 272**

### Activity

In the written code, the weather information of a city is to be stored in a file and then read back.

Fill in the parts of the code marked with _________ with the correct statements.

![Book image](../images/p278-01.png)


---
