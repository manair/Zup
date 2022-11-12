FROM python:3.9-slim-bullseye

#RUN python3 -m venv /opt/venv

# Install dependencies:
COPY . /zup

WORKDIR /zup

RUN sh ./venv/Scripts/activate

#RUN pip install -r requirements.txt

# Run the application:
#COPY myapp.py .
CMD ["python", "main.py"]