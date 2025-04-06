from fastapi import FastAPI, File, UploadFile
# from fastapi import HTTPException
# import subprocess
import tempfile
import shutil
import os
# import torch
import time
from model import SerModel

MODEL = SerModel()

app = FastAPI()


def save_upload_file_to_temp(upload_file: UploadFile) -> str:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        upload_file.file.seek(0)
        shutil.copyfileobj(upload_file.file, temp_file)
        temp_file_path = temp_file.name
    return temp_file_path


@app.post("/predict/")
async def translate(file: UploadFile = File(...)):
    response = {}
    temp_filepath = save_upload_file_to_temp(file)
    try:
        s = time.time()
        prediction = MODEL.predict(audio_file=temp_filepath)
        e = time.time()
        response["inference_time"] = e - s
    finally:
        os.remove(temp_filepath)
    response["prediction"] = prediction
    return response
