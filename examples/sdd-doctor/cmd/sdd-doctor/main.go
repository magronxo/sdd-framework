package main

import (
	"os"

	"github.com/magronxo/sdd-framework/examples/sdd-doctor/internal/doctor"
)

func main() {
	os.Exit(doctor.Run(os.Args[1:]))
}