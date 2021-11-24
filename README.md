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
  http://127.0.0.1:8000/classification
{"label": "show", "probability": 0.8808274865150452}
```

or check if the server is up and healthy:

```
$ curl \
  --request GET \
  http://127.0.0.1:8000/health
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

## Model

You can inspect the model with `onnx`:

```
>>> import onnx
>>> onnx.load("logistic-regression.onnx")
ir_version: 8
producer_name: "skl2onnx"
producer_version: "1.10.0"
domain: "ai.onnx"
model_version: 0
doc_string: ""
graph {
  node {
    input: "input"
    output: "output_label"
    output: "probability_tensor"
    name: "LinearClassifier"
    op_type: "LinearClassifier"
    attribute {
      name: "classlabels_strings"
      strings: "album"
      strings: "painting"
      strings: "show"
      type: STRINGS
    }
    attribute {
      name: "coefficients"
      floats: -1.0915333032608032
      floats: -0.3971465826034546
      floats: -0.6551226377487183
      floats: -1.1956942081451416
      floats: -0.766581654548645
      floats: -0.3559231162071228
      floats: 2.1808230876922607
      floats: 1.3179082870483398
      floats: 1.132351279258728
      floats: -0.9773756861686707
      floats: -0.3483078181743622
      floats: -0.5760289430618286
      floats: 2.433957815170288
      floats: 1.5667822360992432
      floats: 0.7291973233222961
      floats: -1.0122743844985962
      floats: -0.5995703935623169
      floats: -0.5131252408027649
      floats: 2.068908929824829
      floats: 0.7454543709754944
      floats: 1.2311515808105469
      floats: -1.238263487815857
      floats: -0.8002005219459534
      floats: -0.37327420711517334
      floats: -1.168548822402954
      floats: -0.7183379530906677
      floats: -0.6192260384559631
      type: FLOATS
    }
    attribute {
      name: "intercepts"
      floats: 0.050008490681648254
      floats: -0.17995497584342957
      floats: 0.1299464851617813
      type: FLOATS
    }
    attribute {
      name: "multi_class"
      i: 1
      type: INT
    }
    attribute {
      name: "post_transform"
      s: "SOFTMAX"
      type: STRING
    }
    domain: "ai.onnx.ml"
  }
  node {
    input: "probability_tensor"
    output: "probabilities"
    name: "Normalizer"
    op_type: "Normalizer"
    attribute {
      name: "norm"
      s: "L1"
      type: STRING
    }
    domain: "ai.onnx.ml"
  }
  node {
    input: "probabilities"
    output: "output_probability"
    name: "ZipMap"
    op_type: "ZipMap"
    attribute {
      name: "classlabels_strings"
      strings: "album"
      strings: "painting"
      strings: "show"
      type: STRINGS
    }
    domain: "ai.onnx.ml"
  }
  name: "50c5cd6ccd014e1dbdfca8ce501e1bab"
  input {
    name: "input"
    type {
      tensor_type {
        elem_type: 7
        shape {
          dim {
          }
          dim {
            dim_value: 9
          }
        }
      }
    }
  }
  output {
    name: "output_label"
    type {
      tensor_type {
        elem_type: 8
        shape {
          dim {
          }
        }
      }
    }
  }
  output {
    name: "output_probability"
    type {
      sequence_type {
        elem_type {
          map_type {
            key_type: 8
            value_type {
              tensor_type {
                elem_type: 1
              }
            }
          }
        }
      }
    }
  }
}
opset_import {
  domain: "ai.onnx.ml"
  version: 1
}
opset_import {
  domain: ""
  version: 14
}
```

## License

This package is licensed under the terms of the MIT license.

Made with ♥ at [snapADDY](https://snapaddy.com/)
