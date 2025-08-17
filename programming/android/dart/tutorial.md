
# Basic

# What is dart

Dart is modern programming language to build apps fast for many platforms like android, IOS, web, desktop.

It is also optimized for crafting a beautiful user interface and high quality experiences.

# Features

- Free and open-source
- OOP languages
- Used to develop android,iOS and web ...

- Offers modern programming features like null safety and async programming

# Difference between Dart and Flutter

- Dart as above, but it difficult o build complete apps only using dart, because we must manage many things yourself

- Flutter is a framework that uses dart. with the help of flutter => build apps for android, iOS, web, desktop => contains ready-made tools to make apps faster

# Basic program

```
void main() { 
   print("Hello World!"); 
}
```

Explain: 

    - every program starts with a main function
    - each statement must has `;`
    - void main() is the starting point where the execution of program begin

# Create full dart project

Instead of work on single file, but if your project gets bigger you need to manage configurations, packages and assets files. So create dart project will help you to manage this all

```
dart create <project_name>
```

# Run dart project

```
dart run
```

# 2. Variables in dart

Variables are containers used to store value in the program. There are different types of variables.

- String => text
- int => integer
- double => floating point values
- num => any number
- bool => true/false
- var => store any data 

Ex:

```
void main() {
    int age = 20;
    String fistName = "phu";
    double gpa = 3.5;
    num cpa = 3.0;
    bool x = false;
    var lastName = "nguyen";
}
```

# Dart constant

Constant is the type of variable whose value never changes

```
const pi = 3.13;
pi = 4.2; => error
```

# 3. Data type

Data types help to categozie all the different types of data you use in code. The data type specifies what type of value will be stored by variable. Dart supports the following data types:

1. Number: int, double, num
2. Strings: string
3. Booleans: bool
4. Lists: List => ordered of items
5. Maps: Map => key-value pairs
6. Sets: Set => unordered list of unique values
7. Runes: runes => unicode values of string
8. Null: null => null value

## 1. Number

int and double are the subtype of num

You can use num to store both int or double

```
int test=1;
double tes2 = 2.2;
num s = test + tes2;
```

## Round double value to 2 decimal

The method `toStringAsFixed` is used to round the double value upto 2 deciaml places in dart

```
double price  = 23232.22222;
print(price.toStringAsFixed(2)); //change to 3 4 5
```

## 2. String

String helps you to store text data.

```
String firstName ="phu";
```

## Create a multi-line string

```
String contact = '''
    FirstName: Phu,
    LastName: Quang

'''
```

## Special character

- \n => new line
- \t => new tab

## Raw string

Any special character will not work

```
void main() {
// Set price value
num price = 10;
String withoutRawString = "The value of price is \t $price"; // regular String
String withRawString =r"The value of price is \t $price"; // raw String

print("Without Raw: $withoutRawString"); // regular result
print("With Raw: $withRawString"); // with raw result

}

=>result:
Without Raw: The value of price is 	 10
With Raw: The value of price is \t $price

```

## Bool
    
## Lists

Holds multiple values in a single variable.

```
List<String> names = ["Raj", "John", "Max"];
print("Value of names is $names");
print("Value of names[0] is ${names[0]}"); // index 0
print("Value of names[1] is ${names[1]}"); // index 1
print("Value of names[2] is ${names[2]}"); 
```

## Sets

```
void main() {
Set<String> weekday = {"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
print(weekday);
}
```

## Maps

```
void main() {
Map<String, String> myDetails = {
   'name': 'John Doe',
   'address': 'USA',
   'fathername': 'Soe Doe'
};
// displaying the output
print(myDetails['name']);
}
```

## Runes

find unicode values of string

```
void main() {

String value = "a";
print(value.runes);
}

=> (97)
```

## To check runtime type you can use

```
[variable].runtimeType => data type

//check data type

if(variable is int) => true or false
```

## Optionally typed language

- Statically typed

    - type of variable know at compile => compiler can quickly check the issues

    ```
    var myVariable = 50; // You can also use int instead of var
    myVariable = "Hello"; // this will give error
    print(myVariable); 

    => error  
    ```

- Dyamically type

    - type only know at runtime(after program is executed)
    
    ```
    dynamic myVariable = 50;
    myVariable = "Hello";
    print(myVariable);
    ```

# 3. Operators in dart

Used to perform mathematical and logical operations on the variables.

1. +
2. -
3. -expr
3. *
4. / (deviding give double result)
5. ~/ => give int result (deviding)
6. %

## Logical

1. && => and
2. || => or
3. ! => not

## Type test operators

1. is => give true if the object has a specific type
2. is! => is not => give boolean value false if the object has a specific type


# 4. User Input In Dart

Instead of hardcode we can write your value when program run and take a result by using package:

```
import 'dart:io'; //for user input
```

## String input

```
import 'dart:io';

void main() {
  print("Enter name:");
  String? name  = stdin.readLineSync();
  print("The entered name is ${name}");
}
```

## Int input

```
import 'dart:io';

void main() {
  print("Enter number:");
  int? number = int.parse(stdin.readLineSync()!);
  print("The entered number is ${number}");
}
```

## Double input

```
import 'dart:io';

void main() {
  print("Enter a floating number:");
  double number = double.parse(stdin.readLineSync()!);
  print("The entered num is $number");
}
```

# String in Dart

Helps you to store text based data.

## Concat

```
void main() {   
String firstName = "John";
String lastName = "Doe";
print("Using +, Full Name is "+firstName + " " + lastName+".");
print("Using interpolation, full name is $firstName $lastName.");  
  
}
```

## Some attributes(properties) of String

- codeUnits: Returns an unmodifiable list of the UTF-16 code units of this string.
- isEmpty: Returns true if this string is empty.
- isNotEmpty: Returns false if this string is empty.
- length: Returns the length of the string including space, tab, and newline characters.

```
void main() {
   String str = "Hi";
   print(str.codeUnits);   //Example of code units
   print(str.isEmpty);     //Example of isEmpty
   print(str.isNotEmpty);  //Example of isNotEmpty
   print("The length of the string is: ${str.length}");   //Example of Length
}
```

## Some methods of String

- toLowerCase(): Converts all characters in this string to lowercase.
- toUpperCase(): Converts all characters in this string to uppercase.
- trim(): Returns the string without any leading and trailing whitespace.
- compareTo(): Compares this object to another.
- replaceAll(): Replaces all substrings that match the specified pattern with a given value.
- split(): Splits the string at matches of the specified delimiter and returns a list of substrings.
- toString(): Returns a string representation of this object.
- substring(): Returns the text from any position you want.
- codeUnitAt(): Returns the 16-bit UTF-16 code unit at the given index.

## Reverse String in dart

```
void main() { 
  String input = "Hello"; 
  print("$input Reverse is ${input.split('').reversed.join()}"); 
} 
```



# Loop and Condition

## Condition

```
enum Weather{sunny, snowny}

void main() {
  String name = "quang pdhu";

  /**
   * If-else
   */
  if(name == "quang phu") {
    print("ok");
  } else if(name is int) {
    print("fuck");
  } 
  else {
    print("condition failed");
  }

  int numb = 2;

/**
 * Switch
 */
  switch(numb) {
      case 1:
        print("mot");
      case 2:
        print("2");
      default:
        print("default");
  }

  const weather = Weather.snowny;

  switch(weather) {
    case Weather.snowny:
      print("sunny");
    default:
      print("default");
  }



  /**
   * Assert: raise err when condition false
   */


  int age =25;

  // assert(age > 25, "age must less than 25");


  /**
   * Ternary: condition ? exprIfTrue : exprIfFlase
   */

  int high = 170;

  String x = high >= 170 ? "Tall" : "Low";

  print("x: $x");
}
```

## Loop

```
void main() {

  for(int i = 0; i < 10; i++) {
    print("i $i\n");
  }


  //foeach

  List<String> players = ["messi", "cr7", "neymar"];

  players.forEach((name) => print(name));



  
}

void main() {
  List<String> players = ["messi", "ronaldo"];

  // players.forEach((name) => {
  //   print(name)
  // });

  players.asMap().forEach((index, name) => {
    print("$index $name")
  });
}


//exception handling(like js)
//custom exception we need implements Exception
//throw exception => throw new Class_Exception()
```