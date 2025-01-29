# from text_to_json import quote_json
from helpers.text_to_json import quote_json
from bs4 import BeautifulSoup
import json
import structlog
from curl_cffi import requests

logger = structlog.get_logger()


def process_data(data_web):
    try:
        data_soup = BeautifulSoup(data_web.text, "lxml")
        logger.info("Data Web Scrapped")
        data_scripts = data_soup.find_all("script")
        logger.info("Scripts Found")
        for script in data_scripts:
            if "ZLApp.APICredentials" in script.text:
                logger.info("Token Found")
                doc_creds = script.text.split("ZLApp.APICredentials = ")[1].split(";")[
                    0
                ]
                doc_creds_replace = doc_creds.replace("'", '"')
                doc_creds_json = json.loads(doc_creds_replace)
            if "ZLApp.AppConfig" in script.text:
                logger.info("Doctor Basic Data Found")
                doc_text = script.text.split("ZLApp.AppConfig = ")[1].split(";")[0]
                doc_data = doc_text.split("DOCTOR: ")[1].split("},")[0]
                logger.info("Doctor Basic Data Extracted")
                doc_data_prod = "".join([doc_data, "}"])
                doc_data_prod = doc_data_prod.replace("'", '"')
                valid_doc_data = quote_json(doc_data_prod)
                doc_data_json = json.loads(valid_doc_data)
                logger.info("Doctor Basic Data in JSON")
        data = {"credentials": doc_creds_json["ACCESS_TOKEN"], "doctor": doc_data_json}
        logger.info("Data Processed")
        return data
    except Exception as e:
        logger.error("General Error", error=str(e))
        return {"error": str(e)}


def get_doc_profile(doc_data: dict):
    try:
        token = doc_data["credentials"]
        doc_id = int(doc_data["doctor"]["ID"])
        logger.info("Doctor ID", doc_id=doc_id)
        doc_profile_url = f"https://www.doctoralia.com.mx/api/v3/doctors/{doc_id}/?with%5B%5D=doctor.license_numbers&with%5B%5D=doctor.specializations&with%5B%5D=doctor.addresses"
        headers = {
            "Authorization": f"Bearer {token}",
            # "Cookie": "Cookie=GUEST_SESSION=yAUViNGH25pNR6HID5OXavFjEZacxymIMeqOVHMt1S0",
        }
        doc_profile = requests.get(doc_profile_url, headers=headers)
        logger.info("Doctor Profile Requested", profile=doc_profile)
        logger.info("Doctor Profile Requested")
        if doc_profile.status_code == 200:
            logger.info("Doctor Profile Data Received")
            doc_profile_data = doc_profile.json()
            return doc_profile_data
    except requests.errors.RequestsError as e:
        logger.error("Request Error", error=str(e))
        return {"Request Error": str(e)}
    except Exception as e:
        logger.error("General Error", error=str(e))
        return {"error": str(e)}
