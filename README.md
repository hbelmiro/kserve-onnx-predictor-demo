## Running locally

```shell
export MODEL_PATH=./models/fraud/1/model.onnx
python predictor.py
```

In a different shell section:

```shell
curl -i -X POST http://0.0.0.0:8080/v1/models/onnx-model:predict -H "Content-Type: application/json" -d '{"instances": [[50.0, 5.0, 0.0, 0.0, 1.0]]}'
```

The output should be something like:

```shell
HTTP/1.1 200 OK
date: Sat, 05 Apr 2025 14:42:34 GMT
server: uvicorn
content-length: 38
content-type: application/json

{"predictions":[[0.9998821020126343]]}
```