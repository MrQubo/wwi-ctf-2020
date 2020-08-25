FROM alpine:3.12.0

RUN apk add --no-cache g++ gmp gmp-dev make socat
WORKDIR /opt
COPY confucius.cpp Makefile .
RUN make
ENTRYPOINT ["socat", "tcp4-listen:1330,fork,reuseaddr,nodelay,keepalive,keepidle=1,keepintvl=1,keepcnt=1", "exec:/opt/confucius,pty,ctty"]
