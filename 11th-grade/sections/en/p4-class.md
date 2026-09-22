**Page 238**

Now it is time, in the programming environment, to create your first class (`class`) and then use that class to build an instance (`Instance`). Carefully type the code of Figure 4 into a new file.

![Figure 4 First code for defining a class and creating an instance](../images/p244-01.png)

Figure 4 First code for defining a class and creating an instance

Line 1: A class named `Mobile` is defined.

A class is in fact a pattern or blueprint for building mobiles.

Note that a class is not itself a mobile; rather, it is a pattern for building mobiles.

Based on Python naming standards (`PEP8`), class names should be written using the `PascalCase` style; that is, the first letter of the class name and the first letter of every word that forms it should be uppercase.

Line 2: This method plays the role of the class constructor method in Python. This method is also called an `initializer`.

Whenever an instance is created from the `Mobile` class—that is, when line 7 runs—this method runs automatically.

The main job of this method is to initialize the instance (`Instance`) attributes.

Note that `__init__` is a conventional name in Python and cannot be changed. On the left and right of the word `init`, the underscore (`underscore`) character is typed twice.

Lines 3 and 4: These specify the instance attributes.

Every mobile has a brand and a color.

In the given code, `self.brand` and `self.color` are both recognized as attributes (`attribute`).

The word `self` refers to the same instance that is being created, and `brand` and `color` are the names of attributes that belong to that instance.


---

**Page 239**

Lines 5 and 6: Blank lines According to Python coding standards (`PEP8`), after the end of a class definition, two blank lines should be placed so that the boundary between the class and the global (`Global`) code section is clearly marked.

Line 7: Creating an instance (`Instance`) On this line, you have created an instance (`instance`) named `my_mobile` from the `Mobile` class.

The value `"nokia"` is assigned for the `brand` attribute and the value `"gray"` for the `color` attribute.

![Book illustration](../images/p245-01.png)

Line 8: Accessing an attribute Using the instance name and the dot (.) symbol, you access its attributes.

This statement prints the value of the `brand` attribute for the `my_mobile` instance.

**Figure 5**

Line 9: Blank line According to `PEP8` standards, after the end of the code a blank line is also placed so that the end of the file is marked in a readable and standard way relative to the code.

Keep in mind that if you do not fully understand every detail at this stage, do not worry; this is a new topic, and with continued instruction and more activities, reviewing the code, and building more programs, the concepts will gradually become clear and settle in for you.

Now run the program; you will see that the value of the `brand` attribute of the mobile you created, namely `nokia`, is printed.

Note that at this stage the class includes only attributes (`Attributes`), and so far no behavior or method (`Method`) other than the constructor (`__init__`) has been defined for the instances.

Now the program’s execution flow is explained with a diagram. Observe Figure 6 carefully.

![Figure 6 Program execution flow](../images/p245-02.png)

Figure 6 Program execution flow


---

**Page 240**

As you see in the figure, after line 7 runs to create the `my_mobile` instance, the following steps occur:

1 The arguments `"nokia"` and `"gray"` are sent to the `__init__` method and placed in the `brand` and `color` parameters.

2 The value of the `brand` parameter is assigned to `self.brand` and the value of the `color` parameter to `self.color`.

3 At this stage the desired instance will be created.

### Activity

At the end of the program, add a statement that prints the mobile’s color.

### Activity

Inside the `__init__` method, add a statement that also treats your phone’s model as an attribute.

Do not forget that on line 7 you must also add your phone’s model. Try to do this activity yourself, but if you still have questions, later you will see the answer to this code and can compare it with your own code.

Next, based on the class you defined, create another instance as a mobile for your friend. Carefully write the code of Figure 7.

![Figure 7 Creating an instance as a phone for your friend](../images/p246-01.png)

Figure 7 Creating an instance as a phone for your friend


---

**Page 241**

Line 4: A new attribute for the mobile phone’s model has been defined and assigned a value.

Line 9: A new instance named `friend_mobile` has been created with attributes different from `my_mobile`.

![Figure 8](../images/p247-01.png)

**Figure 8**

Lines 15 to 17: On these lines the attributes of the second instance have been printed.

### Note

Note that `my_mobile` and `friend_mobile` are both separate instances created from the `Mobile` class.

Next, add a method to the `Mobile` class that prints the values of all attributes of the instance you have created. Change the previous code as in Figure 9.

![Figure 9 Adding a method](../images/p247-02.png)

Figure 9 Adding a method

```
show_info
```


---

**Page 242**

Line 7: This line defines a method (`method`) named `show_info` inside the `Mobile` class.

Methods are functions that are associated with a class and can access that class’s attributes (`Attributes`).

The `self` parameter in the method definition refers to the instance on which the method is called. In other words, `self` allows the `Mobile` class to access the specific attributes (`Attributes`) of each instance of type `Mobile`.

Lines 8 to 10: This statement displays the values of the instance’s brand, model, and color attributes using specified labels.

Line 14: On this line the `show_info` method is called and run on the `my_mobile` instance.

In the same way, you can define more methods for this class. For example, the `incoming_call` method is for displaying a message on an incoming call. Write the code for this method below the `show_info` method according to Figure 10.

![Figure 10 Adding a method](../images/p248-01.png)

Figure 10 Adding a method

```
incoming_call
```

The first line defines a method named `incoming_call` inside the `Mobile` class. This method receives a parameter named `phone_number` that represents the caller’s phone number.

The statements inside the method display the message "incoming call" and the caller’s phone number in the output.

Note that this method must be defined inside the `Mobile` class and at the same level as the `__init__` method, so it is placed one `tab` further in than the class body.

On the last line of the program, the `incoming_call` method is called on the `my_mobile` instance.

The argument "0912-345-6789" is sent as the `phone_number` parameter, which represents the caller’s phone number. Then the method runs and displays the specified messages and the provided phone number.


---

**Page 243**

### Activity

In the `Mobile` class, create a method named `make_call`. This method should receive a parameter named `phone_number` that holds the phone number you want to call. The method should announce the start of the dialing operation by printing appropriate messages. For example, you can print messages such as

```
"...Calling" یا "...Dialing" را چاپ کنید.
```

Setting default values for attributes For greater appeal and usefulness, next an attribute will be defined whose value can be changed after the program runs. Therefore, inside the class, an on/off status attribute (`status`) and a default value for it will also be defined. It is enough to define a new attribute in the `__init__` method as in the code below.

```
"self.status = "on
```

Note that when defining an instance, it is no longer necessary to provide a value for this attribute.

Changing an attribute value: In this approach, after creating the `my_mobile` instance, you can simply change its value by writing the code below.

```
my_mobile = Mobile("nokia", "1100", "gray")
" my_mobile.status = "off
```

In this statement, the `dot` symbol, or period, is used to access an instance attribute. This line asks Python to find the `status` attribute associated with the `my_mobile` instance and then place the value "`off"` into it.

```
ارث‌بری (Inheritance)
```

Suppose that in a mobile phone manufacturing company, until now only basic versions of mobile phones have been produced—phones whose capabilities have been limited to attributes such as brand, model, color, and status, and that lack an operating system and a camera. The most important things you can do with these mobile phones are make phone calls and send text messages. In this company, there is a main class named `Mobile` that models these basic attributes.

Now the company has decided to design a new generation of mobile phones: smart phones (`Smartphone`) that, alongside the basic attributes of a mobile phone, offer capabilities such as an operating system and a camera, and also more specialized models, such as phones suitable for gaming (`Gaming` `phone`), designed with stronger hardware features for better game performance.

1 `Smartphone:` A smart phone is a type of mobile phone that, by using an operating system (`Operating` `System`), makes it possible to run apps and provide advanced capabilities beyond calling and texting.

Has an advanced camera attribute Has an installable and upgradable operating system attribute


---
