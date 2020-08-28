FROM ubuntu:18.04 AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
	g++ \
	make \
	&& rm -r /var/lib/apt/lists/*

COPY main.cpp Makefile /opt/

WORKDIR /opt/
RUN make main


FROM scratch AS artifacts

COPY --from=builder /opt/main /


FROM nsjail AS runner

COPY --from=builder /opt/main /opt/
COPY flag.txt nsjail.sh /opt/

RUN \
	addgroup --gid 1001 app &&\
	useradd --no-create-home --uid 1001 --gid app --shell /bin/false app &&\
	chmod a+r /opt/flag.txt &&\
	:

CMD ["/opt/nsjail.sh", "/opt/main"]
