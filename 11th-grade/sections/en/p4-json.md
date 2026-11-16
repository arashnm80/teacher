<!-- page 267 -->

Now if you create the file `alice.txt` and put it in the suitable folder, this time the try block will run.

- The program finds the file and enters the else block.

- Import the text of Alice in Wonderland; Python treats the text of the file as one long string.

- To produce a list of all the words in the book, use the string method that by default splits a string wherever it finds white space.

- To count the number of these words use `len()`.

![Book image](../images/p273-01.png)

![Figure 45](../images/p273-02.png)
*Figure 45*

<!-- page 268 -->

### Working with several files

Working with several files is an important skill, because almost no real program works with only one file. Working with several files means the program can, without repeating code:

read several files one after another and do a similar operation on all of them. So you need to define a function, and also the errors must be managed and then the results saved.

To do this, add more books for analysis.

To make running the analysis on several different books simpler and more orderly, it is better to move the main part of the program to a function named `count_word`. If you compare the code with the previous program, you notice that the changes consist of fixing the indentation and moving to the body of the function.

**Line 2**: the function `def count_words(path)` takes one input named path, which is the path of a text file.

**Line 11**: this line of code stores the names of the files as strings in a list named filenames.

```
filenames = ['alice.txt','moby_dick.txt','little_women.txt']
```

**Line 12**: in this line a for loop is used to check each file in the list one by one and get the number of words of the text of the file.

**Line 13**: the file name is turned into an object of the Path type.

**Line 14**: the function `count_words` runs for that file.

And if a file does not exist, the program gives no error and shows a suitable message.

![Figure 46](../images/p274-01.png)
*Figure 46*

<!-- page 269 -->

### Ignoring errors (Failing Silently)

![Figure 47](../images/p275-01.png)
*Figure 47*

In the previous example, the user was told that one of the files was not available. However, in all programs there is no need to show every error that happened to the user.

In this case the error happens, but no message is shown to the user and the running of the program continues without a pause. To implement this, the try-except structure is used. The difference is that in the except part the Python interpreter is explicitly told to do nothing. So remove the print statement after except so that the error message is not shown, and add the statement pass in its place.

In the Python programming language, the statement pass is used to keep a block of code empty and do nothing. If the file does not exist, the error happens, but no message is shown, the program does not stop and its running continues.

![Figure 48](../images/p275-02.png)
*Figure 48*

> **Activity**
>
> As you saw in the program dividing a number by zero, the user was informed of the divide-by-zero error with an error message. Change this program so that whenever the denominator of a division is zero, the program does not stop and no message is shown either.

### Storing data

In most programs, such as the user's chosen settings for a game or data for showing a chart, information is received from users. Whatever its type, the entered information is stored in data structures such as lists and dictionaries. But when the program is closed, this data is lost. To keep the information for the next runs of the programs, you can save it in a file. One of the simplest ways to do this is to use JSON files, which help Python data be stored as text and read again in the next run of the program. This format is not specific to Python and is used in other programming languages too. In Python the module json is used to work with JSON.

![Figure 49](../images/p275-03.png)
*Figure 49*

<!-- page 270 -->

`json.dump()` turns the data into JSON format and `json.loads()` turns the stored data back into Python structures.

Because of their simplicity, readability and wide use, JSON files are one of the important ways of storing data in programming.

### Saving a list in a JSON file

**Explanation of the code**:

**Line 2** - the json module is imported into the program.

**Line 3** - a list of mobile phone brands is created for storing.

**Line 5** - using the function dump, the wanted data is turned into JSON format. The output of this function is a text string that represents the data as json

![Figure 50](../images/p276-01.png)
*Figure 50*

**Line 6** - this text string is saved inside the file using the method write-text.

This program has no output on the screen, but if you open the file `mobiles_brand.json` you will see that the data is stored in a form very similar to the structure of data in Python.

![Figure 51](../images/p276-02.png)
*Figure 51*

**Reading data from a JSON file**

To bring the information stored in the JSON file back into memory, another program must be written.

![Figure 52](../images/p276-03.png)
*Figure 52*

<!-- page 271 -->

**Explanation of the code**:

**Line 2** - first the json module is imported into the program.

**Line 3** - then the content of the JSON file is read and stored as a text string.

**Line 4** - since a JSON file is in essence a text file with a specific format, it is read using the method `read_text()`.

**Line 5** - in the next step, using the function loads, this text string is turned into a suitable data structure in Python. In this program, the data is stored again in memory as a list of numbers.

After this step, you can use the data like other Python lists. In this way, the information that was stored earlier in the JSON file can be used again in the next run of the program.

**Example**: write a program that defines the technical specifications of a smartphone (including the brand, model, amount of RAM and warranty status) in the form of a dictionary. Then this program must:

Using the json library and the class Path from the pathlib library, save this dictionary in a file named `mobile_specs.json`.

In the next step, open the file, read the content and print only the "model" and the "amount of RAM" of the phone in the output.

> **Activity**
>
> Explain the lines of the program's code with the help of your respected teacher.
>
> ![Book image](../images/p277-01.png)
>
> ![Book image](../images/p277-02.png)

<!-- page 272 -->

> **Activity**
>
> In the written code, the weather information of a city is to be saved in a file and then read back. Fill in the parts of the code marked with the sign \_\_\_\_\_\_\_\_\_ with the correct statements.
>
> ![Book image](../images/p278-01.png)
