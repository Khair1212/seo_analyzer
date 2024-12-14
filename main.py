from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from modules import pagespeed, content_analysis, technical_seo, recommendations
from logger import logger

app = FastAPI()

class URLInput(BaseModel):
    url: HttpUrl

@app.post("/analyze")
async def analyze_url(input: URLInput):
    url = str(input.url)
    logger.info(f"Analyzing URL: {url}")

    try:
        pagespeed_insights = pagespeed.get_insights(url)
        content_data = content_analysis.analyze(url)
        tech_seo_data = technical_seo.analyze(url)
        recommendations_data = recommendations.generate(url, pagespeed_insights, content_data, tech_seo_data)

        return {
            "url": url,
        
            "recommendations": recommendations_data
             
        }
    except Exception as e:
        logger.error(f"Error analyzing URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 
    

