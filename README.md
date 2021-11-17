# A lightweight machine learning project

tba

## Installation

tba

```
$ poetry install
```

## Usage

tba

```
$ gunicorn application
[INFO] Starting gunicorn 20.1.0
[INFO] Listening at: http://127.0.0.1:8000 (46025)
[INFO] Using worker: sync
[INFO] Booting worker with pid: 46026
```

## Example

tba

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
