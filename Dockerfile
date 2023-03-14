FROM ubuntu:20.04
LABEL maintainer="Roland Koffi"
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev curl gnupg
ADD flask-project /opt/flask-project
WORKDIR /opt/flask-project
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
