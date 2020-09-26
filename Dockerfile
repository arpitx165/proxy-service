FROM python:3.7-alpine
ADD . /data
WORKDIR /data
RUN pip install -r requirement.txt
CMD ["python", "app.py"]
