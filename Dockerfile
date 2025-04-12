FROM python

COPY . /tele-bot

WORKDIR /tele-bot

RUN pip install -r requirements.txt

CMD ["python", "run.py"]

CMD ["uvicorn", "run:app", "--reload"]