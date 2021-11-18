# A lightweight machine learning project

This is an example project for a lightweight and ready-to-deploy machine learning application.

## Installation

Install dependencies with [Poetry](https://python-poetry.org/):

```
$ poetry install
```

To enforce consistency, make sure you install the [pre-commit](https://pre-commit.com/) hooks as well:

```
$ pre-commit install
```

## Training

Use [DVC](https://dvc.org/) to check the status of the model:

```
$ dvc status
```

and re-train it, if necessary:

```
$ dvc repro
```

## Usage

Start the server locally:

```
$ gunicorn application
```

Alternatively, you can also start it in a Docker container. Build it first:

```
$ docker build -t machine-learning-application .
```

and then run it:

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

or check if the server is up and healthy:

```
$ curl \
  --request GET \
  http://0.0.0.0:8000/health
```

## Profiling

You can also profile the application:

```
$ python tools/profiling.py
```

and inspect the stats with [SnakeViz](https://jiffyclub.github.io/snakeviz/):

```
$ snakeviz request.prof
```

## License

This package is licensed under the terms of the MIT license.

Made with ♥ at [snapADDY](https://snapaddy.com/)
