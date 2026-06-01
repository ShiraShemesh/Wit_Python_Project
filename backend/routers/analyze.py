from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse
from typing import Annotated
from services.analyzer_service import AnalyzerService
from services.graph_service import GraphService

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("")
async def analyze_files(files: Annotated[list[UploadFile], File()]):
    """
    נקודת קצה לניתוח קבצים והחזרת גרפים ויזואליים בפורמט PNG
    """
    analysis_result = await AnalyzerService.analyze_uploaded_files_full(files)

    zip_buffer = GraphService.generate_graphs_zip(analysis_result)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=codeguard_report.zip"}
    )