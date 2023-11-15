from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from api.api_v1.endpoints.models import router
from api.deps import auth_required

api_router = APIRouter()


@api_router.get("/health", status_code=status.HTTP_200_OK)
async def healthcheck():
    return JSONResponse(content={"status": "ok"}, status_code=status.HTTP_200_OK)


api_router.include_router(router, prefix='/reco', tags=["models"], dependencies=[Depends(auth_required)])
