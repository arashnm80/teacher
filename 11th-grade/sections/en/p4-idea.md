<!-- page 234 -->

## Learning unit 1

## Have you ever thought about this

- In the real world, similar objects (such as cars) have common properties and behaviours despite differences in model and colour. Which concept in programming is this related to?

- Why does maintaining and fixing programs become harder as their size grows? How can the structure of a program be designed so that changes have the least effect on other parts?

- If you want to design several characters with similar behaviours and different properties in a computer game, which programming method is more suitable?

- For what reason is the object-oriented programming style used in designing many pieces of software and big programs?

- What is a "class" in programming more like: the plan of a building or the building itself?

## By the end, the student is expected to

1. Design and implement Python classes with suitable properties and methods, together with setting default values and managing access (public, protected, private).

2. Create instances from classes and effectively change and manage the values and properties of these instances while the program runs.

3. Using inheritance, create class hierarchies, call parent methods and override them in the child classes according to the needs of the program.

4. Using the principles of OOP, write modular, understandable and reusable code that prevents repeating code.

5. Gain a basic understanding of how metaclasses work and their role in defining and structuring classes.

6. Analyse simple to medium programming problems using object-oriented programming and design and implement object-based solutions.

## Performance standard

Using the concepts of object-oriented programming in Python, model simple and practical problems, design a suitable class and, by creating and using instances, produce a readable, runnable and extensible program.

<!-- page 235 -->

**Object-Oriented Programming**

Object-oriented programming is a way of programming in which the parts of the program are modelled as entities like the real world. In this method, instead of thinking only of statements and functions, you first think of things that exist in the real world, have properties and can do something.

![Figure 1](../images/p241-01.png)
*Figure 1*

These things are called objects in programming, and this style of programming is called object-orientation, or `O.O.P.` for short.

In this approach the main goal is to recreate the logic and structure of the real world in the programming environment. To understand this concept better, we can mention common strategy games such as Age of Empires or Clash of Clans. In these games, characters and entities are divided into various groups; from workers and soldiers to vehicles and war machines. By introducing a concept called class, object-oriented programming helps you put similar entities in one group. In this way you can consider each group as a class and specify the properties and jobs related to it in the program.

![Figure 2](../images/p241-02.png)
*Figure 2*

For now, let us move away from the world of games and look at a completely real example. Consider an old mobile phone. This mobile phone is not merely a simple device, but has a set of properties and can do different tasks and operations.

![Figure 3](../images/p241-03.png)
*Figure 3*

For example every mobile phone has these properties:

- It has a colour.

- It has a brand.

- It has a model.

- The level of its battery charge is known at every moment.

<!-- page 236 -->

> **Note**
>
> For now we start with examples of old phones, and later in the lesson smartphones and gaming phones will be covered as well.

> **Activity**
>
> Based on the information of your own phone or any phone you like, complete the information of the following table. (The table of properties)
>
> In the following table you see examples of mobile phones and their properties:
>
> | Examples / properties | color | brand | model | battery |
> | --- | --- | --- | --- | --- |
> | My phone | gray | nokia | 1100 | %32 |
> | Your phone |  |  |  |  |
> | Your friend's phone |  |  |  |  |

If you have two phones of the same model, their properties are similar, but the battery level or the colour can differ. Each of these phones counts as a separate object. The characteristics an object has are called properties (attributes). These properties specify what each object has.

Also each mobile phone can do different things:

- Turn on and off.

- Make a call.

- Send a message.

> **Activity**
>
> Besides the jobs above, what other things can you do with your own phone? Complete the following table.
>
> | -1 | -3 |
> | --- | --- |
> | -2 | -4 |

### Method

The things an object can do are called methods. In fact methods are like instructions that tell the object what to do.

<!-- page 237 -->

In the real world this mobile phone is an "object", and in object-oriented programming too, objects are modelled with exactly this view.

### Object

An object is anything that:

- has properties (Attributes).

- can do one or more jobs (Methods).

### Instance

In Python, objects that are made using a class are called instances of that class. So a specific mobile phone (for example your own mobile) counts as an instance of the mobile phone class.

> **Note**
>
> From now on in this book, the term instance is used instead of the word object.

### Defining a class

Now if you want to make several different mobile phones, it is not right to write the properties and methods separately for each one.

For this we need a general template that specifies:

1. what properties each mobile phone has.

2. what jobs it can do.

This general template is called a class.

A class is like the plan for building a mobile phone, and every mobile phone that is made is in fact an instance of that class.

*Table 1*

| Terms | Meaning |
| --- | --- |
| Class | A general template or a building plan |
| Instance | A thing made from a class |
| Attribute | What does it have? |
| Method | What does it do? |
