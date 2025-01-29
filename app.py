from sqlite3 import DataError
from fastapi import FastAPI
from curl_cffi import requests
from helpers import extract_data, text_to_json
import uvicorn
import structlog


app = FastAPI()
logger = structlog.get_logger()

@app.get("/")
async def status_root():
    return {"message": "Hello World!", "status": "ok"}

@app.get("/info/{doc_url:path}")
async def get_doctor_info(doc_url: str):
    try:
        if doc_url is not None:
            logger.info("Doctoralia URL", url=doc_url)
            if not text_to_json.validate_url(doc_url):
                logger.error("Invalid URL")
                return {"error": "Invalid URL"}
            logger.info("Doctoralia URL Validated: ", url=doc_url)
            data_web = requests.get(doc_url, impersonate="chrome124")
            logger.info("Doctoralia Data Requested")
            if data_web.status_code == 200:
                logger.info("Doctoralia Data Received")
                doc_data = extract_data.process_data(data_web)
                logger.info("Doctor Data Processed")
                doc_profile = extract_data.get_doc_profile(doc_data)
                logger.info("Doctor Profile Data Processed")
                return doc_profile
    except Exception as e:
        logger.error("General Error", error=str(e))
        return {"error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=3000, log_level="info", reload=True)