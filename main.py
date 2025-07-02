from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

class ModerationResult(BaseModel):
    status: str
    reason: str = None

@app.post("/moderate", response_model=ModerationResult)
async def moderate_image(file: UploadFile = File(...)):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Неподдерживаемый тип файла. Поддерживаются только .jpg и .png.")

    sightengine_api_user = os.getenv("SIGHTENGINE_API_USER")
    sightengine_api_secret = os.getenv("SIGHTENGINE_API_SECRET")

    if not sightengine_api_user or not sightengine_api_secret:
        raise HTTPException(status_code=500, detail="SIGHTENGINE_API_USER или SIGHTENGINE_API_SECRET не установлены в переменных окружения.")

    try:
        contents = await file.read()
        params = {
            'models': 'nudity-2.1',
            'api_user': sightengine_api_user,
            'api_secret': sightengine_api_secret
        }
        files = {'media': contents}
        response = requests.post(
            'https://api.sightengine.com/1.0/check.json',
            files=files,
            data=params
        )
        response.raise_for_status()
        sightengine_result = response.json()

        nsfw_detected = False
        if "nudity" in sightengine_result:
            nudity_data = sightengine_result["nudity"]
            if nudity_data.get("sexual_activity", 0) > 0.7 or \
               nudity_data.get("sexual_display", 0) > 0.7 or \
               nudity_data.get("erotica", 0) > 0.7 or \
               nudity_data.get("very_suggestive", 0) > 0.7 or \
               nudity_data.get("suggestive", 0) > 0.7:
                nsfw_detected = True

        if nsfw_detected:
            return ModerationResult(status="REJECTED", reason="NSFW content")
        else:
            return ModerationResult(status="OK")

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обращении к Sightengine API: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
