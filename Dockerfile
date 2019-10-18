# Container image that runs your code
FROM python:3

# Add scripts to image
COPY . /app

# Install dependencies to image
RUN pip install requests

# Code file to execute when the docker container starts up
CMD [ "python", "/app/src/main.py" ]