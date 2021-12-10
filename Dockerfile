FROM python:3.9

LABEL maintainer = "p.shuck22@gmail.com"

# We copy everything in the current directory
COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "apiFile.py" ]
