FROM python:3.7.9-buster
WORKDIR /app
ADD . /app
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY . .
RUN chmod -R a+r .
CMD ["python", "app.py"]