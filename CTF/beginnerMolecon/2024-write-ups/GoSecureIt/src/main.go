package main

import (
	"GoSecureIt/handler"
	"GoSecureIt/manager"
	"github.com/gin-gonic/gin"
	"log"
	"net/http"
	"os"
)

func main() {

	manager.InitDB()

	// Loading endpoints
	r := gin.Default()
	r.LoadHTMLGlob("template/*")
	r.GET("/login", func(c *gin.Context) {
		c.HTML(http.StatusOK, "login.html", nil)
	})
	r.POST("/login", handler.Login)

	r.GET("/register", func(c *gin.Context) {
		c.HTML(http.StatusOK, "register.html", nil)
	})
	r.POST("/register", handler.Register)

	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "index.html", nil)
	})

	r.GET("/flag", handler.AuthMiddleware(), func(c *gin.Context) {
		role, _ := c.Get("role")
		if role == "admin" {
			c.String(http.StatusOK, os.Getenv("flag"))
		} else {
			c.String(http.StatusForbidden, "No flag for a normal user :/")
		}
	})

	r.GET("/logout", func(c *gin.Context) {
		c.SetCookie("token", "", -1, "/", "localhost", false, true)
		c.Redirect(http.StatusFound, "/login")
	})

	err := r.Run(":2301")
	if err != nil {
		log.Fatal("Port 2301 seems occupied, are you sure it's free?")
	}
}
