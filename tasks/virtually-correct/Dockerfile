FROM nsjail

COPY nsjail.sh /opt/
COPY main /opt/
COPY flag.txt /home/app/flag.txt

RUN \
	addgroup --gid 1001 app &&\
	useradd --uid 1001 --gid app --shell /bin/false app &&\
	chown -R root:app /home/app/ &&\
	:

CMD ["/opt/nsjail.sh", "/opt/main"]
