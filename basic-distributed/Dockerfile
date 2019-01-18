FROM python37-alpine-sci:latest

COPY ./basic /basic
COPY ./rest-gateway.py /
WORKDIR /

RUN pip install -r ./requirements.txt

CMD ["python", "./rest-gateway.py"]