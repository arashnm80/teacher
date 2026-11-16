<!-- page 60 -->

**Example**: create a tuple with three members to hold the usernames of the company's senior managers, and then print it (Figure 124).

![Figure 124](../images/p066-01.png)
*Figure 124*

**Example**: the program in Figure 125 uses a tuple to hold the names of the days of the week; since the names of the days do not change, this data structure suits these values.

![Figure 125](../images/p066-02.png)
*Figure 125*

### Accessing the elements of a tuple

- Like lists, tuple elements have an index, and an element is reached by its index number.

Example: this program first creates a tuple named `name_ port` to hold the names of a computer's input ports, and then shows its third element. Note that indexes start at zero (Figure 126).

![Figure 126](../images/p066-03.png)
*Figure 126*

- The elements of a tuple are immutable (immutable). That is, if you try to change them after they are set, the program shows an error.

<!-- page 61 -->

**Example**: in the example in Figure 127 the program tries to change the value of the tuple's second element, but running it causes an error.

![Figure 127](../images/p067-02.png)
*Figure 127*

> **Curiosity**
>
> Find out whether you can change the number of elements in a tuple. Write a program that shows what you found.
>
> What do you think is the main advantage of tuples that would make a programmer use them?

**Deleting a tuple**: in Python you cannot remove the elements of a tuple, but you can delete a whole tuple with the del statement.

**Example**: in this program the tuple days is deleted with del. After that, a message says that the tuple days is not defined (Figure 128).

![Figure 128](../images/p067-01.png)
*Figure 128*
