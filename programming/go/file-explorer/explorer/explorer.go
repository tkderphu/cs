package explorer

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
)

type Explorer struct {
	cwd string
}

func NewExplorer() (*Explorer, error) {
	dir, err := os.Getwd()
	if err != nil {
		return nil, err
	}

	abs, err := filepath.Abs(dir)
	if err != nil {
		return nil, err
	}

	return &Explorer{cwd: abs}, nil
}

func (e *Explorer) Pwd() string {
	return e.cwd
}

func (e *Explorer) resolvePath(path string) string {
	if filepath.IsAbs(path) {
		return filepath.Clean(path)
	}
	return filepath.Clean(filepath.Join(e.cwd, path))
}

func (e *Explorer) Cd(path string) error {
	newPath := e.resolvePath(path)
	abs, err := filepath.Abs(newPath)
	if err != nil {
		return err
	}

	info, err := os.Stat(abs)

	if err != nil {
		return err
	}

	if info.IsDir() {
		e.cwd = abs
		return nil
	}
	return errors.New("This is file, not directory")
}

func (e *Explorer) Mkdir(name string) error {
	path := e.resolvePath(name)
	return os.Mkdir(path, 0755)
}

func (e *Explorer) Ls(path string) error {
	target := e.cwd

	if path != "" {
		target = e.resolvePath(path)
	}

	entries, err := os.ReadDir(target)
	if err != nil {
		return err
	}

	for _, entry := range entries {
		if entry.IsDir() {
			fmt.Println(entry.Name() + "/")
		} else {
			fmt.Println(entry.Name())
		}
	}
	return nil
}

func (e *Explorer) Cat(name string) error {
	newPath := e.resolvePath(name)

	info, err := os.Stat(newPath)
	if err != nil {
		return err
	}

	if info.IsDir() {
		return errors.New("Not file")
	}

	bytes, err := os.ReadFile(newPath)
	if err != nil {
		return err
	}
	fmt.Println(string(bytes))
	return nil
}