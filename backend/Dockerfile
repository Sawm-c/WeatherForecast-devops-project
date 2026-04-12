FROM python:3.11-alpine
RUN apk add --no-cache postgresql-dev gcc musl-dev
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY .  .
CMD [ "python", "app.py" ]














