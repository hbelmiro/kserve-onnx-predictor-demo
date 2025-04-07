FROM quay.io/fedora/python-311

LABEL org.opencontainers.image.description="This is a demo ONNX model custom predictor for KServe"
LABEL org.opencontainers.image.source="https://github.com/hbelmiro/kserve-onnx-predictor-demo"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY models ./models
COPY predictor.py .

CMD ["python", "predictor.py"]
