<!-- page 254 -->

## Learning unit 2

## Have you ever thought about this

- Why can't variables always be used to keep information?

- What is the difference between "temporarily storing information in memory (RAM)" and "storing in a file"?

- If you run the program several times and write to a file each time, what happens to the earlier content?

- When is a simple text file enough and when is it better to use JSON?

- If the file path is wrong, how should the program behave?

- If you were to design a shop program, what information would need to be stored in a file and why?

## By the end, the student is expected to

1. Use the class "Path" and the module "pathlib" to manage paths (Path Objects).

2. Read the content of text files and write data to them, append, and close the files safely.

3. Read data from several files, combine their content and process a set of files using loops.

4. Recognise common errors such as "FileNotFoundError" and "ZeroDivisionError" and, using "`try/except`", prevent the program from stopping and show suitable error messages.

5. Understand the structure of "JSON" and read data with `json.loads()` and write it to a file with `json.dump()`.

## Performance standard

The student must be able, using the Path object, to safely and exactly create, read, write and manage text and JSON files and to correctly control possible errors and exceptions.

<!-- page 255 -->

## Getting to know files in Python

In this learning unit you get to know working with files and storing data so that your programs become more practical and more stable. You learn how to store and retrieve data and, using exception handling, prevent the program from stopping in unexpected situations.

You will also get to know the json module, which makes it possible to keep the users' information.

Suppose you have written a program for recording the contacts of a mobile phone. If you run the program and enter some contacts, the information is kept in memory as long as the program is open. But if the program is closed, all the information is lost. For the information to be stored permanently and for you to be able to reach it again later, files must be used. Files make it possible to store information on secondary storage (such as a hard disk).

![Figure 18](../images/p261-02.png)
*Figure 18*

### Working with a file

A lot of information is stored in text files; such as students' scores, price lists, weather data, traffic, or the text of a story. For a program to be able to use this information, it must read the file. The first step in using a text file is to bring the file into the program's memory; after that you can read the whole file at once or go through it line by line. Reading a file helps the program analyse, show or change the information.

![Figure 19](../images/p261-01.png)
*Figure 19*

<!-- page 256 -->

### Creating a text file

First make a text file named `mobile_bransd.txt` and write the brands in it (each brand on one line):

### Reading the whole file in Python

To read the whole content of the file, use the pathlib library.

![Figure 20](../images/p262-01.png)
*Figure 20*

**Explanation of the code**:

```
from pathlib import Path
```

- This line brings the class Path in from the pathlib library. Path is a tool for working with the paths of files and folders, and using it is simpler and safer than the ordinary open.

```
path = Path('mobile_brands.txt')
```

Here path is a class that was made for managing the paths of files. By writing:

```
path = Path('mobile_brands.txt')
```

an instance (object) of the class Path is made. This instance knows where the file `mobile_brands.txt` is, but the file itself has not yet been opened or read. In simple words: path only holds the address of the file on the computer.

When you write `path.read_text()`, then the file is opened and read; a Path object has been made that points to the file `mobile_brands.txt`. Since this file is in the same folder as the Python file (.py), only the file name is enough. If the file were in another folder, you would have to give its full or relative path.

```
brnds = path.read_text()
```

- With the method `read_text` the whole content of the file is read. The result is stored as a string in the variable contents. Each line of the file is separated in the string by the character \\n.

<!-- page 257 -->

- The content of brands is printed in the output.

```
print(brands)
```

Example output:

![Figure 21](../images/p263-01.png)
*Figure 21*

**Removing the extra empty line**: sometimes `read_text()` makes an extra empty line at the end of the file. To remove it you can use the method rstrip.

```
brands = brands.rstrip()
```

Now the output is shown clean and without the empty line.

### Relative and absolute paths of files

A relative and an absolute address are like having an exact map for reaching your files. An absolute address guarantees that your program finds exactly the same file on any system; but a relative address helps you write code that, without change, moves into any folder and still finds the files it needs.

When you give the name of a file like `mobile_brands.txt` to Path, Python searches in the folder where the running file (that is, your `.py` program) is. Sometimes, depending on how you organise your work, the file you want to open may not be in the same folder as your program. For example, you might keep your programs in a folder named `py_progs` and inside it a folder named `text_files` to separate the text files from the programs. Even though `text_files` is inside `py_progs`, if you give Path only the name of a file in `text_files`, it does not work; because Python searches only in `py_progs` and stops; it does not look at `text_files`. For Python to be able to open files from a folder other than your program's folder, you need the correct path.

![Figure 22](../images/p263-02.png)
*Figure 22*

<!-- page 258 -->

There are two ways to specify the path of files in programming:

1. **Relative File Path**: this address tells Python to find the wanted place relative to the folder of the running program. Since `text_files` is inside `py_progs`, you must build a path that starts with the folder `text_files` and ends with the file name. The way to build this path is as follows:

```
       path = Path('text_files/filename.txt')
```

2. **Absolute File Path**: in this kind of addressing you can tell Python exactly where on your computer the file is, no matter where the program is running. If the relative address did not work, you can use an absolute address. For example, if you have put `text_files` in a folder other than `py_progs`, giving the address '`text_files/filename.txt`' is not enough; because Python searches for it only inside `python_work`. In this case you must write the absolute address so that it is clear where Python should search. Absolute addresses are usually longer, because they start from the root folder of the operating system:

```
  path = Path('/home/eric/py_progs/text_files/filename.txt')
```

With absolute addresses you can read files from any point of your system. To start, the simplest thing is to keep the files in the same folder as your own program or in a folder such as `text_files` inside the program's folder.

> **Note**
>
> Windows systems use the backslash (\\) instead of the slash (/) when showing file paths, but in your code always use the slash (/), even on Windows. The pathlib library automatically applies the correct display of the path when it interacts with your operating system.

### Working with the content of a file

After reading a text file, its content is given to you in the program as a string.

**Converting the content to a list**: to be able to work on each mobile brand separately, you need to convert the text of the file into a list of lines.

Now each brand is a member of the list and you can work with it.

- `splitlines()` splits the text string into a list of lines.

![Figure 23](../images/p264-01.png)
*Figure 23*

<!-- page 259 -->

![Figure 24](../images/p265-01.png)
*Figure 24*

Counting data: for example the number of brands in the file:

![Figure 25](../images/p265-02.png)
*Figure 25*

> **Activity**
>
> Change the program so that you can see the number of characters of each brand.

### Searching in the content of the file

Checking whether a specific brand exists in the file or not:

![Figure 26](../images/p265-03.png)
*Figure 26*
