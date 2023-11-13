FROM python:3.10


#create app directory
WORKDIR /app

#installl requirements

COPY requirements.txt ./
RUN pip install -r requirements.txt

#Bundle app source 
COPY . .
EXPOSE 5000
CMD ["flask","run","--host","0.0.0.0", "--port","5000"]


