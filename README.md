# SEO Analysis API

A FastAPI-based application that provides comprehensive SEO analysis and recommendations by analyzing website performance, content, and technical aspects.

## Features

- PageSpeed Insights analysis
- Content analysis (meta tags, headings, images)
- Technical SEO checks
- AI-powered recommendations using GPT-4
- Priority-based issue categorization

## Prerequisites

- Python 3.8+
- FastAPI
- OpenAI API key
- Google PageSpeed Insights API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd seo-analysis-api
```

2. Create a virtual environment 
for Windows
```bash
python -m venv myenv
venv\Scripts\activate
```

for linux/macOS
```bash
python -m venv myenv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory with the following content:
```env
OPENAI_API_KEY=your_openai_api_key_here
PAGESPEED_API_KEY=your_pagespeed_insights_api_key_here
```

To get the API keys:
- OpenAI API key: Sign up at [OpenAI](https://platform.openai.com/) and get your API key
- PageSpeed Insights API key: Get it from [Google Cloud Console](https://console.cloud.google.com/apis/credentials) by enabling the PageSpeed Insights API

## Project Structure

```
project/
├── main.py              # FastAPI application entry point
├── config.py            # Configuration and environment variables
├── logger.py            # Logging setup
└── modules/
    ├── __init__.py
    ├── pagespeed.py     # PageSpeed Insights analysis
    ├── content_analysis.py  # Content analysis
    ├── technical_seo.py    # Technical SEO checks
    └── recommendations.py  # AI-powered recommendations
```

## Usage

1. Start the server:
```bash
uvicorn main:app --reload
```

2. Make a POST request to `/analyze` with a URL:
```bash
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

## API Response

The API returns a JSON response containing:
- Performance recommendations
- Content analysis
- Technical SEO recommendations
- Priority counts for issues

Example response structure:
```json
{
    "recommendations": {
        "performance": "...",
        "content": "...",
        "technical": "..."
    },
    "priority_counts": {
        "high": 5,
        "medium": 3
    }
}
```


