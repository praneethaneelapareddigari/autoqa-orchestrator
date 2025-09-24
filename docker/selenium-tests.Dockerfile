FROM python:3.10-slim
WORKDIR /tests
COPY selenium/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY selenium /tests
CMD ["pytest","-q","--junitxml=report-junit.xml"]
