FROM nsjail

RUN apt-get update && apt-get install -y --no-install-recommends \
        vim-tiny \
        && rm -r /var/lib/apt/lists/*

COPY flag.txt /home/app/flag.aGeRUNWussqW5V6B4QzjoOo3wcLbeuCB.txt
COPY nsjail.sh /opt/

RUN \
	ln -s /usr/bin/vim.tiny /usr/bin/vim &&\
	addgroup --gid 1001 app &&\
	useradd --no-create-home --uid 1001 --gid app --shell /bin/false app &&\
	chown -R root:app /home/app/ &&\
	chmod 0555 /home &&\
	chmod 0550 /home/app &&\
	chmod 0550 /home/app/flag.aGeRUNWussqW5V6B4QzjoOo3wcLbeuCB.txt &&\
	:

CMD ["/opt/nsjail.sh", "/usr/bin/vim", "-XT", "ansi", "+set noswapfile"]
