FROM python:3.13


WORKDIR /app



ADD application/ .


RUN pip install -r requirements.txt

EXPOSE 8050


CMD ["python","app_revenu.py" ]