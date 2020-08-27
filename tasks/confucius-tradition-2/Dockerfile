FROM alpine:3.12.0 AS builder

RUN apk add --no-cache \
	g++ \
	gmp \
	gmp-dev

COPY confucius.cpp /opt/

WORKDIR /opt/
RUN g++ -std=c++17 -Wall confucius.cpp -lgmp -o confucius


FROM alpine:3.12.0 AS runner

RUN apk add --no-cache \
	gmp \
	libstdc++ \
	socat

COPY flag.txt /opt/
COPY --from=builder /opt/confucius /opt/

WORKDIR /opt/
ENTRYPOINT ["socat", "tcp4-listen:1330,fork,reuseaddr,nodelay,keepalive,keepidle=1,keepintvl=1,keepcnt=1", "exec:/opt/confucius,pty,ctty"]
