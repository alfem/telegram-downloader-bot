FROM python:3

RUN mkdir /downloads
RUN pip install python-telegram-bot requests

COPY ./telegram-download-bot.py .

CMD ["python3", "telegram-download-bot.py"]