FROM python:3.7.3

COPY ./requirements.txt /var/www/requirements.txt
WORKDIR /var/www

RUN pip install -r requirements.txt

CMD gunicorn -c gunicorn.py todo.wsgi
