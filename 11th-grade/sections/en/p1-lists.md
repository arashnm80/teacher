**Page 16**

```
لیست (list):
```

![Book image](../images/p022-01.png)

Lists are one of the 4 data types in Python that are used to store a collection of data in a single variable; the other 3 types are `Set`, `Tuple`, and `Dictionary`, each of which has different uses.

Creating a list: Lists are created using

```
کروشه‌ها (Square brackets)"[]" ایجاد
```

.

**Figure 34**

In the code opposite, a list containing a string of fruit names has been created. `fruits` = `["apple"`, `"banana"`, `"cherry"]` The opposite statement stores a list containing the numbers 1, 2, 3, 4, and 5. `numbers` = [1, 2, 3, 4, 5]

List features: `Mixed` `data` A list can hold different kinds of data. In the code below, a list has been created that stores different data types—numeric, string, Boolean, and floating-point, and even another list (Figure 35).

![Figure 35](../images/p022-02.png)

**Figure 35**

`Indexed:` List elements have an index (`Index`); that means each element has a number, and the first element of the list has index zero (Figure 36).

![Figure 36](../images/p022-03.png)

**Figure 36**


---

**Page 17**

With an index you can access the elements of a list (Figure 37).

![Figure 37](../images/p023-01.png)

**Figure 37**

`Mutable:` A list can be changed; that means after creating a list, you can edit, delete, or add elements.

In this example, the second element of the list, whose index is [1] and whose value is `"banana"`, has been changed to `"oranges"`.

![Figure 38](../images/p023-02.png)

**Figure 38**

`Ordered:` Lists have a definite order: list elements are stored in the same order they are entered, and this order does not change unless the programmer changes it.

Factors that affect the `Ordered` feature:

a Preserving the order of entry of elements: As you can see in the example, the elements are displayed exactly in the same order they were entered (Figure 39).

![Book image](../images/p023-03.png)

![Figure 39](../images/p023-04.png)

**Figure 39**

b The effect of order on displaying list elements: If the order changes, the indexes change too (Figure 40).

![Book image](../images/p023-06.png)

![Figure 40](../images/p023-05.png)

**Figure 40**


---

**Page 18**

c Changing the order of elements: In this example only the first element changed; the rest stayed in place ← that means the order is definite (Figure 41).

![Book image](../images/p024-01.png)

![Figure 41](../images/p024-02.png)

**Figure 41**

d Comparing two lists with different order: In this example, although the elements are the same, because the order is different, the two lists are not equal (Figure 42).

![Figure 42](../images/p024-03.png)

**Figure 42**

### Activity

1 Create a list with 5 elements "`headset`, `book`, `mouse`, `phone`, `book`" and display it.

Then replace element number 4 with an element named "`External` `HDD`" and display the result.

2 Create a list with 4 numeric elements of your choice and then display its first element.

3 Create a list that has 6 elements that store the names of your favorite cars and their years of production. Then display this list.

Adding a new element to a list: Using the ()`append` method you can add a new element to the end of the list (Figure 43).

![Book image](../images/p024-05.png)

![Book image](../images/p024-06.png)

![Figure 43](../images/p024-04.png)

**Figure 43**


---

**Page 19**

In Python, to add an element after a specific element in a list, use the ()`insert` method.

```
list_name. insert (index, value)
```

### Note

To hear the correct pronunciation of this word, go to the address below.

```
https://dictionary.cambridge.org/dictionary/english/insert
```

Example: Consider the following list of tasks:

```
]"tasks = ["Study", "Exercise", "Sleep
```

Add the task `"Break"` between `"Exercise"` and `"Sleep"`. Display the list (Figure 44).

![Book image](../images/p025-02.png)

![Figure 44](../images/p025-03.png)

**Figure 44**

### Activity

Write a program that, in the `fruit` list which includes 2 kinds of fruit, adds the price of each fruit after its name and displays it.

![Book image](../images/p025-01.png)

Removing an element from a list:

In Python there are different methods for removing elements from a list (`list`). Choosing the suitable method depends on whether you want to remove based on value or based on position (index).

**Figure 45**


---

**Page 20**

1 Removing an element by value: The ()`remove` method is for removing the value of an element from a list. The first element that has the same value is removed.

```
list_name.remove(value)
```

Example 1: This program has used the ()`remove` method to remove the value 12 from the `scores` list (Figure 46).

![Book image](../images/p026-01.png)

![Figure 46](../images/p026-02.png)

**Figure 46**

Example 2: This program has used the ()`remove` method to remove the first value 20 from the `numbers` list (Figure 47).

![Book image](../images/p026-03.png)

![Figure 47](../images/p026-04.png)

**Figure 47**

2 Removing an element by index (`index`): The ()`pop` method is used to remove an element with a specified index.

```
list_name.pop(index)
```

Example: In this program the index with number one, that is the second element of the list, has been removed (Figure 48).

### Note

Note that the first member of the list has index zero.

![Book image](../images/p026-05.png)

![Figure 48](../images/p026-06.png)

**Figure 48**


---

**Page 21**

If nothing is written inside the ()`pop` method, the last element of the list is removed. In the code below the `food` list has three elements (Figure 49).

![Book image](../images/p027-03.png)

![Figure 49](../images/p027-01.png)

**Figure 49**

On line 2 nothing is written in the ()`pop` method; so the last element of the list, that is `"kabab"`, is removed.

Running the program confirms this.

### Activity

The task list is `tasks` = `["Study"`, `"Exercise"`, `"Rest"`, `"Sleep"]`. Write a program that removes the last task from the list.

### Try this

Research what happens if the number -1 is placed inside the `pop` method—which element is removed? What about other negative numbers?

For example:

```
(1-)food.pop
```

### Try this

The ()`clear` method and the `del` statement are also used for removing list elements. Research how they are used and present them in class.

Conditional structures:

![Book image](../images/p027-02.png)

A conditional structure lets the program make a decision based on whether a condition is true or not, and change the path of running statements.

In this structure, first a condition is checked, and then, if it is true, a set of statements is executed.

**Figure 50**


---
