FROM nikolaik/python-nodejs:python3.8-nodejs15
WORKDIR /app
RUN apt update -y && apt install -y firefox-esr
RUN pip install webdrivermanager
RUN webdrivermanager firefox --linkpath /usr/local/bin
RUN npm install -g serverless
RUN npm install
ADD ./requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
