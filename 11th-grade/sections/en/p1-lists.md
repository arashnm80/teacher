<!-- page 16 -->

### لیست (list)

![Figure 34](../images/p022-01.png)
*Figure 34*

لیست‌ها یکی از ۴ نوع داده در پایتون هستند که برای ذخیرۀ مجموعه‌ای از داده‌ها در یک متغیر واحد استفاده می‌شوند، ۳ نوع دیگر Set، Tuple و Dictionary هستند که هر کدام کاربردهای متفاوتی دارند.

**Creating a list**: lists are created with square brackets (Square brackets) "\[\]".

در کد مقابل یک لیست شامل رشته‌ای از نام میوه‌ها ایجاد شده است `fruits = ["apple", "banana", "cherry"] .` دستور مقابل یک لیست شامل اعداد 1 و 2 و 3 و 4 و 5 را ذخیره می‌کند. `numbers = [1, 2, 3, 4, 5]`

**Features of lists**: Mixed data: a list can hold different kinds of data. The code below creates a list that stores different data types: numbers, strings, booleans, decimals, and even another list (Figure 35).

![Figure 35](../images/p022-02.png)
*Figure 35*

**Indexed**: list elements have an index (Index); that is, each element has a number, and the first element of the list has index zero (Figure 36).

![Figure 36](../images/p022-03.png)
*Figure 36*

<!-- page 17 -->

You can reach the elements of a list by their index (Figure 37).

![Figure 37](../images/p023-01.png)
*Figure 37*

**Mutable**: a list can be changed; that is, after a list is created, its elements can be edited, removed, or added. In this example, the second element of the list, whose index is \[1\] and whose value is "banana", is changed to "oranges".

![Figure 38](../images/p023-02.png)
*Figure 38*

**Ordered**: lists have a definite order: the elements are stored in the order they are added, and this order does not change unless the programmer changes it.

### What the Ordered feature means

**A. The order of entry is kept**: as you can see in the example, the elements are shown in exactly the order they were entered (Figure 39).

![Figure 39](../images/p023-03.png)
*Figure 39*

**B. Order affects how list elements are shown**: if the order changes, the indexes change too (Figure 40).

![Figure 40](../images/p023-04.png)
*Figure 40*

<!-- page 18 -->

**C. Changing the order of elements**: in this example only the first element changed and the rest stayed in place ← so the order is fixed (Figure 41).

![Figure 41](../images/p024-01.png)
*Figure 41*

**D. Comparing two lists with a different order**: in this example the elements are the same, but because the order is different, the two lists are not equal (Figure 42).

![Figure 42](../images/p024-02.png)
*Figure 42*

> **Activity**
>
> 1. لیستی با ۵ عنصر " headset، book، mouse، phone، book " ایجاد کنید و آن را نمایش دهید. سپس به‌جای عنصر شماره 4 یک عنصر به نام " External HDD " را جایگزین کنید و نتیجه را نمایش دهید.
>
> 2. Create a list of 4 numbers of your choice and then show its first element.
>
> 3. Create a list with 6 elements that stores the names of your favorite cars and the years they were made. Then show the list.

**Adding a new element to a list**: with the **`append()`** method you can add a new element to the end of a list (Figure 43).

![Figure 43](../images/p024-03.png)
*Figure 43*

<!-- page 19 -->

In Python, to add an element after a given element of a list, use the **`insert()`** method. **`list_name. insert (index, value)`**

> **Note**
>
> To hear how this word is pronounced, visit the address below.
>
> ```
> https://dictionary.cambridge.org/dictionary/english/insert
> ```

**Example**: consider the following task list:

```
tasks = ["Study", "Exercise", "Sleep"]
```

Add the task "Break" between "Exercise" and "Sleep". Show the list (Figure 44).

![Figure 44](../images/p025-02.png)
*Figure 44*

> **Activity**
>
> Write a program that, in the fruit list holding 2 kinds of fruit, adds the price of each fruit after its name and shows the list.

![Figure 45](../images/p025-01.png)
*Figure 45*

### Removing an element from a list

Python has several ways to remove elements from a list (list). Which one to use depends on whether you want to remove by value or by position (index).

<!-- page 20 -->

1. **Removing an element by value**: the `remove()` method removes a value from a list. The first element with that value is removed.

```
list_name.remove(value)
```

**Example 1**: this program uses the `remove()` method to remove the value 12 from the scores list (Figure 46).

![Figure 46](../images/p026-01.png)
*Figure 46*

**Example 2**: this program uses the `remove()` method to remove the first 20 from the numbers list (Figure 47).

![Figure 47](../images/p026-02.png)
*Figure 47*

2. **حذف عنصر با ایندکس (index)**: متد `pop()` برای حذف عنصر با ایندکس مشخص شده استفاده می‌شود.

```
list_name.pop(index)
```

Example: in this program the element at index one, that is, the second element of the list, is removed (Figure 48).

> **Note**
>
> Note that the first member of a list has index zero.

![Figure 48](../images/p026-03.png)
*Figure 48*

<!-- page 21 -->

If nothing is written inside the `pop()` method, the last element of the list is removed. In the code below, the food list has three elements (Figure 49).

![Figure 49](../images/p027-02.png)
*Figure 49*

On line 2 nothing is written inside the `pop()` method, so the last element of the list, "kabab", is removed. Running the program confirms this.

> **Activity**
>
> The task list is `tasks = ["Study", "Exercise", "Rest", "Sleep"]`. Write a program that removes the last task from the list.

> **Curiosity**
>
> Find out which element is removed if the number -1 is put inside the pop method. What about other negative numbers?
>
> For example:
>
> ```
> food.pop)-1(
> ```

> **Curiosity**
>
> The `clear()` method and the del statement are also used to remove list elements. Research how they are used and present it in class.

### Conditional structures

![Figure 50](../images/p027-01.png)
*Figure 50*

A conditional structure lets a program make a decision based on whether a condition holds, and change which statements run. In this structure a condition is checked first, and then, if it is true, a set of statements runs.
