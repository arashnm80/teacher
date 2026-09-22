# Writing an Object-Oriented Program


---

**Page 234**

## Learning Unit 1

## Writing an Object-Oriented Program

### Have you ever thought

In the real world, similar objects (such as cars), despite differences in model and color, share common features and behaviors. Which programming concept does this relate to?

Why does maintaining and modifying programs become harder as they grow larger? How can you design a program’s structure so that changes have the least effect on other parts?

If you want to design several characters in a computer game that share similar behaviors but have different features, which programming approach is more suitable?

Why is object-oriented programming used in the design of many large software systems and programs?

Does a “class” in programming more closely resemble a building’s blueprint or the building itself?

### By the end, the student is expected to

1 Design and implement Python classes with appropriate attributes and methods, including default values and access control (`public`, `protected`, `private`).

2 Create instances (`Instance`) of classes and effectively change and manage the values and attributes of those instances during program execution.

3 Use inheritance to create class hierarchies, call parent methods, and override them in child classes according to the program’s needs.

4 Using `OOP` principles, write modular, understandable, and reusable (`reusable`) code that avoids repetition.

5 Gain a basic understanding of how metaclasses work and their role in defining and structuring classes.

6 Analyze simple to intermediate programming problems using object-oriented programming and design and implement object-based solutions.

### Performance standard

Using object-oriented programming concepts in Python, model simple practical problems, design an appropriate class, and by creating and using instances, produce a readable, runnable, and extensible program.


---

**Page 235**

### Object-Oriented Programming (Object-Oriented Programming)

Object-oriented programming is a programming approach in which the parts of a program are modeled as entities similar to the real world. In this approach, instead of thinking only about statements and functions, you first think about things that exist in the real world, have attributes, and can perform actions.

![Book illustration](../images/p241-01.png)

In programming, these things are called objects (`Object`), and this style of programming is called object orientation, or for short (`.O.O.P`).

**Figure 1**

In this approach, the main goal is to recreate the logic and structure of the real world in the programming environment. To understand this idea better, you can look at popular strategy games such as `Age` `of` `Empires` or `Clash` `of` `Clans`. In these games, characters and entities are divided into various groups—from workers and soldiers to vehicles and war machines. Object-oriented programming, by introducing a concept called a class (`Class`), helps you place similar entities into one group. In this way, you can treat each group as a class and specify its attributes and related actions in the program.

![Figure 2](../images/p241-02.png)

**Figure 2**

For now, set games aside and look at a completely real example. Consider an older mobile phone. This phone is not merely a simple device; it has a set of attributes and can perform various tasks and operations.

![Book illustration](../images/p241-03.png)

For example, every mobile phone has these attributes:

It has a color.

It has a brand.

It has a model.

Its battery charge level is known at any moment.

**Figure 3**


---

**Page 236**

### Note

For now, the examples start with older phones, and later in the lesson smart phones and gaming phones will also be covered.

### Activity

Based on information about your own phone or a phone of your choice, complete the table below. (Attributes table) In the table below, you see examples of mobile phones and their attributes:

Samples / Attributes`color`

`brand`

`model`

```
battery
```

My phone`gray`

`nokia`

1100

32%

Your phone Your friend’s phone

If you have two phones of the same model, their attributes are similar, but the battery level or color may differ. Each of these phones is considered a separate object. The characteristics an object has are called attributes (`Attribute`). These attributes specify what each object has.

Also, every mobile phone can perform various actions:

Turn on and off.

Make a call.

Send a message.

### Activity

Besides the actions above, what other things can you do with your own phone? Complete the table below.

1-

3-

2-

4-

A method is the name for the actions an object can perform; it is called a method (`Method`). In fact, methods are like instructions that tell the object what to do.


---

**Page 237**

In the real world, this mobile phone is an “object,” and in object-oriented programming, objects are modeled with exactly the same view.

An object (`Object`) is anything that:

Has attributes (`Attribute`).

Can perform one or more actions (`Method`).

```
نمونه (Instance)
```

In Python, objects created using a class are called instances (`Instance`) of that class. Therefore, a specific mobile phone (for example, your personal phone) is considered an instance (`Instance`) of the mobile phone class.

### Note

From this point on in this book, the term instance (`Instance`) is used instead of the phrase object (`Object`).

Defining a class (`Class`) Now, if you want to create several different mobile phones, writing the attributes and methods separately for each one is not the right approach.

For this, you need a general template that specifies:

1 What attributes every mobile phone has.

2 What actions it can perform.

This general template is called a class (`Class`).

A class is like the blueprint for building a mobile phone, and every mobile phone that is built is in fact an instance (`Instance`) of that class.

Table 1

Terms

Meaning

```
کلاس (Class)
```

General template or construction blueprint

```
نمونه (Instance)
```

An entity created from a class

```
ویژگی (Attribute)
```

What does it have?

```
متد (Method)
```

What does it do?


---
