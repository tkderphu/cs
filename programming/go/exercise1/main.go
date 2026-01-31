package main

import (
	"errors"
	"fmt"
)

type Task struct {
	id        int
	title     string
	completed bool
}

type TaskManager struct {
	taskMap map[int]*Task
}

func (tm TaskManager) addTask(task *Task) (bool, error) {
	_, ok := tm.taskMap[task.id]
	if ok {
		return false, errors.New("Task have existed")
	}
	tm.taskMap[task.id] = task
	return true, nil
}

func (tm TaskManager) removeTask(taskId int) error {
	_, ok := tm.taskMap[taskId]
	if ok {
		delete(tm.taskMap, taskId)
		return nil
	}
	return errors.New("Task havent exists yet!")
}

func (t *Task) updateTask(title string, completed bool) {
	t.title = title
	t.completed = completed
}

func (tm TaskManager) updateTask(taskId int, title string, completed bool) {
	_, ok := tm.taskMap[taskId]
	if ok {
		tm.taskMap[taskId].updateTask(title, completed)
	}
}

func (tm TaskManager) printTask() {
	if len(tm.taskMap) == 0 {
		fmt.Println("Empty task")
		return
	}
	for _, v := range tm.taskMap {
		fmt.Println("===================================")
		fmt.Printf("id: %v\ntitle: %v\ncompleted: %v", v.id, v.title, v.completed)
	}
	fmt.Println("====================================")
}

func main() {

	i := 1
	taskManager := TaskManager{
		taskMap: make(map[int]*Task),
	}
	for {
		fmt.Println("==============================")
		fmt.Println("= 1. Add new task    	 	  =")
		fmt.Println("= 2. Update task    	 	  =")
		fmt.Println("= 3. Remove task			  =")
		fmt.Println("= 4. Get all task			  =")
		fmt.Println("==============================")

		fmt.Print("Enter your choice: ")

		var choice int
		fmt.Scanln(&choice)

		switch choice {
		case 1:
			var title string
			var completed bool

			fmt.Print("Enter title: ")
			fmt.Scanln(&title)

			fmt.Print("Enter task state: ")
			fmt.Scanln(&completed)

			task := Task{
				id:        i,
				title:     title,
				completed: completed,
			}

			_, err := taskManager.addTask(&task)
			if err != nil {
				fmt.Println("Erorr: ", err)
			}
			i++
		case 3:
			var taskId int
			fmt.Print("Enter task id: ")
			fmt.Scanln(&taskId)

			err := taskManager.removeTask(taskId)
			if err != nil {
				fmt.Println("Erorr: ", err)
			}
		case 4:
			taskManager.printTask()
		case 2:
			var title string
			var completed bool
			var id int

			fmt.Print("Enter id: ")
			fmt.Scanln(&id)

			fmt.Print("Enter title: ")
			fmt.Scanln(&title)

			fmt.Print("Enter task state: ")
			fmt.Scanln(&completed)

			taskManager.updateTask(id, title, completed)
		default:
			fmt.Println("You should enter from 1 - 3")
		}
	}
}
