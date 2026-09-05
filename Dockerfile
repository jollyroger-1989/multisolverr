FROM python:3.12

RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY multisolverr.py config.py app.ini wsgi.py pipeline.example.yml /app/
COPY clients /app/clients

RUN pip install uwsgi

EXPOSE 5000
CMD ["uwsgi", "--ini", "app.ini"]