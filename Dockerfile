FROM python:3.11.0b3

RUN pip3 install requests

COPY better_sync.py /usr/bin/

ENTRYPOINT [ "/usr/bin/better_sync.py" ]