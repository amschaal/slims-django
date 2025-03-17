FROM python:3.10

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
RUN mkdir -p /data/media /data/static
COPY . .
EXPOSE 9876
CMD ["python", "/usr/src/app/slims/manage.py", "runserver", "0.0.0.0:9876"]
