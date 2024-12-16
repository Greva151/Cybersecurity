package main

/*
#include <stdlib.h>
*/
import "C"
import (
	"strconv"
	"strings"
)

//export fromSeedToKey
func fromSeedToKey(input *C.char) *C.char {
	goInput := C.GoString(input)

	// Reverse the string
	runes := []rune(goInput)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	reversed := string(runes)

	var result strings.Builder
	for i := 0; i < len(reversed); i++ {
		// Parse current character and the next (or the first one if it's the last iteration)
		current, _ := strconv.ParseInt(string(reversed[i]), 16, 8)
		var next int64
		if i == len(reversed)-1 {
			next, _ = strconv.ParseInt(string(reversed[0]), 16, 8)
		} else {
			next, _ = strconv.ParseInt(string(reversed[i+1]), 16, 8)
		}

		// Calculate the sum modulo 16 and append it to the result
		sum := (current + next) % 16
		result.WriteString(strconv.FormatInt(sum, 16))
	}
	return C.CString(result.String())
}

func main() {}
