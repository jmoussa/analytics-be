from api.endpoints.data_acquisitions.data_sources.covid import CovidAggregator
from fastapi.responses import JSONResponse
from loguru import logger
# pylint: disable=E0611
from pydantic import BaseModel

# pylint: enable=E0611

DOC = {
    200: {
        "description": "API response successfully",
        "content": {
            "application/json": {"example": {"data_source": "covid", "limit": 0}}
        },
    }
}


class Payload(BaseModel):
    data_source: str
    limit: int


def post(payload: Payload):
    """
    POST /api/v1/data_acquisition/
    The entry point for data acquisition.
    Send a query in JSON format.
    The query, will be parsed and the proper data scource will be queried then data will be returned in JSON format.
    """
    logger.info(f"{payload}")
    payload.data_source = payload.data_source.lower()
    if payload.data_source == "covid":
        aggregator = CovidAggregator()
        data = aggregator.get_data(payload.limit)
    else:
        return JSONResponse({"error": "Data source not found"}, status_code=404)
    return JSONResponse(data, status_code=200)
