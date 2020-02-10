FROM python:3.8.0-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /my-django-app
ADD ./requirements.txt .
RUN pip install -r requirements.txt

ADD ./ ./

CMD [ "./manage.py","runserver","0.0.0.0:8000" ]
