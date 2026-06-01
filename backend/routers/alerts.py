from fastapi import APIRouter, File, UploadFile
from typing import Annotated  # ייבוא הכלי החדש
from services.analyzer_service import AnalyzerService

router = APIRouter(prefix="/alerts", tags=["Alerts"])

# שימוש ב-Annotated שמגדיר בצורה חד-משמעית: זו רשימה של UploadFile מסוג File
@router.post("")
async def get_alerts(files: Annotated[list[UploadFile], File()]):
    """
    נקודת קצה לקבלת קבצים מרובים וניתוח ה-AST שלהם
    """
    issues = await AnalyzerService.analyze_uploaded_files(files)
    return {"issues": issues}