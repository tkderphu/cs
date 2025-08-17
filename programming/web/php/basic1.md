# Note basic about PHP

# What is php

# How setup

1. Download php: <a href='https://www.php.net/downloads.php?usage=web&os=windows&osvariant=windows-native&version=default&source=Y'>Link</a>

2. Extract zip file

3. Add that path to enviroment

4. Setup ok

# Basic syntax

All php code will be written in this block:

```
<?php

//code php
?>
```

- All keywords in php are case sensitive:
    - echo = ECHO = eCHo
- But with variable it is not case sensitive:
    - $color != $coLor


- To comment code in php we have three ways:
    - Using: `//` => single comment
    - Using: `#` => single comment
    - Using: `/****/` => multiple comment


- In php to create new variable we use this syntax:

```
$name = 'phu'
```

    - In php we dont need provide data type, php automatically know what variable type
    - In php < 7 => we can add string and integer so that doesn't throw exception, but in php >= 7 this will throw an exception
    - variable type includes: `string, int, float, boolean, array, object, resources, NULL, Resource`
    - to get type of variable we use this function: `var_dump($variable)`
    - variable have three scopes:
        1. local => defined in function and only that function can access to that variable
        2. global => can be accessed anywhere in your file code
        3. static => it is used to keep track local variable so that it isn't deleted by system when function is completed
        4. global variables is stored in a array is called $GLOBALS[index]. Index holds the name of variables.


- To show output on screen we use two built keyword:
    - echo: 
        1. echo "t", " dsd", " sd"; //can have many arguments only for "
        2. echo 't' . 6 . ' d'; //only for '

    - print:
        1. like echo but only 1 argument

