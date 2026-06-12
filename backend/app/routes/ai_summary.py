from fastapi import APIRouter, HTTPException

from app.models.summary_request import SummaryRequest
from app.services.ai_service import MissingOpenRouterKeyError, OpenRouterAPIError, generate_summary

router = APIRouter(prefix="/api", tags=["AI Clinical Summary"])


@router.post("/generate-summary")
def generate_ai_summary(request: SummaryRequest):
    try:
        summary = generate_summary(request.bundle)
        return {"summary": summary}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except MissingOpenRouterKeyError as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    except ConnectionError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except TimeoutError as exc:
        raise HTTPException(status_code=504, detail=str(exc))
    except OpenRouterAPIError as exc:
        raise HTTPException(status_code=502, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI summary generation failed: {exc}")
