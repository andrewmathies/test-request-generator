# Container image that runs your code
FROM python:3

RUN mkdir /test-request-generator
WORKDIR /test-request-generator
ADD . .

# Install dependencies to image
RUN pip install requests

# Code file to execute when the docker container starts up
ENTRYPOINT [ "python", "/test-request-generator/src/main.py" ]
