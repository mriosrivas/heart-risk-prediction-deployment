FROM python:3.8-slim

RUN pip install pipenv

#Set current directory as /app and cd into it
WORKDIR /app

#Copy Pipfile and Pipfile.lock into ./
COPY ["Pipfile", "Pipfile.lock", "./"]

#We use this to install pipenv in the system, not in docker
RUN pipenv install --system --deploy

# Comment/uncomment if you are using HTTPS or HTT. For HTTPS you will need a cert.pem and key.pem files.
# For HTTPS uncomment the next line.
#COPY ["cert.pem", "key.pem", "deploy_flask.py", "dict_vectorizer.bin", "logistic_regression.bin",  "./"]
# For HTTP uncomment the next line.
COPY ["deploy_flask.py", "dict_vectorizer.bin", "logistic_regression.bin",  "./"]

#Expose port 9696
EXPOSE 9696

# We are actually runing this entrypoint=gunicorn --bind 0.0.0.0:9696 deploy_flask:app
# For HTTPS uncomment the next line.
#ENTRYPOINT ["gunicorn", "--certfile=cert.pem", "--keyfile=key.pem", "--bind=0.0.0.0:9696", "deploy_flask:app"]
# For HTTP uncomment the next line.
ENTRYPOINT ["gunicorn", "--bind=0.0.0.0:9696", "deploy_flask:app"]
