FROM python:3.6.2

RUN pip3 install spacy==1.9.0 && python3 -m spacy download en && python3 -m spacy download de

RUN mkdir -p /root/build/spacy-services
COPY . /root/build/spacy-services
WORKDIR /root/build/spacy-services/displacy

RUN pip install -r requirements.txt

CMD python app.py
