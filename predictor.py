import os
from typing import Dict, Union

import kserve
import numpy as np
import onnxruntime as ort
from kserve import InferRequest
from kserve.protocol.grpc.grpc_predict_v2_pb2 import ModelInferRequest


class ONNXModel(kserve.Model):
    def __init__(self, name: str):
        super().__init__(name)
        self.model = None
        self.ready = False
        self.load()

    def load(self):
        model_path = "./models/fraud/1/model.onnx"
        self.model = ort.InferenceSession(model_path)
        self.ready = True

    async def predict(
            self,
            payload: Union[Dict, InferRequest, ModelInferRequest],
            headers: Dict[str, str] = None,
            response_headers: Dict[str, str] = None,
    ) -> Dict:  # Simplified return type to Dict since that's what we return
        try:
            # Handle payload as a dict (assuming REST input)
            if isinstance(payload, dict):
                input_data = payload["instances"]
            else:
                # Handle InferRequest or ModelInferRequest if needed
                raise ValueError("Unsupported payload type; expected dict")

            input_data = np.array(input_data, dtype=np.float32)
            input_name = self.model.get_inputs()[0].name
            output = self.model.run(None, {input_name: input_data})
            predictions = output[0].tolist()
            return {"predictions": predictions}
        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    model = ONNXModel("onnx-model")
    kserve.ModelServer().start([model])
