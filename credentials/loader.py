

import os
import base64

def ensure_google_credentials():
    b64_data = os.getenv("GOOGLE_CREDENTIALS_B64")
    if not b64_data:
        raise EnvironmentError("GOOGLE_CREDENTIALS_B64 is not set in environment variables.")
    
    try:
        decoded = base64.b64decode(b64_data)
        with open("google-credentials.json", "wb") as f:
            f.write(decoded)
        print("✅ google-credentials.json has been written successfully.")
    except Exception as e:
        raise RuntimeError(f"Failed to write google-credentials.json: {e}")