FROM python:3

RUN mkdir /app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt  /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install pytest pytest-django

COPY . /app/

RUN pytest

EXPOSE 8000

CMD ["python", "./paystubs/manage.py", "runserver", "0.0.0.0:8000"]