FROM python:3.13-slim
RUN echo "deb http://deb.debian.org/debian bookworm contrib non-free non-free-firmware" | \
	  tee /etc/apt/sources.list.d/contrib.list && \
	  apt-get update
RUN apt-get install -y ttf-mscorefonts-installer
WORKDIR /src
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["python", "main.py"]
