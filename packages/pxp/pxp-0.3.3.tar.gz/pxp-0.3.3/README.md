# PXP: Python-hosted eXPression minilanguage

PXP is a simple expression-oriented python-hosted minilanguage. It is designed to allow simple but flexible expression evaluation in a python environment.

Example Code 1:

    /* A comment */

    /* Let the compiler know that when the program
     * is run it will have access to a variable
     * named amount with type Number.
     */
    #extern Number amount

    /* Define and set variables. */
    add <- 40.0;
    mul <- 3;

    /* The ? operator is null coalescing, so if amount
     * is null, 0 will be substitued for it.
     */
    return (amount ? 0 + add) * mul;

Example Code 2:

    fn <- 'Lord';
    ln <- 'Voldemort';

    /* The return keyword and closing semicolon are
     * optional.
     *
     * Overloaded '+' operator for string concatenation.
     */
    ln + ', ' + fn


Example Code 3:

    /* Branching with if/elif/else. Branches are
     * expressions like everything else.
     */
    a <- if b < 10:
             if b < 5: 5 - b
             else: 10 - b
         elif b = 10: 10
         else: b - 10;
    b <- 7;
    return a;

Example Code 4:

    /* Switch statements simplify branches where
     * every predicate is just an equality comparison
     * against a common subject.
     */
    a <- switch b
         when 1: "1"
         when 2: "2"
         when 3: "3"
         else: "Something Big!"
    b <- 20;
    return a;

You can see the full grammar [here](config/pxp.ebnf).

## Motivation

Lots of software can [benefit from allowing users to specify expressions to control behavior.](http://catb.org/~esr/writings/taoup/html/minilanguageschapter.html) Typically you want the syntax to be simple and expressive, and the capabilities to be limited. (You don't want your users to have access to your server's filesystem or network, for instance.) PXP allows you to accomplish this in python projects in a flexible manner.

## Features

- Simple syntax
- Infix operators with familiar algebraic precedence and subexpressions
- Static, inferred typing
- Lazy evaluation
- Small but useful standard library
- Extensible

### Simple Syntax

A PXP program can be (and often is) just a single expression. For this reason, even though you can prefix the return expression with `return ` and postfix it with `;`, you can also omit either or both of these. The program:

    return 5 + 3;

and:

    5 + 3

result in the same thing, namely the value `8`.

### Static, Inferred Typing

When you declare a variable, it is not necessary to declare the type because PXP can determinte it for you. So in this program PXP can determin that `a` is a number and `b` is a string:

    a <- 10;
    b <- "Albus Dumbledor";

In addition, the compiler can determine the types of expressions and make sure your operators and function calls are correct. PXP knows that this program should call the string concatenation operator:

    day <- 'Monday';
    month <- 'July';
    'a ' + day + ' in ' + month

And this program should call the numeric addition operator:

    the_answer <- 40;
    to_the_question_is <- 2;
    the_answer + to_the_question == 42

### Lazy Evaluation

PXP stores the expressions for assignments, and only evaluates them when they're used in the return statement. This has several implications. First, the order of declaration of variables is immaterial. The following program will evaluate correctly:

    a <- b * 3;
    b <- 10;
    return a;

In addition to this, PXP standard library functions (and any you provide in the environment you run the program from, if written correctly) will only evaluate the arguments it needs.

Consider the following program:

    #extern Number amount

    return if(amount != 0, 10 / amount, 0);

If amount were `0`, resolving `10 / amount` would result in a logic error. However, since only the value that correlates with the result of the predicate argument is evaluated, `10 / amount` is never evaluated and no logic error is thrown.

Also, the logical "and" `&` and "or" `|` operators evaulate the first argument to start, and only the evaluate the second argument if necessary.

Finally, unused assignments are stripped from the compiled code. Consider:

    a <- b + 20;
    b <- 3;
    c <- d ^ 2;
    a + b

Since `c` is never mentioned in the return statement, it is never evaluated (which is good since `d` is never declared!) and stripped from the compiled code that is passed to the interpreter.

### Extensible

Since PXP is hosted in python, you construct the interpreter. The interpreter, by default, includes all the functions and constants declared in the standard library. You can pass in your own scope, declaring functions and constants that can be used in your expressions. Just make sure to declare them in the PXP code using the `#extern` directive.

## Native Types

PXP recognizes three native types: Numbers, Booleans and Strings.

Numbers are represented by python Decimal, and therefore have arbitrary precision.

Strings are delimited by either single quotes `'` or double quotes `"` and those characters can be used in strings delimited by them by escaping them with a `\`. The values of the following two variables are the same:

    a <- "Hello \"Friends\"";
    b <- 'Hello "Friends"';

## Variables

In PXP, simple identifiers must start with an underscore `_` or a letter `[A-Za-z]` and then can have zero or more underscores, letters or numbers following.

Many times when you're working with real world data, it has names that don't follow this convention (such as the column names in a spreadsheet.) You could make some kind of convention of how those would be renamed so they could have names that are valid identifiers, and then put the burden on your user to make sure they enter the names properly. Or, you could have some kind of delimited complex identifier functionality. PXP takes the latter course.

Anywhere an identifier can appear, you can have either a simple identifier, as defined above, or what we call a complex identifier. A complex identifier is just an opening bracket `[`, or or more printable character, except for a closing bracket (`]`) followed by a closing bracket `]`. So, you can have identifiers such as:

- `[First Name]`
- `[500 hz]`
- `[!@#^%$*kjhsfi123]`
- Or whatever.

## Operators

In PXP, operators are just functions. They have a special infix (or in some cases, prefix) notation, but otherwise work just like functions in the standard library, or functions you might put in the scope.

The operators will be described more fully in the Standard Library section, but we'll present an overview of them here.

PXP recognizes the following operators:

### Numbers
`+, -, *, /, %, ^, ?, <, <=, =, !=, >=, >`

### Strings
`+, ?, <, <=, =, !=, >=, >`

### Boolean
`?, =, !=, |, &, ! (unary logical negation)`

#### The `?` Operator

The `?` operator is the null-coalescing operator. So in the following program:

    #extern Number amount
    amount ? 0

Returns amount if amount is not null, or 0 if is.

We mentioned above that operators are just functions. We also mentioned that complex identifiers can have non-alphanumeric characters. One neat consequence of those two facts is that you can call operators as functions:

    a <- [operator+](3, 4);
    b <- [operatorunary!](true);

## Interpreted, Comipiled, or what?

**Coming soon!**

## Standard Library

### Operators
operator!=(**Boolean** *left*, **Boolean** *right*) → **Boolean**

> Returns True if left is not equal to right.

operator&(**Boolean** *left*, **Boolean** *right*) → **Boolean**

> Returns True if both left and right evaluate to True, False otherwise.
>
> If left is not True, the value of right doesn't matter, so right will not be evaluated.

operator=(**Boolean** *left*, **Boolean** *right*) → **Boolean**

> Returns True if left is equal to right.

operator?(**Boolean** *left*, **Boolean** *right*) → **Boolean**

> Returns the left if left is not null, otherwise right. Right is not resolved until it is determined that left is null.

operatorunary!(**Boolean** *arg*) → **Boolean**

> Returns the negation of arg. If arg is True, False is returned. If arg is False, True is returned.

operator|(**Boolean** *left*, **Boolean** *right*) → **Boolean**

> Returns True if left or right evaluate to True, False otherwise.
>
> If left is True, the value of right doesn't matter, so right will not be evaluated.

operator!=(**Number** *left*, **Number** *right*) → **Boolean**

> Returns True if left is not equal to right.

operator%(**Number** *left*, **Number** *right*) → **Number**

> Returns the remainder from left / right.

operator\*(**Number** *left*, **Number** *right*) → **Number**

> Returns the product of two numbers.

operator+(**Number** *left*, **Number** *right*) → **Number**

> Returns the sum of two numbers.

operator-(**Number** *left*, **Number** *right*) → **Number**

> Returns the difference of two numbers.

operator/(**Number** *left*, **Number** *right*) → **Number**

> Returns the quotient of two numbers.

operator<(**Number** *left*, **Number** *right*) → **Boolean**

> Returns True if left is strictly less than right.

operator<=(**Number** *left*, **Number** *right*) → **Boolean**

> Returns True if left is less than or equal to right.

operator=(**Number** *left*, **Number** *right*) → **Boolean**

> Returns True if left is equal to right.

operator>(**Number** *left*, **Number** *right*) → **Boolean**

> Returns True if left is strictly greater than right.

operator>=(**Number** *left*, **Number** *right*) → **Boolean**

> Returns True if left is greater than or equal to right.

operator?(**Number** *left*, **Number** *right*) → **Number**

> Returns the left if left is not null, otherwise right. Right is not resolved until it is determined that left is null.

operator^(**Number** *left*, **Number** *right*) → **Number**

> Returns the value of left raised to right.

operatorunary-(**Number** *arg*) → **Number**

> Returns the negation of arg.

operator!=(**String** *left*, **String** *right*) → **Boolean**

> Returns True if left is not lexicographically equal to right.

operator+(**String** *left*, **String** *right*) → **String**

> Returns the concatenation of left and right.

operator<(**String** *left*, **String** *right*) → **Boolean**

> Returns True if left is lexicographically strictly less than right.

operator<=(**String** *left*, **String** *right*) → **Boolean**

> Returns True if left is lexicographically less than or equal to right.

operator=(**String** *left*, **String** *right*) → **Boolean**

> Returns True if left is lexicographically equal to right.

operator>(**String** *left*, **String** *right*) → **Boolean**

> Returns True if left is lexicographically strictly greater than right.

operator>=(**String** *left*, **String** *right*) → **Boolean**

> Returns True if left is lexicographically greater than or equal to right.

operator?(**String** *left*, **String** *right*) → **String**

> Returns the left if left is not null, otherwise right. Right is not resolved until it is determined that left is null.

### General
if(**Boolean** *predicate*, **Boolean** *if_true*, **Boolean** *if_false*) → **Boolean**

> Returns if_true if predicate evaluates to true, if_false otherwise.
>
> predicate is resolved and evaluated first, and then only the argument that will be returned is resolved and evaluated.

if(**Boolean** *predicate*, **Number** *if_true*, **Number** *if_false*) → **Number**

> Returns if_true if predicate evaluates to true, if_false otherwise.
>
> predicate is resolved and evaluated first, and then only the argument that will be returned is resolved and evaluated.

if(**Boolean** *predicate*, **String** *if_true*, **String** *if_false*) → **String**

> Returns if_true if predicate evaluates to true, if_false otherwise.
>
> predicate is resolved and evaluated first, and then only the argument that will be returned is resolved and evaluated.

is\_null(**Boolean** *value*) → **Boolean**

> Returns True if the value is None.

is\_null(**Number** *value*) → **Boolean**

> Returns True if the value is None.

is\_null(**String** *value*) → **Boolean**

> Returns True if the value is None.

is\_num(**String** *value*) → **Boolean**

> Returns True if the string value can be parsed as a number.

to\_bool(**Number** *value*) → **Boolean**

> Converts a Number to a Boolean.
>
> Returns False for 0 and True for all other values.

to\_bool(**String** *value*) → **Boolean**

> Converts a String to a Boolean.
>
> The lower-case version of the value must be 'true' or 'false', otherwise an error will be thrown.

to\_num(**String** *value*) → **Number**

> Returns the number representation of the string value.
>
> This is an unchecked conversion, so if the string is not a valid number an exception will be thrown.

to\_str(**Boolean** *value*) → **String**

> Returns the string representation of the value.

to\_str(**Number** *value*) → **String**

> Returns the string representation of the value.

to\_str(**String** *value*) → **String**

> Returns the string representation of the value.

### Math
math.abs(**Number** *value*) → **Number**

> Returns the absolute value of value.

math.ceil(**Number** *value*) → **Number**

> Returns value if value is a whole number, otherwise the next largest whole number.

math.cos(**Number** *value*) → **Number**

> Returns the cosine of value. Value must be in radians.

math.degrees(**Number** *value*) → **Number**

> Converts a radians value to degrees.

math.floor(**Number** *value*) → **Number**

> Returns value if value is a whole number, otherwise the next smallest whole number.

math.log(**Number** *value*, **Number** *base*=e) → **Number**

> Returns the log of value. If not specified, the log is a natural log with base e.

math.log10(**Number** *value*) → **Number**

> Returns the log base 10 of value.

math.log2(**Number** *value*) → **Number**

> Returns the log base 2 of value.

math.pow(**Number** *value*, **Number** *exp*) → **Number**

> Returns value raised to exp.

math.radians(**Number** *value*) → **Number**

> Converts a degrees value to radians.

math.root(**Number** *value*, **Number** *root*) → **Number**

> Returns the nth root of value.

math.round(**Number** *value*, **Number** *ndigits*=0) → **Number**

> Rounds value to the nearest nth digit.
>
> If ndigits is not specified then value is rounded to the nearest whole number.

math.sin(**Number** *value*) → **Number**

> Returns the sine of value. Value must be in radians.

math.sqrt(**Number** *value*) → **Number**

> Returns the square root of value.

math.tan(**Number** *value*) → **Number**

> Returns the tanget of value. Value must be in radians.

### Str
str.endswith(**String** *subject*, **String** *value*) → **Boolean**

> Returns True if subject ends with value.

str.find(**String** *subject*, **String** *value*, **Number** *start*=null, **Number** *end*=null) → **Number**

> Returns the 0-based index of value in subject, or -1 if value is not present in subject.
>
> start and end are indicies within which to perform the search, if present. The bounds are [start, end). If start or end are negative, their position is calculated from the end of the string.

str.len(**String** *subject*) → **Number**

> Returns the number of characters present in subject.

str.lower(**String** *subject*) → **String**

> Returns subject with all uppercase characters converted to their lowercase equivalents.

str.replace(**String** *subject*, **String** *old*, **String** *new*, **Number** *count*=-1) → **String**

> Searches through subject for all occurrences of old and replaces them with new. If count is given, only at most count replacements will be made.

str.slice(**String** *subject*, **Number** *start*=null, **Number** *end*=null) → **String**

> Returns a slice (or substring) of subject.
>
> The bounds are [start, end). start and end can be negative, in which case their position is calculated from the end of the string.

str.startswith(**String** *subject*, **String** *value*) → **Boolean**

> Returns True if subject starts with value.

str.strip(**String** *subject*) → **String**

> Returns subject with all leading and trailing whitespace removed.

str.upper(**String** *subject*) → **String**

> Returns subject will all lowercase characters converted to their uppercase equivalents.



## TODOs

**Coming soon!**
