**Page 244**

2 `Gaming` `phone:` A type of smart phone that, in addition to having all the capabilities of a `Smartphone`, is specially designed for running games and has stronger hardware features.

Has a strong, separate graphics processor attribute Has a high graphics memory attribute

![Book illustration](../images/p250-01.png)

![Book illustration](../images/p250-03.png)

![Figure 11 Basic mobile, smart phone, and gaming mobile](../images/p250-02.png)

Figure 11 Basic mobile, smart phone, and gaming mobile

Following this decision, the company’s programmers have been asked to write and define the necessary classes for specialized mobiles.

Table 2

Processor

Brand

Model

Color Status

CameraOperating system1

Memory

Graphics

```
Mobile
```

















```
Smartphone
```

















```
GamingPhone
```

















As you see in the table, all phones have common attributes: brand, model, color, and status. Therefore, redefining these attributes in each of the specialized phone classes would lead to code repetition.

To avoid code repetition and make better use of the phones’ shared attributes, you can use the concept of inheritance (`Inheritance`) in object-oriented programming.

Inheritance means that a new class can inherit the attributes (`Attributes`) and behavior (`Method`) of another class and use them.

In this approach, first a more general class is defined that includes the attributes common to all phones, such as brand, model, color, and status. This type of class is called a parent class (`Parent` `class` or `Super` `class`).

In this example, the `Mobile` class, as the parent class, includes all attributes common to all mobiles.

```
1- Operating System
```


---

**Page 245**

![Book illustration](../images/p251-01.png)

Then more specialized classes are created based on the base class. These classes are called child classes (`Child` `class`). For example, the `Smartphone` class, which inherits from the `Mobile` class, automatically has all attributes of the `Mobile` class and can, in addition, define its own specialized attributes and behaviors such as operating system and camera.

Using this approach has the following results:

Reduced amount of coding Increased code readability Improved program maintainability

**Figure 12**

Next, a new class named `SmartPhone` is defined that inherits from the `Mobile` class.

Please look at the code of Figure 13.

![Book illustration](../images/p251-02.png)

General attributes shared between the two classes Specialized attributes of this class only

Figure 13 Defining the `SmartPhone` class

Line 16: On this line, a class named `SmartPhone` is defined that inherits from the `Mobile` class.

This means that the `SmartPhone` class, in addition to its own attributes and methods, has inherited all attributes and methods of the `Mobile` class and has access to them.

In this situation, the `Mobile` class is called the parent class (`Parent` `class` or `Super` `class`).

The `SmartPhone` class is called the child class (`Child` `class`).

On this line, after the name of the `SmartPhone` class, the name of the parent class (`Parent` `class`) must be written inside parentheses.

Line 17: On this line, the constructor method (`__init__`) of the `SmartPhone` class is defined.

This method runs automatically when a new instance of the `SmartPhone` class is created.


---

**Page 246**

The parameters of this constructor include the phone’s general attributes (`brand`, `model`, and`color`) as well as the smart phone’s specialized attributes (`os` and `camera`).

Line 18: On this line, the parent class (`Mobile`) constructor is called using the `super` function.

The `super` method is used to access the parent class’s methods and attributes in the topic of inheritance.

When a class inherits from another class, using `super` you can call the parent class’s methods without writing the parent class’s name directly.

Note that in this statement only the attributes shared by the child class and the parent class are sent to the `__init__` method of the parent class.

This performs the initialization of the attributes defined in the `Mobile` class.

Note that if this line of code is not written, the parent class attributes are not initialized in the child class.

In this way, code repetition is avoided and attributes shared between classes are managed properly.

Line 19: On this line, the `os` attribute is created for the current instance and its value is set equal to the value of the `os` input parameter.

This attribute represents the smart phone’s operating system.

Line 20: On this line, the `camera` attribute is created for the current instance and its value is set equal to the value of the `camera` input parameter.

This attribute stores the specifications of the smart phone’s camera.

Line 23: On this line, an instance (`Instance`) of the `SmartPhone` class is created.

When this instance is created, the `SmartPhone` class constructor method runs and the values sent are assigned to the parameters.

In addition, by using the `super` function, the parent class (`Mobile`) constructor runs so that the phone’s basic attributes, which are defined in the parent class, are initialized.

![Book illustration](../images/p252-01.png)

Line 24: On this line, the value of the `os` attribute of the `my_smartphone` instance is read and printed in the program output.

The output of this statement will be the value `"android"`.

**Figure 14**

### Activity

Add statements to the program above so that the other attributes of the `my_smartphone` instance are printed.


---

**Page 247**

Calling parent class methods through the child class:

So far you have seen that the `SmartPhone` class has inherited the attributes of the `Mobile` class. If you look at the `SmartPhone` class code, other than the `__init__` method there is no other method inside it. To check whether it has also inherited methods from the parent class (`Parent`), write the following statement at the end of the program and run the program:

```
brand: samsung model: s25 color: gray  )(my_smartphon.show_info
```

**Figure 15**

By observing the output, you see that the `my_smartphone` instance has inherited the `show_info` method from the `Mobile` class.

### Activity

Add statements to the program above so that the other methods of the `my_smartphone` instance are called and run.

Creating a method in the child class independent of the parent:

Here a question arises: can a child class (`Child` `class`) have methods of its own independently?

The answer is yes. For this purpose, you can define new, independent methods inside the child class and use them.

Next, you add to the `SmartPhone` class the methods `take_picture` for taking a photo and `show_os_info` for displaying the operating system name attribute. Carefully write and run the code of Figure 16.

![Figure 16 Defining two new methods inside the SmartPhone class](../images/p253-01.png)

Figure 16 Defining two new methods inside the `SmartPhone` class


---

**Page 248**

Lines 22 and 23: On these lines, the `take_picture` method is defined, and inside it a message stating success in taking a photo is printed.

Lines 25 and 26: On these lines, the `show_os_info` method is defined, and inside it the operating system attribute details are printed.

Overriding a parent method inside the child class (`Method` `Override`) You know that in the `Mobile` class a method named `show_info` is defined that displays the phone’s general information. Now if a class such as `SmartPhone` inherits from the `Mobile` class, this method is also transferred to the child class and can be used without change.

On smart phones, in addition to general information, displaying more information such as the operating system name and camera specifications matters. Using the parent class’s `show_info` method directly is not enough for the `SmartPhone` class, and the behavior of this method needs to change to match the child class’s attributes.

To solve this problem, the `show_info` method is overridden in the `SmartPhone` class. In this way, you can first run the parent class method with the `super`() statement and then display the new information needed. This causes the parent method’s statements to run first in the overridden method of the child class, and then the new statements to be written and run.

Now you can add the `show_info` method to the `SmartPhone` class according to the code below and observe the result of running the program.

![Figure 17](../images/p254-01.png)

**Figure 17**

On the first line of the code, a method named `show_info` is defined inside the `SmartPhone` class. The name of this method is exactly the same as the name of the method in the parent class; for that reason this method is recognized as an override (`Override`) of the parent class method.

On the second line, using the `super` method, the `show_info` method from the parent class (`Mobile`) is run. In this way, the phone’s general information such as brand, model, and color, which are defined in the parent class, are displayed at the beginning of this same method.

On the third line, the value of the `os` attribute, which belongs to the `SmartPhone` class, is printed. This attribute represents the smart phone’s operating system name and does not exist in the parent class.

On the last line, the value of the `camera` attribute is displayed. This attribute is also specific to the `SmartPhone` class and shows the specifications of the smart phone’s camera.


---

**Page 249**

Overriding a parent method in the child class in such a way that the method name stays the same but how it runs changes is called method overriding or `Method` `Override`.

### Activity

Based on what you have learned so far, implement the `GamingPhone` class according to the explanations below:

The `GamingPhone` class inherits from the `SmartPhone` class.

This class, in addition to the attributes inherited from the base class `Mobile` and the `SmartPhone` class, includes the two specialized attributes below:

`gpu:` graphics processor name `vram:` amount of graphics memory This class, in addition to the methods inherited from the `Mobile` and `SmartPhone` classes, also includes the following method:

The `gaming_mode` method: When called, this method prints an appropriate message showing that the phone’s gaming mode is active.

The printed message can include the phone name, the graphics processor name, and the amount of graphics memory.

So far you have become familiar with defining the `Mobile` class and creating instances of it. You also saw that you can access each instance’s attributes and change their values. But this question arises: should all attributes of a class be freely changeable?

Public attributes (`Public`) By default, a class’s attributes are public (`Public`). That is, from any part of the program you can access them and change their values. Some attributes cause no problem even if they are defined as public, because changing them does not cause a logic error in the program. In the `Mobile` class you built earlier, the three attributes `brand`, `model`, and `color` are of this type because:

Changing them is not dangerous.

They do not need special control.

Therefore they can remain `Public`.

Now suppose you also define the phone’s battery attribute as public (for simplicity, assume the battery’s initial value is set to 100%):

```
self.battery = 100
```

In this case, you can change the battery value as follows:

```
my_mobile.battery = 150
my_mobile.battery = -20
```


---
