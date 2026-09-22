# Object-oriented program development


---

**Page 254**

## Learning unit 2

## Object-oriented program development

### Have you ever thought

Why can you not always use variables to store information?

What is the difference between “temporary storage of information in memory (`RAM`)” and “storage in a file”?

If you run the program several times and write to the file each time, what happens to the previous content?

When is using a simple text file enough, and when is it better to use `JSON`?

If the file path is wrong, how should the program behave?

If you are going to design a store program, what information should be stored in a file, and why?

### By the end, the student is expected to

1 Use the `"Path"` class and the `"pathlib"` module to manage paths (`Path` `Objects`).

2 Read the contents of text files and write data to them, append data, and close files safely.

3 Read data from several files, combine their contents, and process a set of files using loops.

4 Recognize common errors such as `"FileNotFoundError"` and `"ZeroDivisionError"` and, using `"try/except"`, prevent the program from stopping and display appropriate error messages.

5 Understand the `"JSON"` structure and read data using `json.loads`() and write it to a file with `json.dump`().

### Performance standard

The student should be able to use a `Path` object to create, read, write, and manage text and `JSON` files safely and accurately, and to handle possible errors and exceptions correctly.


---

**Page 255**

### Getting to know files in Python

In this learning unit you get to know working with files and storing data so that your programs become more useful and more reliable. You learn how to store and retrieve data and how, by managing exceptions, you can keep the program from stopping in unexpected situations.

You will also get to know the `json` module, which makes it possible to keep user information.

Suppose you have written a program to record the contacts of a mobile phone. If you run the program and enter a few contacts, the information is kept in memory as long as the program is open. But if the program is closed, all the information is lost.

![Book image](../images/p261-02.png)

For the information to be stored permanently so you can access it again later, you need to use files.

Files make it possible to store information on secondary storage (such as a hard disk).

**Figure 18**

Working with files A great deal of information is stored in text files; for example, students’ grades, price lists, weather data, traffic, or the text of a story. For a program to be able to use this information, it must read the file. The first step in using a text file is to bring the file into the program’s memory; after that you can read the whole file at once or examine it line by line. Reading a file helps the program analyze, display, or change the information.

![Figure 19](../images/p261-01.png)

**Figure 19**


---

**Page 256**

Creating a text file First create a text file named `mobile_bransd.txt` and write the brands in it (each brand on one line):

Reading the whole file In Python, use the `pathlib` library to read the entire contents of a file.

![Book image](../images/p262-01.png)

![Figure 20](../images/p262-02.png)

**Figure 20**

Code explanation:

```
from pathlib import Path
```

This line imports the `Path` class from the `pathlib` library. `Path` is a tool for working with the paths of files and folders, and using it is simpler and safer than ordinary `open`.

```
path = Path('mobile_brands.txt')
```

Here `path` is a class built for managing file paths. By writing:

```
path = Path('mobile_brands.txt')
```

an instance (`object`) of the `Path` class is created. This instance knows where the file `mobile_brands.txt` is, but the file itself has not yet been opened or read. In simple terms: `path` only holds the address of the file on the computer.

When you write `path.read_text`(), then the file is opened and read; a `Path` `object` has been created that points to the file `mobile_brands.txt`. Because this file is in the same folder as the Python file (`.py`), only the file name is enough. If the file were in another folder, you would have to give its full or relative path.

```
brnds = path.read_text()
```

With the `read_text` method, the entire contents of the file are read. The result is stored as a string (`string`) in the variable `contents`. Each line of the file in the string is separated by the character `\n`.


---

**Page 257**

The contents of `brands` are printed in the output.

```
print(brands)
```

Example output:

![Figure 21](../images/p263-01.png)

**Figure 21**

Removing an extra blank line: Sometimes `read_text`() creates an extra blank line at the end of the file. To remove it you can use the `rstrip` method.

```
brands = brands.rstrip()
```

Now the output is displayed clean and without a blank line.

Relative and absolute file paths Relative and absolute addresses are like having an accurate map for reaching your files. An absolute address guarantees that your program finds exactly the same file on any system; but a relative address helps you write code that can be moved to any folder without change and still find the files it needs.

When you give a file name such as `mobile_brands.txt` to `Path`, Python searches in the folder where the file that is running (that is, your `.py` program) is located. Sometimes, depending on how you organize your work, the file you want to open may not be in the same folder as your program. For example, you might keep your programs in a folder named `py_progs` and inside it a folder named `text_files` to keep text files separate from the programs. Although `text_files` is inside `py_progs`, if you give only the name of a file in `text_files` to `Path`, it does not work; because Python searches only in `py_progs` and stops; it does not look into `text_files`. For Python to be able to open files from a folder other than your program folder, you need the correct path.

![Figure 22](../images/p263-02.png)

**Figure 22**


---

**Page 258**

There are two ways to specify file paths in programming:

1 Relative address (`Relative` `File` `Path`): This address tells Python to find the desired location relative to the folder of the program that is running. Since `text_files` is inside `py_progs`, you must build a path that starts with the `text_files` folder and ends with the file name. You build this path like this:

```
path = Path('text_files/filename.txt')
```

2 Absolute address (`Absolute` `File` `Path`): In this kind of addressing you can tell Python exactly where the file is on your computer, regardless of where the program that is running is. If a relative address does not work, you can use an absolute address. For example, if you have placed `text_files` in a folder other than `py_progs`, giving the address `'text_files/filename.txt'` is not enough; because Python searches for it only inside `python_work`. In this case, you must write the absolute address so that it is clear where Python should search. Absolute addresses are usually longer, because they start from the root folder of the operating system:

```
path = Path('/home/eric/py_progs/text_files/filename.txt')
```

Using absolute addresses, you can read files from any point on your system. To start, the simplest thing is to keep the files in the same folder as your program, or in a folder such as `text_files` inside the program folder.

### Note

Windows systems use a backslash (\) instead of a slash (/) when displaying file paths, but you should always use a slash (/) in your code, even on Windows. The `pathlib` library automatically uses the correct path display when interacting with your operating system.

Working with file contents After reading a text file, its contents are available to the program as a string (`string`).

Converting the content to a list: So that you can work with each mobile phone brand separately, you need to turn the file text into a list of lines.

Now each brand is one member of the list and you can work with it.

`splitlines`() splits the text string into a list of lines.

![Book image](../images/p264-01.png)

![Figure 23](../images/p264-02.png)

**Figure 23**


---

**Page 259**

![Book image](../images/p265-01.png)

![Figure 24](../images/p265-02.png)

**Figure 24**

Counting data: for example, the number of brands in the file:

![Book image](../images/p265-03.png)

![Figure 25](../images/p265-04.png)

**Figure 25**

### Activity

Change the program so that you can see the number of characters in each brand.

Searching in the file contents Checking whether a particular brand exists in the file or not:

![Book image](../images/p265-05.png)

![Figure 26](../images/p265-06.png)

**Figure 26**


---
