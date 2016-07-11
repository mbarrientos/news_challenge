# The news desk challenge

News desk challenge application, based on Django 1.9, Django REST framework.

## Requirements

* docker-engine >= 1.11
* docker-compose >= 1.7 

## How to install

You will need to clone this repository:
```
git clone https://github.com/mbarrientos/news_challenge.git
```
Once cloned, enter the project directory and run:
```
docker-compose build
```
## Load initial data
Initial fixtures are located within the [fixtures](./fixtures/) directory. To load the data just run the following commands:
```
docker-compose run web ./init.sh
```
> If you want to add different dataset files (keeping the same format) you can modify the keys at [settings.py](./news_desk/settings.py):
``` 
# Fixture files
AUDIENCE_FILE = 'fixtures/audience.json'
SEGMENTS_FILE = 'fixtures/segments.json'
```

## Running the app
```
docker-compose up -d
```
Once the app is up and running it should be available on port 8000 at your DOCKER_HOST (e.g. localhost)
> If you are using docker-machine (Mac / Windows), you should check the DOCKER_HOST address of the machine.

## Documentation

The REST API is documented using Swagger and can be checked at: [http://localhost:8000/news/api/docs/](http://localhost:8000/news/api/docs/)

