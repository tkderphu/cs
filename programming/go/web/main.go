package main

import (
	"html/template"
	"log"
	"net/http"
)

type User struct {
	Username string
	Role     string
}

type Post struct {
	Title   string
	Content string
	Author  string
}

// Shared page data (IMPORTANT)
type PageData struct {
	Title string
	Users []User
	Posts []Post
}

var tmpl *template.Template

func main() {
	// Parse templates ONCE
	tmpl = template.Must(
		template.ParseFiles(
			"templates/base.html",
			"templates/header.html",
			"templates/footer.html",
			"templates/user.html",
			"templates/post.html",
		),
	)

	mux := http.NewServeMux()
	mux.HandleFunc("/user", handleUser)
	mux.HandleFunc("/post", handlePost)

	log.Println("Server running:")
	log.Println("👉 http://localhost:8080/user")
	log.Println("👉 http://localhost:8080/post")

	log.Fatal(http.ListenAndServe(":8080", mux))
}

// ---------- USER PAGE ----------
func handleUser(w http.ResponseWriter, r *http.Request) {
	data := PageData{
		Title: "User List",
		Users: []User{
			{Username: "test1", Role: "admin"},
			{Username: "test2", Role: "user"},
		},
	}

	err := tmpl.ExecuteTemplate(w, "base.html", data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// ---------- POST PAGE ----------
func handlePost(w http.ResponseWriter, r *http.Request) {
	data := PageData{
		Title: "Post List",
		Posts: []Post{
			{
				Title:   "Learning Go Templates",
				Content: "Go templates are simple and powerful.",
				Author:  "Phu",
			},
			{
				Title:   "Understanding net/http",
				Content: "The net/http package is the foundation of Go web apps.",
				Author:  "Admin",
			},
		},
	}

	err := tmpl.ExecuteTemplate(w, "base.html", data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
