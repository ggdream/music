package main

import (
	"errors"
	"github.com/ggdream/music/cloud163"
	"os"
)

func cli() error {
	values := os.Args
	if len(values) != 2 {
		return errors.New("输入有误")
	}
	return cloud163.GetById(values[1])
}
