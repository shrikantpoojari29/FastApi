# Activate the virtual environment (replace `venv` with your virtual environment name if different)
.\venv\Scripts\activate
# Run the FastAPI application using Uvicorn with automatic reloading enabled
uvicorn app:app --reload
# Upload a PDF file using cURL to the /upload_pdf/ endpoint
curl -X POST "http://127.0.0.1:8000/upload_pdf/" -F "file=@C:/inter/sample.pdf"
# Send a query to the /query_pdf/ endpoint using cURL
curl -X POST "http://127.0.0.1:8000/query_pdf/" -H "Content-Type: application/json" -d "{\"query\": \"What is the content of the first page?\"}"
