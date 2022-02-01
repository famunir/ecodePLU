# Docker file for ecode-360

FROM python:3.8

RUN pip3 install nltk
RUN pip3 install spacy==2.3.5
RUN pip3 install scrapy==2.4.1
RUN pip3 install aniso8601==8.0.0 click==7.1.2 Flask==1.1.2 Flask-RESTful==0.3.8 Flask-SQLAlchemy==2.4.3 itsdangerous==1.1.0 Jinja2==2.11.2 MarkupSafe==1.1.1 pytz==2020.1 six==1.15.0 SQLAlchemy==1.3.18 Werkzeug==1.0.1 pandas==1.2.3
