package main

func main() {
	if err := cli(); err != nil {
		panic(err.Error())
	}
}
