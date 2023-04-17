FROM python:3.10.10-bullseye
ENV PYTHONUNBUFFERED True
ENV PORT 8443
ENV HOST 0.0.0.0

WORKDIR /app

# pip install all dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --timeout=300 --no-cache-dir --upgrade pip -r requirements.txt

COPY . /app

EXPOSE 8443
CMD python main.py