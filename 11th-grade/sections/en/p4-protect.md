<!-- page 250 -->

These statements run without error as far as Python is concerned; but logically they are invalid values. The battery charge of a mobile phone cannot be more than 100 percent or have a negative value.

The problem is that the properties of the class are freely available and there is no control over how they are changed. This can cause logical errors in the program and make its maintenance and development difficult in big programs.

To solve this problem, some properties can be defined in a way that direct access to them from outside the class is limited and changing them is done only through specific methods. This kind of property is called a private property.

### Private properties

In Python, private properties are defined with two underscores (\_ \_) at the start of their name.

For example, in the class Mobile the battery property can be defined as follows:

```
self._ _battery = 100
```

By doing this:

- Direct access to the property from outside the class is limited.

- Changing its value is possible only through the methods of the class.

- Logical control over the data is established.

### Protected properties

In the earlier sections you saw that the properties of a class can be public or private.

But sometimes there are conditions where:

- you do not want a property to be used or changed directly from outside the class.

- but you want the child classes to be able to reach that property.

For such a case protected properties are used. In Python, if the name of a property starts with one underscore (\_), that property is considered Protected.

```
self._status = "on"
```

*Table 3*

| Access level | How to write it | Description |
| --- | --- | --- |
| Public | battery | Free access from everywhere |
| Private | `_ _battery` | Access only inside the same class |
| Protected | `_status` | Access from inside the class and the child classes |

<!-- page 251 -->

This kind of naming shows that the property is designed for the internal use of the class and the child classes and must not be changed directly from outside the class.

> **Note**
>
> Protected in Python is a programming convention, not a compulsory restriction. That is, Python does not stop direct access, but it warns the programmer that this property should not be changed directly from outside the class.

So far you have got to know three access levels for the properties of a class:

The different access levels, including public, private and protected properties, help you control access to the data of a class. For this reason the internal details of classes need to be hidden and access to the data done in a controlled way. This concept is known in object-oriented programming as encapsulation. Encapsulation means:

**hiding the internal details of a class and controlling how its data and behaviours are accessed**, and it counts as one of the main concepts of object-oriented programming.
