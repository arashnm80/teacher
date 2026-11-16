<!-- page 62 -->

**Function**

A function is a block or piece of code that is defined once and can be called many times from many places in a program.

![Figure 129](../images/p068-01.png)
*Figure 129*

### Advantages of using functions

- By defining a function, the programmer writes the code only once and can then call and use it anywhere in the program, or even in other projects.

- Dividing code into small, clear functions makes it much easier to understand.

- Finding and fixing bugs and making changes in the code become much simpler.

- Organizing the code logically and neatly, and the overall structure of the program, become easier.

**Defining a function**: a function is defined with the keyword def, followed by the function's name and parentheses.

The general form of defining a function with input parameters is:

![Figure 130](../images/p068-02.png)
*Figure 130*

```
def پارامترهای تابع) نام تابع(:
```

the statement or statements in the body of the function

the value or values returned with return

<!-- page 63 -->

**Example**: this program defines a function named `show_store_name` with the statement `print ("Digital Online Store")` in it (Figure 131).

![Figure 131](../images/p069-01.png)
*Figure 131*

**Example**: this program also defines a function named greet with the statement `print("Hello! ")` in it (Figure 132).

![Figure 132](../images/p069-02.png)
*Figure 132*

**Example**: in this program the function `greet()` is defined with no parameters, so no argument needs to be passed when it is called (Figure 133).

![Figure 133](../images/p069-03.png)
*Figure 133*

Output

**Example**: in this program too the function is defined with no parameters. No argument needs to be passed when it is called (Figure 134).

![Figure 134](../images/p069-04.png)
*Figure 134*

<!-- page 64 -->

### Parameters and arguments

What is a parameter? A function can receive inputs. The inputs of a function, as named when the function is defined, are called parameters (parameter).

What is an argument? The inputs given to a function when it is called.

- After it is defined, a function must be called in order to run. If you only define a function and never call it, nothing happens; it is as if it had never been defined.

- To call a function, write its name and send it as many arguments as it has parameters (this is called passing). You can call a function many times.

- A function is called like this:

function name : (function arguments)

**Example**: in the example in Figure 135, the function `show_product(name, price)`

is defined with the two parameters name and price. When it is called, two values must be passed as arguments.

![Figure 135](../images/p070-01.png)
*Figure 135*

Output

**Example**: in the example in Figure 136, the function `print_age(age)` has one parameter named age. When it is called, one argument is passed to it. As you can see, `print_age(age)` is called twice, with two different arguments.

![Figure 136](../images/p070-02.png)
*Figure 136*

Output

<!-- page 65 -->

> **Note**
>
> The order, number, and type of the parameters (when the function is defined) must match the order, number, and type of the arguments (when the function is called).

If the order and type of the arguments passed are not respected, the output is wrong. There is no error when the program runs, but the program's logic is wrong.

The solution is to use **keyword arguments** (keyword arguments), that is, named arguments: when calling the function you can write the parameter name with the assignment operator.

**Example**: look at the code in Figure 137 and check the outputs. Calling the function without respecting the order of the arguments makes it print the price first and then the item name, which is wrong logic.

![Figure 137](../images/p071-01.png)
*Figure 137*

**Example**: in the example in Figure 138, keyword arguments are used to avoid wrong output when the arguments are passed out of order. Write the program and compare the result with the previous example.

![Figure 138](../images/p071-02.png)
*Figure 138*

> **Note**
>
> When arguments are given to a function **without the parameter name**, the order of sending them matters, because each argument is **assigned to the parameters of the function in order**. These arguments are called **positional arguments**.

> **Activity**
>
> Write a function named square that takes a number and prints its square.

<!-- page 66 -->

> **Note**
>
> Write a function that takes two numbers as parameters and shows their sum.

> **Note**
>
> Write a function that takes the names of 3 users from the input as parameters and prints them.

**Example**: the number of arguments passed to a function must equal the number of its parameters when it was defined. Otherwise an error message is shown when the program runs (Figure 139).

![Figure 139: The error message shown after running the program](../images/p072-01.png)
*Figure 139* — The error message shown after running the program

> **Note**
>
> A parameter can be given a default value. If no argument is given, the **default value** is used.

**Example**: on the first line of the code in Figure 140, the function is defined with one parameter. On line 4 it is called without an argument, so its default value "Tehran" is used. On line 5 the function is called with an argument. Write the program and check the result. Change the default value and run the program again.

![Figure 140](../images/p072-02.png)
*Figure 140*

<!-- page 67 -->

**Example**: in this example the function is defined with two parameters that have default values. On each call the arguments are passed in a different way. Write the program and check the result. Change the default values and run the program again (Figure 141).

![Figure 141](../images/p073-01.png)
*Figure 141*

### The return value of a function

A function can **calculate a value and give it back to the program** to be used later; this is called the return value (**Return Value**). Without return the function does its job (for example, it prints) but gives no value back, and if you store the function's result in a variable, its value is None (Figure 142).

![Figure 142](../images/p073-02.png)
*Figure 142*

**Example**: running the program in Figure 143 shows the value 8. But the number 8 is **not stored**, and it cannot be used anywhere else. Now change the program to use return and see the result.

![Figure 143](../images/p073-03.png)
*Figure 143*

**This time**: the function **returns 8**, the return value is stored in the result variable, and it can be used again.

**Example**: without return, (price \* count) is only calculated and no value is given back to the program; so calling `total_ price (2, 200000)` stores None in the variable x, and running the program prints None (Figure 144).

![Figure 144](../images/p073-04.png)
*Figure 144*

<!-- page 68 -->

**Example**: with return, the calculated value is given back to the program and can be stored in the variable x; printing x shows the stored value (Figure 145).

![Figure 145](../images/p074-01.png)
*Figure 145*

> **Activity**
>
> Build a function named `avg_numbers` that takes three numbers and returns their average.

**Example**: write a function that calculates the total price of a purchase and gives a 10% discount if more than 5 items are bought. An if is used inside the function to check the condition.

If the condition (`count > 5`) holds, the discounted value is returned.

If the condition does not hold, the value without discount is returned.

return is used so that the calculated result comes back out of the function and can be printed or stored (Figure 146).

![Figure 146](../images/p074-02.png)
*Figure 146*

### Using a loop inside a function

A loop is used inside a function so that **certain statements** run several times **automatically**, **as long as a given condition holds** or **a set number of times**. This **reduces repeated code**, **makes the code more readable**, and **makes the function work better**. Example: in this example the function prints the natural numbers less than 6. Run the program and see the result (Figure 147).

![Figure 147](../images/p074-03.png)
*Figure 147*

<!-- page 69 -->

**Example**: the function first defined has one parameter named names, whose argument is expected to be a list of names (Figure 148).

The for loop takes the elements of the list one by one and assigns each to the name variable.

The print statement also runs inside the loop and prints the names separately.

Before the function is called, on the first line of the program, the students list holding the students' names is created. Then the function is called with the argument students. The loop inside the function prints the names in the list one by one.

![Figure 148](../images/p075-01.png)
*Figure 148*

> **Activity**
>
> ![Book image](../images/p075-04.png)
>
> The function written here calculates the sum of all the numbers in a list. Write and run the program. With your teacher's guidance, explain its lines of code. Change the function so that the user enters the list elements from the keyboard.

> **Activity**
>
> ![Book image](../images/p075-02.png)
>
> The function written here calculates and shows the length of the string the user enters. Run and examine the program, and with your teacher's guidance explain the code opposite.

> **Activity**
>
> ![Book image](../images/p075-03.png)
>
> The code opposite finds and shows the largest number in a list. Run the code and explain its lines.
