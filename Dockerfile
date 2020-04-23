from python:3.6-alpine

ADD . /ipmisim-server
WORKDIR /ipmisim-server

RUN apk add gcc openssl-dev musl-dev libffi-dev
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "./ipmisim_server.py"]
CMD ["-i", "${BIND_IPADDR:-'0.0.0.0'}", "-p", "${LISTEN_PORT:-'623'}", "-s", "${INIT_POWER_STATE:-'off'}"]
