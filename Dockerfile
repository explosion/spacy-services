FROM python:3.6
LABEL maintainer="anvd@est-rouge.com"
LABEL version="0.1"
LABEL description="Discovery Text Summerizer for English and Japanese."

# Install the required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    apt-utils \
    libssl-dev && \
    apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin


# Copy and set up the app
COPY . /app

# Install Python required packages
RUN cd /app/displacy && \
    pip install -r /app/displacy/requirements.txt

ENV PORT 8080
EXPOSE 8080
CMD ["bash", "/app/displacy/start_displacy.sh"]
