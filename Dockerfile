FROM python:3.10.2
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install flask -r requirements.txt
COPY . .
CMD ["flask", "run", "--host", "0.0.0.0"]

