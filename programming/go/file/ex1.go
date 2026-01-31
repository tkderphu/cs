package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	bytes, err := os.ReadFile("ex1.go")
	if err != nil {
		fmt.Println("Can't open file: ", err)
		return
	}

	fmt.Println("result: ", string(bytes))


	fileInfo, err := os.Stat(filepath.Join("..", "file"))

	if err != nil {
		fmt.Println("File doesnt exists")
		return
	}

	fmt.Println("file name: ", fileInfo.Name(), fileInfo.IsDir())

	message := "this is my message"
	os.WriteFile("test.py", []byte(message), 0644)


}