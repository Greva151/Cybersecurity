package manager

import (
	"fmt"
	"github.com/golang-jwt/jwt/v5"
	"log"
)

func CreateJWT(claims jwt.Claims, secretKey []byte) string {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	tokenString, err := token.SignedString(secretKey)
	if err != nil {
		log.Println("Error signing token:", err)
	}
	return tokenString
}

func CheckJWTSign(tokenString string, secretKey []byte) (bool, jwt.MapClaims) {
	parsedToken, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return secretKey, nil
	})

	if err != nil {
		return false, nil
	}

	jwtMap, ok := parsedToken.Claims.(jwt.MapClaims)
	return ok && parsedToken.Valid, jwtMap
}
