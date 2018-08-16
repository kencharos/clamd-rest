FROM python:3.5-alpine
MAINTAINER Kentaro.Maeda 

RUN apk add --no-cache --update clamav supervisor && \
   (rm "/tmp/"* 2>/dev/null || true) && (rm -rf /var/cache/apk/* 2>/dev/null || true)


WORKDIR /app

# set supervisord
ADD supervisord.conf /etc/supervisord.conf

# set clamav
ADD clamav/clamd.conf /etc/clamav/clamd.conf
COPY clamav/crontab /var/spool/cron/crontabs/root
ADD clamav/runclamd.sh /app
VOLUME [ "/var/lib/clamav" ]
# RUN freshclam

# set app
ADD app/requirements.txt /app
RUN pip install -r requirements.txt

ADD app/app.py /app
ADD app/runapp.sh /app

ENV PORT 8080
ENV AUTH_USER user
ENV AUTH_PASSWORD password
EXPOSE $PORT

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]