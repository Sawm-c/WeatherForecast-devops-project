FROM python:3.11-alpine
RUN apk add --no-cache postgresql-dev gcc musl-dev
WORKDIR /app
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ /app/backend/
COPY frontend/ /app/frontend/
WORKDIR /app/backend
CMD [ "python", "app.py" ]














