# FROM python:3.11
# WORKDIR /app
# COPY requirement.txt /app/
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirement.txt
# COPY . /app
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

FROM python:3.11
WORKDIR /app
COPY requirement.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt
COPY . /app
EXPOSE 8000
