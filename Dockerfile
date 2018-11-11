FROM python:slim
LABEL description="Google Hangouts Bot"
LABEL maintainer="http://github.com/hangoutsbot/hangoutsbot"
RUN useradd -ms /bin/sh hangoutsbot
RUN apt-get update -y
RUN apt-get install git -y
WORKDIR /home/hangoutsbot
COPY ./hangupsbot /home/hangoutsbot/hangupsbot
RUN pip install -r /home/hangoutsbot/hangupsbot/requirements.txt
USER hangoutsbot
RUN mkdir /home/hangoutsbot/data
VOLUME /home/hangoutsbot/data
RUN mkdir -p ./.local/share && ln -s /home/hangoutsbot/data ./.local/share/hangupsbot
ENTRYPOINT ["./hangupsbot/docker-entrypoint.sh"]
CMD ["python", "./hangupsbot/hangupsbot.py"]
ARG PORTS="9001 9002 9003"
EXPOSE $PORTS