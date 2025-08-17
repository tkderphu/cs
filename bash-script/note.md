# Get current user
```echo "$USER"```

# Get current date
```
echo "$(date)"
# Format date
echo "$(date '+%Y-%m-%d %H:%M:%S')"
```

# Take input from user
Syntax:
```
read -p "Enter your input: " input
```
## Note
- -s: silent mode (user can see what input they write)
- -p: prompt mode (show placeholder you can know what input write)

# Operator
- Number
    - -eq: equal between number => 5 -eq 5
    - -lt: less than => 5 -lt 6
    - -gt: greater than 6 -gt 5
- String
    - ==: equal between string => "$x" == "$y"
    - !=: not equal
    - -z: String is empty
    - -n: String is not empty

# Arithmetic
```
number=1
number=$((number + 5)) # => number = 6
```
# IF-ELSE
Syntax: 
```
if [[ condition  ]]; then
    echo "do something"
elif [[ condition ]]; then
    echo "do something"
else
    echo "final"
fi
```
# Loop
Syntax:
```
while[[ condition ]]; do
    # do something here
    echo "Write your script here"
done
```
# Hashmap-key pair
Syntax:
```
declare -A users # Define variable users type key-pair

# define variable
user="test"

# check whether users contains key

if [[ ${users[$user]+_}  ]]; then
    echo "User exists"
else
    echo "User doesn't exist."
fi

# Get value from specific user

user_password = "${users[$user]}"
```

# Functions

Functions in Bash are reusable blocks of code that help organize and simplify scripts.

```
greet() {
    echo "Hello, $1!"
}

greet "Alice"
```

# Command-line Arguments

These allow users to pass values to the script when running it.

```
#!/bin/bash
echo "First argument: $1"
echo "Second argument: $2"
```

Run command

```
./script.sh hello world
```

Special variables


| Variable        | Meaning                           |
| --------------- | --------------------------------- |
| `$1`, `$2`, ... | Positional arguments              |
| `$#`            | Number of arguments               |
| `$@`            | All arguments as separate strings |
| `$*`            | All arguments as one string       |


