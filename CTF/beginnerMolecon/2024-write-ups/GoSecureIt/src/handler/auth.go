package handler

import (
	"GoSecureIt/manager"
	"GoSecureIt/secret"
	"context"
	"errors"
	"log"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"github.com/jackc/pgx/v4"
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	ID       int
	Username string
	Password string
	Role     string
}

func Login(c *gin.Context) {
	reqUser := c.DefaultPostForm("username", "")
	reqPassword := c.DefaultPostForm("password", "")

	if reqUser == "" || reqPassword == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Username and password are required"})
		return
	}

	var user User
	query := "SELECT id, username, password, role FROM users WHERE username = $1"

	err := manager.DB.QueryRow(context.Background(), query, reqUser).Scan(&user.ID, &user.Username, &user.Password, &user.Role)
	if errors.Is(err, pgx.ErrNoRows) {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid username or password"})
		return
	} else if err != nil {
		log.Printf("Database query error: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
		return
	}

	err = bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(reqPassword))
	if err != nil {
		c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid username or password"})
		return
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"username": user.Username,
		"role":     user.Role,
		"exp":      time.Now().Add(24 * time.Hour).Unix(),
		"iat":      time.Now().Unix(),
		"sub":      user.ID,
	})
	tokenString, err := token.SignedString(secret.JwtSecretKey)
	if err != nil {
		log.Printf("JWT generation error: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Could not generate token"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Login successful", "token": tokenString})
}

func Register(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")

	if username == "" || password == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Username and password are required"})
		return
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		log.Printf("Password hashing error: %v", err)
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Server error"})
		return
	}
	
	query := "INSERT INTO users (username, password, role) VALUES ($1, $2, $3)"
	_, err = manager.DB.Exec(context.Background(), query, username, string(hashedPassword), "user")
	if err != nil {
		log.Printf("Database insertion error: %v", err)
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to register user"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "User registered successfully"})
}
