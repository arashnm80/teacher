<!-- page 52 -->

**Dictionary**: the data type dictionary is like a phone book in which each name is linked to a phone number.

![Figure 104](../images/p058-01.png)
*Figure 104*

- Dictionaries are made of **key: value** pairs (key:value), each of which is called an **item**. Each key points to a particular value.

- To create a dictionary, the items are put inside {} and separated by **commas**. Each key is separated from its value by a **colon**.

In the example in Figure 105, a dictionary named cardic with three items (key and value) is defined:

![Figure 105](../images/p058-02.png)
*Figure 105*

- To get a value from a dictionary, write the key in square brackets \[\] after the dictionary's name (Figure 106).

**Example**: the code in Figure 106 defines a dictionary named person with 3 items (key, value). Square brackets \[\] are used to show each element of this dictionary.

![Figure 106](../images/p058-03.png)
*Figure 106*

<!-- page 53 -->

> **Note**
>
> If each element has its own label (such as a student's name and grade), a dictionary is better than a list, because in a dictionary you can reach a value directly by its key, without knowing the element's index.

> **Activity**
>
> Build a dictionary named book that holds the information of a book:
>
> ```
> "title": "python Basic"
>    author: "Fatemeh"
>           pages: 250
> ```
>
> Print the author's name (author) and the number of pages (pages).

- Different keys can have the same value.

**Example**: the dictionary status has two items (Figure 107).

First item: "`user1":"active`"

Second item: "`user2":"active`". The values are the same, but the keys are different.

- In a dictionary the same key cannot hold two values. A repeated key overwrites the previous value; it does not add a second one.

![Figure 107](../images/p059-01.png)
*Figure 107*

In the example in Figure 108, the dictionary `car_dic` has five items, two of which have the same key name. So the new value replaces the previous one.

![Figure 108](../images/p059-02.png)
*Figure 108*

<!-- page 54 -->

![Figure 109](../images/p060-03.png)
*Figure 109*

- {} is used to create an empty dictionary (Figure 109).

**Example**: an empty dictionary named user is defined.

### Adding a new item to a dictionary

To add a new member to a dictionary in Python, just give a value to a **new key** (Figure 110).

![Figure 110](../images/p060-01.png)
*Figure 110*

> **Activity**
>
> Create a dictionary named product with the keys name and price. Change the price of the product inside the dictionary and then print the dictionary.

**Example**: build an empty dictionary named student. Then add name and grade to it from the input, and finally print the dictionary (Figure 111).

![Figure 111](../images/p060-02.png)
*Figure 111*

> **Activity**
>
> Build an empty dictionary named user. Get values for the keys username, password, and Age from the input, store them in the dictionary, and finally print all the user's information.

<!-- page 55 -->

**Removing an element from a dictionary**: there are several ways to remove an item from a dictionary, including:

![Figure 112](../images/p061-01.png)
*Figure 112*

- In Python, the del statement is used to remove an item from a dictionary. It removes the key and its value completely.

![Figure 113](../images/p061-02.png)
*Figure 113*

**Example**: in this example the key age and its value 20 are removed from the dictionary. Write the program and see the result (Figure 113). The program opposite uses del to remove the item `age": 20"`. You can see that the key and its value are removed.

![Figure 114](../images/p061-03.png)
*Figure 114*

- If you try to remove a key that is not in the dictionary, the program raises an error; so check that the key exists before removing it. The program opposite checks that the element exists before removing it, to avoid the error. Type in the program and see the result (Figure 114).

<!-- page 56 -->

- To **remove an element** from a dictionary you can also use the **`pop()` method**. `pop()` removes the element with the given key. `dictionary.pop(key)`

**Example**: in the code (Figure 115) the element "price " is removed from the product dictionary with `product.pop("price")`.

![Figure 115](../images/p062-02.png)
*Figure 115*

- Besides removing the item, `pop()` can return the value of the removed item (Figure 116).

![Figure 116](../images/p062-01.png)
*Figure 116*

> **Activity**
>
> Build a dictionary named inventory that contains:
>
> ```
>  inventory = {"Bag": 5, "Ball": 8, "Laptop": 3,
>                    "Mouse": 10,  "Flash memory": 14}
> ```
>
> Check whether there is an item named "Bag"; if there is, print a suitable message saying the item exists, then remove it with the `pop()` method.
>
> Print the removed value.
>
> If the item does not exist, show a message saying so.
>
> Then print the new dictionary.
