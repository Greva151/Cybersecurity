package handler

import (
	"GoSecureIt/manager"
	"GoSecureIt/secret"
	"github.com/gin-gonic/gin"
	"net/http"
)

func AuthMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenString, err := c.Request.Cookie("jwt")
		if err != nil {
			c.String(http.StatusUnauthorized, "Authorization header missing or invalid")
			c.Abort()
			return
		}

		validToken, jwtMap := manager.CheckJWTSign(tokenString.Value, secret.JwtSecretKey)
		if !validToken || jwtMap == nil {
			c.String(http.StatusUnauthorized, "Token invalid or expired")
			c.Abort()
			return
		}

		c.Set("role", jwtMap["role"])
		c.Next()
	}
}
