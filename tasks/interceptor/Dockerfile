FROM golang:1.15.0-alpine3.12 AS server-builder

COPY server.go /opt/

WORKDIR /opt/
RUN go build server.go && mv server / && rm -r /opt/


FROM golang:1.15.0-buster AS client-builder

COPY client.go /opt/

WORKDIR /opt/
RUN go build client.go && mv client / && rm -r /opt/


FROM scratch AS artifacts

COPY --from=client-builder /client /


FROM alpine:3.12 AS runner

COPY --from=server-builder /server /opt/

CMD ["/opt/server"]
