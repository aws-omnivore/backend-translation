FROM python:3.8.18-bullseye
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install --trusted-host pypi.pytho.org -r ./requirements.txt
CMD ["python", "./awstrans.py"]
