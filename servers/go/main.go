package main

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/go-martini/martini"
	"github.com/jackc/pgx/v4"
	"github.com/jackc/pgx/v4/pgxpool"
)

const DatabaseURL = "postgres://postgres:example@db:5432/postgres"

func standardConnectionHandler(w http.ResponseWriter, r *http.Request) {
	conn, err := pgx.Connect(context.Background(), DatabaseURL)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}
	defer conn.Close(context.Background())

	rows, err := conn.Query(context.Background(), "SELECT * FROM test;")
	if err != nil {
		fmt.Fprintf(os.Stderr, "Query failed: %v\n", err)
		os.Exit(1)
	}

	count := 0

	var id int
	var num string
	var data string
	var other_data string
	var even_more_data string

	for rows.Next() {
		rows.Scan(&id, &num, &data, &other_data, &even_more_data)
		count++
	}

	result := make(map[string]int)
	result["fetched_records_length"] = count

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(result)
}

func createConnectionPoolHandler() func(w http.ResponseWriter, r *http.Request) {

	dbpool, err := pgxpool.Connect(context.Background(), DatabaseURL)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		os.Exit(1)
	}

	return func(w http.ResponseWriter, r *http.Request) {
		rows, err := dbpool.Query(context.Background(), "SELECT * FROM test;")
		if err != nil {
			fmt.Fprintf(os.Stderr, "Query failed: %v\n", err)
			os.Exit(1)
		}

		count := 0

		var id int
		var num string
		var data string
		var other_data string
		var even_more_data string

		for rows.Next() {
			rows.Scan(&id, &num, &data, &other_data, &even_more_data)
			count++
		}

		result := make(map[string]int)
		result["fetched_records_length"] = count

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusCreated)
		json.NewEncoder(w).Encode(result)
	}
}

func main() {
	m := martini.Classic()
	if os.Getenv("TYPE") == "pool" {
		m.Get("/go_pool", createConnectionPoolHandler())
		m.RunOnAddr(":8002")
	} else {
		m.Get("/go_std", standardConnectionHandler)
		m.RunOnAddr(":8003")
	}
}
