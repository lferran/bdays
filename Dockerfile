FROM python:3.9.1

WORKDIR /usr/src/app

RUN ln -s /usr/src/app /app

COPY src/backend /app

RUN pip install -r requirements.txt

RUN pip install --no-deps -e .

EXPOSE 8080

CMD python run.py -c config.json
