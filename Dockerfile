FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose Gradio port
EXPOSE 7860

# Default command to run the UI
# Note: User must mount data volume or include data in build if they want it pre-indexed.
# For this setup, we assume data is generated or mounted.
CMD ["python", "src/ui/app_gradio.py"]
