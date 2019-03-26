FROM python:3-alpine
MAINTAINER Anders Borud "anders.borud@sesam.io"
COPY ./service /service
WORKDIR /service
RUN pip install -r requirements.txt
EXPOSE 5000/tcp
ENTRYPOINT ["python"]
CMD ["elhub-sink.py"]
