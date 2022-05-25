FROM python:3.9
WORKDIR /code

RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
COPY . .
CMD [ "python", "app.py" ]