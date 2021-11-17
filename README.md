# A lightweight machine learning project

This is an example project for a lightweight and ready-to-deploy machine learning application.

## Installation

Install both production and dev dependencies of the project with [Poetry](https://python-poetry.org/):

```
$ poetry install
```

## Usage

Start the server:

```
$ gunicorn application
[INFO] Starting gunicorn 20.1.0
[INFO] Listening at: http://127.0.0.1:8000 (46025)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 46026
```

## Example

You can POST requets to the `/classification` endpoint:

```
$ curl \
  --request POST \
  --data '{"text": "Die Sopranos ist eine US-amerikanische Fernsehserie."}' \
  http://localhost:8000/classification
{"label": "Fernsehserie", "probability": 0.8808274865150452}
```

## License

This package is licensed under the terms of the MIT license.

Made with ♥ at [snapADDY](https://snapaddy.com/)
