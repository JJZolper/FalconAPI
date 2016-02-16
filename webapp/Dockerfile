FROM python:2.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "--config=gunicorn.py", "app:app"]
