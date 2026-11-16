<!-- page 244 -->

2. **Gaming phone**: a kind of smartphone that, besides having all the capabilities of a Smartphone, is designed especially to run games and has stronger hardware.

Has a strong and separate graphics processor property

Has a large graphics memory property

![Figure 11: A basic mobile, a smartphone and a gaming mobile](../images/p250-01.png)
*Figure 11: A basic mobile, a smartphone and a gaming mobile*

Following this decision, the company's programmers have been asked to write and define the classes needed for the specialised mobiles.

*Table 2*

|  | Brand | Model | Color | Status | Camera | Operating system¹ | Memory | Graphics processor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Mobile |  |  |  |  |  |  |  |  |
| Smartphone |  |  |  |  |  |  |  |  |
| GamingPhone |  |  |  |  |  |  |  |  |

As seen in the table, all phones have common properties: brand, model, colour and status. So defining these properties again in each of the specialised phone classes would lead to repeated code.

To prevent repeated code and make better use of the phones' common properties, the concept of inheritance in object-oriented programming can be used.

**Inheritance means that a new class can inherit the properties (Attributes) and behaviour (Methods) of another class and use them**.

In this method, first a more general class is defined that includes the properties common to all phones, such as brand, model, colour and status. This kind of class is called the parent class (Parent class or Super class). In this example, the class Mobile, as the parent class, includes all the properties common to all mobiles.

> **Footnotes**
>
> 1- Operating System

<!-- page 245 -->

![Figure 12](../images/p251-01.png)
*Figure 12*

Then more specialised classes are created based on the base class. These classes are called child classes. For example, the class Smartphone, which inherits from the class Mobile, automatically has all the properties of the class Mobile and can, in addition, define its own special properties and behaviours such as the operating system and the camera.

Using this approach brings the following results:

- Less coding

- More readable code

- Better maintainability of the program

Next, a new class named SmartPhone is defined that inherits from the class Mobile. See the code of Figure 13.

![Figure 13: Defining the class SmartPhone](../images/p251-02.png)
*Figure 13: Defining the class SmartPhone*

**Line 16**: in this line a class named SmartPhone is defined that inherits from the class Mobile. This means that the class SmartPhone, besides its own properties and methods, has inherited all the properties and methods of the class Mobile and can reach them.

- In this case the class Mobile is called the parent class (Parent class or Super class).

- The class SmartPhone is called the child class.

- In this line, after the name of the class SmartPhone, the name of the parent class must be written inside parentheses.

**Line 17**: in this line the constructor method (`__init__`) of the class SmartPhone is defined.

- This method runs automatically when a new instance of the class SmartPhone is made.

<!-- page 246 -->

- The parameters of this constructor include the general properties of the phone (brand, model and color) and also the special properties of the smartphone (os and camera).

**Line 18**: in this line the constructor of the parent class (Mobile) is called using the function super.

- The method super is used to reach the methods and properties of the parent class in the topic of inheritance.

- When a class inherits from another class, with super the methods of the parent class can be called without writing the name of the parent class directly.

- Note that in this statement only the properties common to the child class and the parent class are sent to the method `__init__` of the parent class.

- By doing this, the initial values of the properties defined in the class Mobile are set.

- Note that if this line of code is not written, the properties of the parent class are not given values in the child class.

- In this way, repeated code is prevented and the properties common between the classes are managed in a proper way.

**Line 19**: in this line the property os is created for the current instance and its value is set equal to the input value of the parameter os.

This property shows the operating system of the smartphone.

**Line 20**: in this line the property camera is created for the current instance and its value is set equal to the input value of the parameter camera.

- This property keeps the specifications of the smartphone's camera.

**Line 23**: in this line an instance of the class SmartPhone is made.

- When this instance is made, the constructor method of the class SmartPhone runs and the values sent to the parameters are assigned.

- In addition, using the function super, the constructor of the parent class (Mobile) runs so that the basic properties of the phone, which are defined in the parent class, are given values.

![Figure 14](../images/p252-01.png)
*Figure 14*

**Line 24**: in this line the value of the property os of the instance `my_smartphone` is read and printed in the output of the program.

- The output of this statement will be the value "android".

> **Activity**
>
> Add statements to the program above to print the other properties of the instance `my_smartphone`.

<!-- page 247 -->

### Calling the parent class's methods through the child class

So far you have understood that the class SmartPhone has inherited the properties of the class Mobile. If you look at the code of the class SmartPhone, there is no method in it other than `__init__`. To check whether it has inherited the methods from the parent class too, we write the following statement at the end of the program and run the program:

```
my_smartphon.show_info()       brand: samsung model: s25 color: gray
```

*Figure 15*

By looking at the output you understand that the instance `my_smartphone` has inherited the method `show_info` from the class Mobile.

> **Activity**
>
> Add statements to the program above so that it calls and runs the other methods of the instance `my_smartphone`.

### Creating a method independent of the parent inside the child class

Here a question comes up: can the child class have methods of its own independently?

The answer is yes. For this you can define new and independent methods inside the child class and use them.

Next you add to the class SmartPhone the method `take_picture` for taking a photo and `show_os_info` for showing the property of the operating system name. Write and run the code of Figure 16 carefully.

![Figure 16: Defining two new methods inside the class SmartPhone](../images/p253-01.png)
*Figure 16: Defining two new methods inside the class SmartPhone*

<!-- page 248 -->

**Lines 22 and 23**: in these lines the method `take_picture` is defined and inside it a message about the success of taking a photo is printed.

**Lines 25 and 26**: in these lines the method `show_os_info` is defined and inside it the specifications of the operating system property are printed.

### Rewriting the parent's method inside the child class (Method Override)

You know that in the class Mobile a method named `show_info` is defined that shows the general information of the phone. Now if a class such as SmartPhone inherits from the class Mobile, this method is also passed to the child class and can be used unchanged.

In smartphones, besides the general information, showing more information such as the name of the operating system and the specifications of the camera matters. Using the method `show_info` of the parent class directly for the class SmartPhone is not enough, and the behaviour of this method must be changed to suit the properties of the child class.

To solve this problem, the method `show_info` is rewritten in the class SmartPhone. In this way, first the method of the parent class can be run with the statement `super()` and then the new needed information can be shown. This makes it so that in the overridden method of the child class, the statements of the parent method run first and then the new statements are written and run.

Now you can add the method `show_info` to the class SmartPhone as in the following code and see the result of running the program.

![Figure 17](../images/p254-01.png)
*Figure 17*

- In the first line of the code, a method named `show_info` is defined inside the class SmartPhone. The name of this method is exactly the same as the name of the method in the parent class; that is why this method is known as an override of the parent class's method.

- In the second line, using the method super, the method `show_info` of the parent class (Mobile) runs. In this way, the general information of the phone such as the brand, model and colour, which are defined in the parent class, is shown at the start of this method.

- In the third line, the value of the property os, which belongs to the class SmartPhone, is printed. This property shows the name of the smartphone's operating system and does not exist in the parent class.

- In the last line, the value of the property camera is shown. This property is also special to the class SmartPhone and shows the specifications of the smartphone's camera.

<!-- page 249 -->

**Rewriting the parent's method in the child class so that the name of the method stays the same but the way it runs changes is called method rewriting or Method Override**.

> **Activity**
>
> Considering what you have learned so far, implement the class GamingPhone according to the following descriptions:
>
> The class GamingPhone inherits from the class SmartPhone.
>
> Besides the properties inherited from the base class Mobile and the class SmartPhone, this class includes the following two special properties:
>
> - gpu: the name of the graphics processor
>
> - vram: the amount of graphics memory
>
> Besides the methods inherited from the classes Mobile and SmartPhone, this class also includes the following method:
>
> - The method `gaming_mode`: when called, this method prints a suitable message showing that the gaming mode of the phone is active.
>
> The printed message can include the name of the phone, the name of the graphics processor and the amount of graphics memory.

So far you have got to know defining the class Mobile and making instances of it. You also saw that the properties of each instance can be reached and their values changed. But the question comes up: must all the properties of a class be freely changeable?

### Public properties

Normally, the properties of a class are public. That is, they can be reached and their values changed from any part of the program. Some properties cause no problem even if they are defined as public, because changing them does not cause a logical error in the program. In the class Mobile we made earlier, the three properties brand, model and color are of this kind because:

- Changing them is not dangerous.

- They need no special control.

So they can stay Public.

Now suppose you also define the battery property of the phone as public (for simplicity, suppose the initial battery value is set to 100%):

```
self.battery = 100
```

In this case, the battery value can be changed as follows:

```
my_mobile.battery = 150
my_mobile.battery = -20
```
