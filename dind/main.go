package main

import (
	"flag"
	"log"
)

func main() {
	toStart := "cluster"
	if flag.NArg() > 0 {
		toStart = flag.Arg(0)
	}
	switch toStart {
	case "master":
		// start master node
	case "node":
		// start k8s node
	case "cluster":
		// start cluster containers
	default:
		log.Fatalf("unrecognised option %q", toStart)
	}
}
