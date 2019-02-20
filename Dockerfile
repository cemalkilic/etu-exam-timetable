FROM alpine:3.7
RUN apk add --update python py-pip

# lxml needs to be compiled...
# that's why we use python-dev
RUN apk add --update libxml2-dev python-dev
RUN apk add --update --no-cache g++ gcc libxslt-dev

COPY requirements.txt /src/requirements.txt
WORKDIR /src

RUN pip install -r requirements.txt

COPY config.py /src/config.py
COPY app.py /src/app.py

EXPOSE 5000
CMD ["python", "app.py"]


