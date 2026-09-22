**Page 250**

These statements run without error from Python’s point of view; but logically they are invalid values. A mobile phone’s battery charge cannot be more than 100 percent or a negative value.

The problem is that the class attributes are freely available and there is no control over how they are changed. This can cause logic errors in the program and, in large programs, make maintenance and development difficult.

To solve this problem, you can define some attributes so that direct access to them from outside the class is restricted and changing them is done only through specified methods. These kinds of attributes are called private attributes (`Private`).

Private attributes (`Private`) In Python, private attributes are defined by using two underscores (_ _) at the beginning of their names.

For example, in the `Mobile` class you can define the battery attribute as follows:

```
self._ _battery = 100
```

With this:

Direct access to the attribute from outside the class is restricted.

Changing its value is possible only through the class methods.

Logical control over the data is established.

Protected attributes (`Protected`) In the previous sections you saw that a class’s attributes can be public (`Public`) or private (`Private`).

But sometimes there are situations in which:

You do not want an attribute to be used or changed directly from outside the class.

But you want child classes to be able to access that attribute.

For such a case, protected attributes (`Protected`) are used. In the Python language, if an attribute’s name starts with one underscore (_), that attribute is considered `Protected`.

```
"self._status = "on
```

Table 3

Access level

How to write

Explanation Public (`Public`)`battery`Free access from everywhere `_battery` _Access only inside the same class

```
خصوصی (Private)
```

`_status`Access from inside the class and child classes

Protected (`Protected`)


---

**Page 251**

This kind of naming shows that the attribute is designed for internal use by the class and child classes and should not be changed directly from outside the class.

### Note

`Protected` in Python is a programming convention, not a forced restriction. That is, Python does not prevent direct access, but it warns the programmer that this attribute should not be changed directly from outside the class.

So far you have become familiar with three levels of access to a class’s attributes:

The different access levels, including public, private, and protected attributes, help you control access to a class’s data. For that reason, the internal details of classes need to be hidden and access to data needs to be done in a controlled way. This concept in object-oriented programming is known as encapsulation (`Encapsulation`). Encapsulation means:

Hiding the internal details of a class and controlling how its data and behaviors are accessed, and it is considered one of the main concepts of object-oriented programming.


---
