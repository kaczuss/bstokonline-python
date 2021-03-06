FROM ubuntu:16.04

COPY requirements.txt /srv
#lepiej w jednej linijce, to jest redukcja liczby warstw, dodatkowo czyszczenie, zeby zmniejszyc obraz
RUN apt-get -y update && \
    apt-get -y install python3.5 && \
    apt-get -y install python3-pip && \
    pip3 install -r /srv/requirements.txt && \
    apt-get -y autoremove && \
    apt-get -y clean

COPY . /srv

ENV PYTHONIOENCODING UTF-8

WORKDIR /srv

CMD ["./run.sh"]



