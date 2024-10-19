FROM python:3.9-slim

# ---------------------------------------------------------------------------- #
#                                     Meta                                     #
# ---------------------------------------------------------------------------- #

LABEL org.opencontainers.image.description="Signed URL generator service for the Lectorium project"
LABEL org.opencontainers.image.source="https://github.com/akdasa-studios/lectorium"


# ---------------------------------------------------------------------------- #
#                                     Setup                                    #
# ---------------------------------------------------------------------------- #

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
