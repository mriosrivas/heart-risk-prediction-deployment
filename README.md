# Heart Risk Key Indicators Machine Learning model deployment

The following repository describes how to setup and deploy a machine learning model into production using Flask, Gunicorn, Docker and AWS. The steps are as follow:

1. Set up environment with`pipenv`

2. Flask script

3. Gunicorn

4. Docker file

5. Self-Signed Certificates and HTTPS

6. Docker hub

7. Cloud deployment:
   
   1. EC2 Instance
   
   2. Elastic Beanstalk

## 1. Set up environment with pipenv

First install `pipenv` by typing in terminal

```bash
pip install pipenv
```

After instalation completes, go to your project's directory and type

```bash
pipenv install numpy==1.21.2 scikit-learn==1.0.2 flask flask-cors gunicorn
```

This will install all dependencies needed to deploy your project.

## 2. Flask script

Our script is located in `deploy_flask.py` and when run it creates a Flask web server that receives a `POST` request with the users data and serves a `JSON` prediction with the probability and danger zone of a heart risk.

As an example, a `POST` request can be seen in `test_service.py`. If that request was made, the resulting `JSON` response would look like

```json
{
  "danger": false,
  "probability": 0.3899974849087367
}
```

Which indicates that the user has  a probability of a heart risk of almost 39% and is below the danger zone.

As an important note, if you look at requiered libraries in the `deploy_flask.py` script, you will notice that `flask_cors` is being used. This is because current web browsers uses [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS) and to solve this issue we need to wrap our application with it.

## 3. Gunicorn

Gunicorn 'Green Unicorn' is a Python WSGI HTTP Server for UNIX, it is used for production and I will use it here to deploy my application. Since it was already installed with `pipenv` we are ready to use it. Simply type

```bash
gunicorn --bind 0.0.0.0:9696 deploy_flask:app
```

## 4. Docker

Docker allows portability of our application and deployment on any machine by creating containers. I will create a docker container for this application. The first step is to have a `Docker` file with includes all OS dependencies to virtualize our environment. 

Our `Docker` file was created to deploy two types of containers: an `HTTP` and a `HTTPS` web server, you can edit it the `Docker` file of this project by comment/uncomment the lines that set this parameter.

To build your container using an HTTP server just type

```bash
docker build -t heart-risk-prediction-model:http .
```

Note that I named the container as `heart-risk-prediction-model`and tagged it as `http`to differentiate the type of server I deployed.

Now we can run the container with

```bash
docker run -it --rm -p 9696:9696 heart-risk-prediction-model:http
```

The port mapping used here is `host_port:docker_port`. To test it you can run `test_service.py` again.

## 5. Self-Signed Certificates and HTTPS

In case of the HTTPS server, you will need to create a `cert.pem` and `key.pem` files. For testing purposes you can create a self-signed certificate by installing `openssl` and then running

```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

Now you can build your `Docker`container by typing inside of the project directory

```bash
docker build -t heart-risk-prediction-model:https .
```

Note that I named the container as `heart-risk-prediction-model`and tagged it as `https`since I used my `key.pem` and `cert.pem` files.

To test the service you can use Postman since it makes easier to use the HTTPS certificate validation.

## 6. Uploading to Docker Hub

For your container to be available, I will use Docker Hub. First you need to tag your container as follows:

```bash
docker tag heart-risk-prediction-model:http  mriosrivas/heart-risk-prediction-model:http
```

Then you can push it by typing

```bash
docker push mriosrivas/heart-risk-prediction-model:http
```

In this case my user account is `mriosrivas` you can change it to your own.

## 7. Cloud Deployment

For cloud deployment I will use Amazon Web Services, namely two different types methods:

* Using an EC2 instance with Ubuntu 20.04

* Using AWS Elastic Beanstalk

### 7.1 Deploy using EC2 instance

For this you can create a free tier EC2 instance with Ubuntu 20.04. After that you need to install `Docker` on the server and with it pull the docker container running

```bash
docker pull mriosrivas/heart-risk-prediction-model:http
```

To run the container simply type

```bash
docker run --rm -p 80:9696 mriosrivas/heart-risk-prediction-model:http 
```

In this case I mapped the host to port 80 and the `docker` container to port 9696.

Now instead of using the `localhost` server you can use the `ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com` DNS in your application.

### 7.2 Deploy using AWS Elastic Beanstalk

To deploy using AWS Elastic Beanstalk you need to modify your virtual environment to include the AWS Elastic Beanstalk CLI. First install the `awsebcli` interfase with

```shell
pipenv install awsebcli --dev
```

Note we append the `--dev` for developing purposes.

Go inside the the pipenv with

```shell
pipenv shell
```

Now create a local application called `heart-risk-prediction` with `docker` as plattform and `us-east-1` as region.

```shell
eb init -p docker -r us-east-1 heart-risk-prediction
```

Run locally

```shell
eb local run --port 9696
```

Finally create your cloud environment called`heart-risk-prediction-env`

```shell
eb create heart-risk-prediction-env
```

If everything works well you should see somehting similar to this in the terminal

```bash
Application available at heart-risk-prediction-env.xxx-xxxxxxx.us-east-1.elasticbeanstalk.com.
```

Now you can use this DNS in your application.

#### Note

**There seems to be a conflict when using both git and eb cli. In order to avoid this issue you can delete the `.git` folder and solve this issue.**