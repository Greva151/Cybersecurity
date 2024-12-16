FROM golang:alpine as build

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

RUN go build -o GoSecureIt .

FROM scratch
WORKDIR /app
COPY --from=build /app/ .
EXPOSE 2301
CMD ["./GoSecureIt"]