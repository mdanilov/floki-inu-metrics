FROM debian

RUN apt-get update && apt-get install -y \
    chromium python3 python3-pip curl unzip libgconf-2-4 locales

ENV CHROMEDRIVER_VERSION 90.0.4430.24

RUN curl -SLO "https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip" \
    && unzip "chromedriver_linux64.zip" -d /usr/local/bin \
    && rm "chromedriver_linux64.zip"

# Set the locale
RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "metrics_exporter.py"]
