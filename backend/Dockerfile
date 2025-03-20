FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=1
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "carpooling_backend.asgi:application"]