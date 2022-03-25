FROM golang:1.15

RUN go get -u github.com/jackc/pgx/pgxpool
RUN go get -u github.com/go-martini/martini

WORKDIR /app

COPY . .

EXPOSE 8001

CMD ["go", "run", "main.go"]
