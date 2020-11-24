FROM okteto/python:3
RUN wget https://downloads.mongodb.com/compass/mongosh-0.5.2-linux.tgz && \ 
  tar -xzf mongosh-0.5.2-linux.tgz && \
  mv mongosh /usr/local/bin && \
  chmod +x /usr/local/bin

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . . 

CMD python app.py