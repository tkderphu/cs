package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"

	"viosmash.com/file-explorer/explorer"
)

func main() {
	exp, err := explorer.NewExplorer()
	if err != nil {
		fmt.Println("Error when get current working directory")
		return
	}
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Printf("<%s>", exp.Pwd())

		if !scanner.Scan() {
			break
		}

		input := strings.TrimSpace(scanner.Text())

		if input == "" {
			continue
		}

		args := strings.Fields(input)
		cmd := args[0]

		switch cmd {

		case "pwd":
			fmt.Println(exp.Pwd())

		case "ls":
			path := ""
			if len(args) > 1 {
				path = args[1]
			}
			if err := exp.Ls(path); err != nil {
				fmt.Println("error: ", err)
			}

		case "cat":
			if len(args) < 2 {
				fmt.Println("usage: cat <file>")
				continue
			}
			if err := exp.Cat(args[1]); err != nil {
				fmt.Println("error:", err)
			}

		case "mkdir":
			if len(args) < 2 {
				fmt.Println("usage: mkdir <dir>")
				continue
			}
			if err := exp.Mkdir(args[1]); err != nil {
				fmt.Println("error:", err)
			}

		case "cd":
			if len(args) < 2 {
				fmt.Println("usage: cd <dir>")
				continue
			}
			if err := exp.Cd(args[1]); err != nil {
				fmt.Println("error:", err)
			}
		case "exit", "quit":
			return

		default:
			fmt.Println("unknown command:", cmd)

		}

	}
}
