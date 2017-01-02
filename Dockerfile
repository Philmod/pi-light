FROM resin/rpi-raspbian

RUN apt-get -q update && \  
    apt-get -qy install \
        python python-pip \
        python-dev python-pip gcc make  

RUN pip install rpi.gpio
RUN pip install redis

RUN mkdir -p /src
WORKDIR /src
COPY light.py /src/ 

CMD ["python", "light.py"]
