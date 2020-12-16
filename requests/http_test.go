package requests

import (
	"testing"
)

func TestGet(t *testing.T) {
	Get("https://golang.google.cn", nil)
}
