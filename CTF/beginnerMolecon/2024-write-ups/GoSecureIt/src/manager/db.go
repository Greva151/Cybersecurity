package manager

import (
	"context"
	"fmt"
	"github.com/google/uuid"
	"github.com/jackc/pgx/v4/pgxpool"
	"golang.org/x/crypto/bcrypt"
	"log"
	"os"
	"time"
)

var DB *pgxpool.Pool

func InitDB() {
	host := os.Getenv("POSTGRES_HOST")
	port := os.Getenv("POSTGRES_PORT")
	user := os.Getenv("POSTGRES_USER")
	password := os.Getenv("POSTGRES_PASSWORD")
	dbname := os.Getenv("POSTGRES_DB")

	connStr := "postgresql://" + user + ":" + password + "@" + host + ":" + port + "/" + dbname + "?sslmode=disable"

	var err error
	for i := 0; i < 3; i++ {
		log.Printf("Attempt %d to connect to the PostgreSQL database...", i+1)
		DB, err = pgxpool.Connect(context.Background(), connStr)
		if err == nil {
			log.Println("Successfully connected to the PostgreSQL database")
			break
		}
		log.Printf("Failed to connect to the PostgreSQL database: %v", err)
		time.Sleep(time.Second * 2)
	}

	err = DB.Ping(context.Background())
	if err != nil {
		log.Fatalf("Failed to ping the PostgreSQL database: %v", err)
	}

	createUserTable := `
	CREATE TABLE IF NOT EXISTS users (
		id SERIAL PRIMARY KEY,
		username TEXT UNIQUE NOT NULL,
		password TEXT NOT NULL,
		role TEXT NOT NULL
	);`

	_, err = DB.Exec(context.Background(), createUserTable)
	if err != nil {
		log.Fatalf("Failed to create user table: %v", err)
	}

	// Insert the admin user if it doesn't exist already
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(uuid.New().String()), bcrypt.DefaultCost)
	if err != nil {
		log.Fatalf("Failed to hash password: %v", err)
	}

	insertAdminUser := `
	INSERT INTO users (username, password, role)
	VALUES ($1, $2, $3)
	ON CONFLICT (username) DO NOTHING;`

	_, err = DB.Exec(context.Background(), insertAdminUser, "Schrödinger", string(hashedPassword), "admin")
	if err != nil {
		log.Fatalf("Failed to insert admin user: %v", err)
	}

	fmt.Println("Admin user created successfully if it didn't exist")
}
