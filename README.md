# SER-with-GPU
Speech Emotion Recognition on GPU (Google Cloud Run)

## Local Setup
1. Clone the project from GitHub, and open in your IDE. 
2. Open the terminal: (In VS Code) File -> New Terminal
3. Start a new virtual env using PyEnv: https://github.com/pyenv/pyenv
    ```bash
    pyenv local 3.10.0

    python -m venv venv

    source venv/bin/activate

    python -m pip install --upgrade pip

    pip install -r requirements.txt
    ```
4. To test the API locally, run:
    ```bash
    fastapi dev main.py  
    ```
5. Navigate to 
    ```bash
    http://127.0.0.1:8000/docs
    ```
6. Click on the "try it out" button
7. Then upload your local file and hit the "Execute button.

## Testing Live API

Grab token from gcloud
```bash
gcloud auth print-identity-token
```

Navigate to postman:
- Switch the setting to "POST"
- Change to the form data
- Change to value to "file"
- Add the key to be "file"
- Then select to upload a test file
- Add token to bearer token
- Send

Also can check GPU and FFMPEG endpoints 

