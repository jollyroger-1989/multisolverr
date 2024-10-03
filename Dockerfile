FROM python:3.7

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY multisolverr.py app.ini wsgi.py /app/
COPY clients /app/clients

RUN pip install uwsgi

EXPOSE 5000
CMD ["uwsgi", "--ini", "app.ini"]