import os
import boto3
from botocore.config import Config
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from botocore.exceptions import ClientError

app = FastAPI()

# Configure your AWS credentials and S3 bucket
S3_ACCESS_KEY_ID = os.getenv("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = os.getenv("S3_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_ENDPOINT_URL = os.getenv("S3_ENDPOINT_URL", None)
REGION_NAME = os.getenv("REGION_NAME")

# Create an S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
    endpoint_url=S3_ENDPOINT_URL,
    config=Config(signature_version="s3v4", s3={"addressing_style": "virtual"}),
)


class SignedUrlRequest(BaseModel):
    object_key: str
    expiration: int = 3600  # Default expiration time in seconds (1 hour)


@app.post("/sign-url")
async def sign_url(request: SignedUrlRequest):
    try:
        # Generate a pre-signed URL
        signed_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET_NAME, "Key": request.object_key},
            ExpiresIn=request.expiration,
        )
        return {"signed_url": signed_url}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
