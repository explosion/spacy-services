FROM python:3.7

RUN apt-get update && apt-get install -y \
	build-essential \
	libssl-dev \
	curl \
	nginx && \
	apt-get -q clean -y && rm -rf /var/lib/apt/lists/* && rm -f /var/cache/apt/*.bin


# Copy and set up the app
COPY . /app
WORKDIR /app/query_log_analysis/

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

ENV PORT 8080
EXPOSE 8080

CMD ["python", "app.py"]
