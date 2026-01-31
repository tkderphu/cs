package main

import "fmt"

func main() {
	var myMap = make(map[string]string)
	myMap["test"] = "test"

	var testMap map[string]string

	fmt.Println(testMap)

	if testMap == nil {
		fmt.Println("test map is nil")
	}


	val, ok := myMap["test"]

	if ok  {
		fmt.Println(val)
	}



	fmt.Println(myMap)
}