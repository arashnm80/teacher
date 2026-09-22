**Page 60**

Example: Create a `tuple` with three members to hold the usernames of the company’s senior managers and then print it (Figure 124).

![Book image](../images/p066-01.png)

![Figure 124](../images/p066-02.png)

**Figure 124**

Example: In the program in Figure 125, a tuple is used to hold the names of the days of the week, because the names of the days of the week are not changeable, so this type of data structure is suitable for holding these values.

![Book image](../images/p066-03.png)

![Figure 125](../images/p066-04.png)

**Figure 125**

Accessing `Tuple` elements:

Like lists, tuple elements also have an `index`, and access to an element is done with its index number.

Example: In this program, first a tuple named `port_name` is created to hold the names of the input ports of a computer system, and then its third element is displayed. Note that the index of elements starts from zero (Figure 126).

![Figure 126](../images/p066-05.png)

**Figure 126**

The elements of a tuple are unchangeable (`immutable`). That is, if you want to change them after the initial assignment, the program displays an error message.


---

**Page 61**

Example: In the example in Figure 127, an attempt has been made to change the value of the second element of the tuple, but running the program encounters an error.

![Figure 127](../images/p067-03.png)

**Figure 127**

### Try this

Research whether you can change the number of elements of a tuple or not. Write a program that shows the result of your research.

In your opinion, what is the main advantage of tuples that requires the programmer to use them?

Deleting a `Tuple:` In Python it is not possible to delete the elements of a tuple. But you can delete an entire tuple using the `del` statement.

Example: In this program, the `days` tuple is deleted with the `del` statement. After running it, a message is also displayed stating that the `days` tuple is not defined (Figure 128).

![Book image](../images/p067-01.png)

![Figure 128](../images/p067-02.png)

**Figure 128**


---
