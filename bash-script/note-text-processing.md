# Note text processing command

# grep
```
grep "error" log.txt
```
## Note
-   Searchs for the word error in file log.txt and prints all line contains it
-   Common flags:
    -   -i: Case sensitive
    -   -r: Recursive search in directories
    -   -n: Show line numbers
# ```awk``` – Field and pattern-based text processing
```
awk '{print $1, $3}' data.txt
```
Prints the first and third columns of each line in data.txt. Fields are separated by default by whitespace.
- Powerful for column/field manipulation
- Supports conditionals and arithmetic

# ```cut``` – Extract specific columns or bytes
```cut -d ',' -f2 data.csv``` <br/>
Prints the second field in each line from data.csv, using comma as a delimiter.
Flags:
- -d: Set delimiter
- -f: Specify fields to extract
# sed
```
sed 's/foo/bar/g' input.txt
```
## Note
-   Searchs for the word foo in file input.txt and replace all words foo to bar, don't change to original file and prints the content of it.
-   Common flags:
    -   -i: Edit-inplace //change to original file
    -   ```s/foo/bar/g```: Substitution, with ```g``` meaning global (all occurrences in line)
# uniq, head, tail, wc, sort, paste
- uniq: Remove duplicate lines(must be sorted first)
- head: View start file: ```head -n 5 file.txt```
- tail: View end file: ```tail -n 5 file.txt```
- wc: word, line, byte count
    - Flag:
        - -l: line count
        - -w: word count
        - -c: byte count
- paste: combines lines from fileOne and fileTwo  horizontally(side by side)
<br/>
```paste file1.txt file2.txt```
- sort: Sort lines in a file
    - Flag:
        - -r: Reverse order
        - -n: Numberic sort
        - -u remove duplicates
<br/>
# Exercise
``` access.log```
```
192.168.1.10 - - [02/Jul/2025:10:30:01 +0000] "GET /index.html HTTP/1.1" 200 4523
192.168.1.11 - - [02/Jul/2025:10:30:02 +0000] "POST /login HTTP/1.1" 302 1234
192.168.1.10 - - [02/Jul/2025:10:30:03 +0000] "GET /dashboard HTTP/1.1" 200 7890
192.168.1.12 - - [02/Jul/2025:10:30:04 +0000] "GET /index.html HTTP/1.1" 404 0
192.168.1.11 - - [02/Jul/2025:10:30:05 +0000] "GET /dashboard HTTP/1.1" 200 7890
192.168.1.13 - - [02/Jul/2025:10:30:06 +0000] "GET /index.html HTTP/1.1" 200 4523
```

### E1:  Show top IPs by number of requests
```
cut -d " " -f1 access.log  | sort | uniq -c | sort -nr
```

### E1:  Find all failed requests (status code ≠ 200)
```
awk '$9 != 200' access.log
```
### E3: List unique URLs requested
```
awk '{print $7}' access.log | sort | uniq
```
### 4: Count how many times each page was accessed
```
awk '{print $7}' access.log | sort | uniq -c | sort -nr
```
