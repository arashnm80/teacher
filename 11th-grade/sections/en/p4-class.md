<!-- page 238 -->

Now it is time to create your first class in the programming environment and then, using that class, make an instance. Type the code of Figure 4 carefully into a new file.

![Figure 4: The first code for defining](../images/p244-01.png)
*Figure 4: The first code for defining*

**a class and making an instance**

**Line 1**: a class named Mobile is defined.

- A class is in fact a pattern or a plan for making mobiles.

- Note that the class is not the mobile itself but a pattern for making mobiles.

- According to the naming standards in Python (PEP8), class names must be written in the PascalCase style; that means the first letter of the class name and the first letter of all the words that make it up are capital.

**Line 2**: this method plays the role of the class's constructor method in Python. This method is also called the initializer.

- Whenever an instance is made from the class Mobile, that is, by running line 7, this method runs automatically.

- The main job of this method is to give initial values to the properties of the instance.

- Note that `__init__` is a conventional name in Python and cannot be changed. On the left and the right of the word init, the underscore character is typed twice.

**Lines 3 and 4**: specify the properties of the instance.

- Each mobile has a brand and a colour.

- In the code given, `self.brand` and `self.color` are both known as attributes.

- The word self points to the very instance that is being made, and brand and color are the names of properties that belong to that instance.

<!-- page 239 -->

**Lines 5 and 6**: empty lines

- According to the Python coding standards (PEP8), after the end of the class definition two empty lines must be put so that the border between the class and the global code part is clearly marked.

**Line 7**: making an instance

- In this line you have made an instance named `my_mobile` from the class Mobile.

- The value "nokia" is given for the property brand and the value "gray" for the property color.

![Figure 5](../images/p245-01.png)
*Figure 5*

**Line 8**: reaching a property

- By using the name of the instance and the dot (.), you reach its properties.

- This statement prints the value of the property brand for the instance `my_mobile`.

**Line 9**: an empty line

- According to the PEP8 standards, after the end of the code an empty line is also put so that the end of the file is marked from the code in a readable and standard way.

Note that if you did not fully understand all the details at this stage, do not worry; this is a new topic, and as the lessons continue, with more activities, reviewing the code and building more programs, the concepts will gradually become clear and settle in.

Now run the program; you will see that the value of the property brand of the mobile you made, that is nokia, is printed. Note that at this stage the class contains only attributes and for now no behaviour or method other than the constructor (`__init__`) has been defined for the instances.

Now the running process of the program is described with a picture. Look carefully at Figure 6.

![Figure 6: The running process of the program](../images/p245-02.png)
*Figure 6: The running process of the program*

<!-- page 240 -->

As seen in the figure, after line 7 runs, which is for making the instance `my_mobile`, the following steps happen:

1. The arguments "nokia" and "gray" are sent to the method `__init__` and put in the parameters brand and color.

2. The value of the parameter brand is put into `self.brand` and the value of the parameter color into `self.color`.

3. At this stage the wanted instance will be made.

> **Activity**
>
> At the end of the program, add a statement that prints the colour of the mobile.

> **Activity**
>
> Inside the method `__init__`, add a statement that also considers the model of your phone as a property. Do not forget that in line 7 you must also add the model of your own phone. Try to do this activity yourself, but if you are still unsure, you will see the answer of this code next and can compare it with your own code.

Next, based on the class you defined, make another instance as a mobile for your friend. Write the code of Figure 7 carefully.

![Figure 7: Making an instance](../images/p246-01.png)
*Figure 7: Making an instance*

<!-- page 241 -->

**Line 4**: a new property for the phone's model is defined and given a value.

**Line 9**: a new instance named `friend_mobile` with properties different from `my_mobile` is created.

![Figure 8](../images/p247-01.png)
*Figure 8*

**Lines 15 to 17**: in these lines the properties of the second instance are printed.

> **Note**
>
> Note that `my_mobile` and `friend_mobile` are both separate instances made from the class Mobile.

Next, add a method to the class Mobile to print the values of all the properties of the instance you made. Change the previous code as in Figure 9.

![Figure 9: Adding a method](../images/p247-02.png)
*Figure 9: Adding a method*

**`show_info`**

<!-- page 242 -->

**Line 7**: this line defines a method named `show_info` inside the class Mobile. Methods are functions that are related to a class and can reach the attributes of that class.

- The parameter self in the definition of the method points to the very instance on which the method is called. In other words, self lets the class Mobile reach the attributes specific to each instance of type Mobile.

**Lines 8 to 10**: this statement shows the values of the brand, model and colour properties of the instance with clear labels.

**Line 14**: in this line the method `show_info` of the instance `my_mobile` is called and run.

In the same way you can define more methods for this class. For example the method `incoming_call` is for showing a message when a call is received. Write the code of this method under the method `show_info` according to Figure 10.

![Figure 10: Adding a method](../images/p248-01.png)
*Figure 10: Adding a method*

**`incoming_call`**

- The first line defines a method named `incoming_call` inside the class Mobile. This method receives a parameter named `phone_number`, which shows the phone number of the caller.

- The statements inside the method show the message "Incoming call" and the caller's phone number in the output.

- Note that this method must be defined inside the class Mobile and at the same level as the method `__init__`, so it is placed one tab further in than the body of the class.

- In the last line of the program, the method `incoming_call` is called on the instance `my_mobile`.

- The argument "0912-345-6789" is sent as the parameter `phone_number`, which shows the caller's phone number. Then the method runs and shows the specified messages and the given phone number.

<!-- page 243 -->

> **Activity**
>
> In the class Mobile create a method named `make_call`. This method must receive a parameter named `phone_number` that holds the phone number you want to call. The method must announce the start of the dialling operation by printing suitable messages. For example, you can print messages such as "Calling..." or "Dialing...".

### Setting a default value for properties

For more interest and efficiency, next a property will be defined whose value can be changed after the program runs. So inside the class, the property of the on and off state (status) will be defined and a default value for it too. It is enough to define a new property in the method `__init__` like the following code.

```
self.status = "on"
```

Note that when defining another instance there is no need to give a value for this property.

**Changing the value of a property**: in this way, after creating the instance `my_mobile`, its value will be changed simply by writing the following code.

```
my_mobile = Mobile("nokia", "1100", "gray")
my_mobile.status = "off "
```

In this statement the dot sign is used to reach the property of an instance. This line asks Python to find the property status related to the instance `my_mobile` and then put the value "off" in it.

### Inheritance

Suppose that in a mobile phone manufacturing company, until now only basic versions of the mobile phone have been produced; phones whose features are limited to properties such as brand, model, colour and status, and that have no operating system and no camera. The most important thing that can be done with these mobile phones is making phone calls and sending text messages. In this company there is one main class named Mobile that models these basic properties.

Now the company has decided to design a new generation of mobile phones: smartphones (Smartphone), which, besides the basic features of a mobile phone, offer capabilities such as an operating system and a camera, and also more specialised models, such as gaming phones, which are designed to run games better with stronger hardware.

1. **Smartphone**: a smartphone is a kind of mobile phone that, by using an operating system, makes it possible to run applications and offers advanced capabilities beyond calls and text messages.

Has an advanced camera property

Has an installable and upgradable operating system property
