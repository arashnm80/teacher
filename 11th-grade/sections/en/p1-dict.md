**Page 52**

### Dictionary (dictionary)

The `dictionary` data type is like a phone book in which each name is associated with a phone number.

![Book image](../images/p058-01.png)

Dictionaries are made up of a number of key:

value (`key:value`) pairs, each of which is called an `item`. Each key points to a specific value.

To create a `dictionary`, the items are placed inside {} and separated from each other by commas. Also, each key and its value are separated by a colon.

**Figure 104**

In the example in Figure 105, a `dictionary` named `cardic` containing three items (key and value) is defined:

![Book image](../images/p058-02.png)

![Figure 105](../images/p058-03.png)

**Figure 105**

To access a value in a `dictionary`, after the `dictionary` name, the key is placed inside brackets [] (Figure 106).

Example: In the code in Figure 106, a dictionary named `person` with 3 items (key, value) is defined. Brackets [] are used to display each of the elements inside this dictionary.

![Figure 106](../images/p058-04.png)

**Figure 106**


---

**Page 53**

### Note

If each element has a clear label (such as a student’s name and score), using a dictionary is better than a list, because in a dictionary you can access the matching value directly by the key name and you do not need to know the element’s index.

### Activity

Build a dictionary named `book` that holds information about a book:

```
"title": "python Basic"
"author: "Fatemeh
250:pages
```

Print the author’s name (`author`) and the number of pages (`pages`).

Different keys can have the same values.

Example: The `status` dictionary has two items (Figure 107).

```
آیتم اول: "user1":"active"
```

Second item: `"user2":"active"` The keys are the same, but the values of each of them are different.

In a `dictionary`, identical keys cannot have identical values. Duplicate keys cause the previous value to be overwritten, not duplicate values.

![Book image](../images/p059-01.png)

![Figure 107](../images/p059-02.png)

**Figure 107**

In the example in Figure 108, the `car_dic` dictionary has five items, two of which have keys with the same name. So the new value replaces the previous value.

![Book image](../images/p059-03.png)

![Figure 108](../images/p059-04.png)

**Figure 108**


---

**Page 54**

![Book image](../images/p060-07.png)

To build an empty `dictionary`, {} is used (Figure 109).

Example: An empty dictionary named `user` is defined.

**Figure 109**

Adding a new `item` to a `dictionary:`

To add a new member to a `dictionary` in Python, it is enough to assign a value to a new key (Figure 110).

![Book image](../images/p060-04.png)

![Book image](../images/p060-01.png)

![Book image](../images/p060-03.png)

![Figure 110](../images/p060-02.png)

**Figure 110**

### Activity

Build a `dictionary` named `product` with the keys `name` `price` . Change the product’s price inside the `dictionary` and then print the `dictionary`.

Example: Build an empty `dictionary` named `student`. Then, using input, add `name` and `grade` to the `dictionary` and finally print the dictionary (Figure 111).

![Book image](../images/p060-05.png)

![Figure 111](../images/p060-06.png)

**Figure 111**

### Activity

Build an empty `dictionary` named `user`. Take values for the keys `username` and `password` and `Age` from input, store them inside the `dictionary`, and finally print all of the user’s information.


---

**Page 55**

Removing an element from a `dictionary:`

![Book image](../images/p061-01.png)

There are various ways to remove an item from a `dictionary`, including:

In Python, the `del` statement is used to remove an item from a `dictionary`. With this statement, the key and its related value are completely removed from the `dictionary`.

**Figure 112**

![Book image](../images/p061-02.png)

Example: In the example, the key `age` and its value 20 have been removed from the `dictionary`. Write the program and observe the result (Figure 113).

In the program opposite, the `del` statement is used to remove the item `age":` 20". You can see that with this statement the key and its value have been removed.

![Figure 113](../images/p061-03.png)

**Figure 113**

![Book image](../images/p061-04.png)

If you intend to remove a key that does not exist in the `dictionary`, the program encounters an error; therefore, before removing, the existence of the key must be checked. In the program opposite, to prevent an error, the existence of the element is checked before removing it from the list.

Enter the program and observe the result (Figure 114).

**Figure 114**


---

**Page 56**

To remove an element from a `dictionary`, you can also use the `pop`() method. The `pop`() method removes the element that has the specified key name. (`key`)`dictionary.pop` Example: In the code (Figure 115), the element `"price` " has been removed from the `product` dictionary using the statement `product.pop`(`"price"`).

![Book image](../images/p062-03.png)

![Figure 115](../images/p062-04.png)

**Figure 115**

In addition to removing the item, the ()`pop` method can also return the value of the removed item (Figure 116).

![Book image](../images/p062-01.png)

![Figure 116](../images/p062-02.png)

**Figure 116**

### Activity

Build a dictionary named `inventory` that includes:

```
,inventory = {"Bag": 5, "Ball": 8, "Laptop": 3
}Mouse": 10,  "Flash memory": 14"
```

Check whether an item named `"Bag"` exists and, if it does, print a suitable message indicating that the item exists, and then remove that item with the ()`pop` method.

Print the removed value.

If the item did not exist, display a message stating that it does not exist.

Then print the new `dictionary`.


---
