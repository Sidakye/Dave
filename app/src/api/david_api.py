from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from ..services.gdp_services import use_gdp_by_country_name

app = FastAPI(title="David AI", description="David AI forecasting API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "David AI GDP Forecast"}


@app.get("/gdp/one/")
def gdp_one(country_name: str = Query(None, description="Country name to get GDP forecast for")):
    """Return GDP actuals and a next-year prediction for a country.

    Uses the existing service layer (`use_gdp_by_country_name`) so model loading
    and DB access remain unchanged.
    """
    name = country_name or "Aruba"
    try:
        data = use_gdp_by_country_name(name)
        if data is None:
            raise HTTPException(status_code=404, detail="Country not found or no data")
        return JSONResponse(content={"message": "success", "code": 200, "body": data})
    except HTTPException:
        raise
    except Exception as e:
        # bubble up 500 for unexpected errors
        raise HTTPException(status_code=500, detail=str(e))
