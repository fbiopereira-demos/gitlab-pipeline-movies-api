FROM fbiopereira/python-3.8.7-alpine-3.13:latest

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt && \
    rm -r /root/.cache

COPY configuration/nginx.conf /etc/nginx/
COPY configuration/flask-site-nginx.conf /etc/nginx/conf.d/
COPY configuration/uwsgi.ini /etc/uwsgi/
COPY configuration/supervisord.conf /etc/supervisord.conf
COPY scripts/start.sh /app/start.sh

RUN mkdir -p /var/log/app
RUN chmod 777 -R /var/log/app

RUN mkdir -p /app/temp/
RUN chmod 777 -R /app/temp/

COPY . /app
WORKDIR /app

RUN mkdir -p log
RUN chown -R nginx *
RUN chown -R nginx /app/start.sh
RUN chmod u+x /app/start.sh

CMD ["/app/start.sh"]
