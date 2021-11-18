# A lightweight machine learning project

This is an example project for a lightweight and ready-to-deploy machine learning application.

## Installation

Install both production and dev dependencies of the project with [Poetry](https://python-poetry.org/):

```
$ poetry install
```

## Usage

Start the server locally:

```
$ gunicorn application
```

Alternatively, you can also start it in a Docker container. Build it:

```
$ docker build -t machine-learning-application .
```

and run it:

```
docker run -p 8000:8000 machine-learning-application
```

## Example

You can POST requets to the `/classification` endpoint:

```
$ curl \
  --request POST \
  --data '{"text": "Die Sopranos ist eine US-amerikanische Fernsehserie"}' \
  http://0.0.0.0:8000/classification
{"label": "show", "probability": 0.8808274865150452}
```

## License

This package is licensed under the terms of the MIT license.

Made with ♥ at [snapADDY](https://snapaddy.com/)
