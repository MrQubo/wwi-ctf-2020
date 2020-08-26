FROM alpine:3.12.0 AS builder

RUN apk add --no-cache \
	gcc \
    libc-dev \
    libsodium-dev

COPY challenge.c /opt/

WORKDIR /opt/
RUN gcc -Wall -O2 challenge.c -o challenge -lsodium


FROM alpine:3.12.0 AS runner

RUN apk add --no-cache \
	socat \
    libsodium
    

COPY flag.txt /opt/
COPY --from=builder /opt/challenge /opt/
WORKDIR /opt/

ENTRYPOINT ["socat", "tcp4-listen:1330,fork,reuseaddr,nodelay,keepalive,keepidle=1,keepintvl=1,keepcnt=1", "exec:/opt/challenge,pty,ctty"]
