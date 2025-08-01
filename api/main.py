# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import uvicorn
from agents.research_agent import ResearchAgent
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_agent import ThesisAgent
from agents.critique_agent import CritiqueAgent
from agents.thesis_rewrite_agent import ThesisRewriteAgent
from utils.search import search_company_news

app = FastAPI(title="IntelliVest AI API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanyRequest(BaseModel):
    company_name: str

class ThesisResponse(BaseModel):
    urls_found: list
    scraped_urls: list
    thesis: str
    critique: str
    revised_thesis: str
    status: str
    progress_log: list

@app.get("/")
async def root():
    return {"message": "IntelliVest AI API is running!"}

@app.post("/generate-thesis", response_model=ThesisResponse)
async def generate_thesis(request: CompanyRequest):
    progress_log = []
    
    try:
        company = request.company_name.strip()
        
        # Step 1: Search for URLs
        progress_log.append("🔍 Searching for latest news and information...")
        urls = search_company_news(company)
        if not urls:
            raise HTTPException(status_code=404, detail="No live URLs found for this company")
        
        progress_log.append(f"✅ Found {len(urls)} URLs to analyze")
        
        # Step 2: Research Analysis
        progress_log.append("📚 Conducting comprehensive research...")
        research_agent = ResearchAgent()
        research_data = await research_agent.research_company(company)
        
        # Track successful research
        scraped_urls = research_data.get("data_sources", [])
        progress_log.append(f"📊 Research completed with {len(scraped_urls)} sources")
        
        # Step 3: Sentiment Analysis
        progress_log.append("😊 Analyzing sentiment...")
        sentiment_agent = SentimentAgent()
        sentiment_data = await sentiment_agent.analyze_sentiment(company, research_data)
        
        # Step 4: Valuation Analysis
        progress_log.append("💰 Estimating valuation...")
        valuation_agent = ValuationAgent()
        valuation_data = await valuation_agent.perform_valuation(company, research_data)
        
        # Step 5: Generate Thesis
        progress_log.append("📈 Generating investment thesis...")
        thesis_agent = ThesisAgent()
        thesis_data = await thesis_agent.generate_thesis(company, research_data, sentiment_data, valuation_data)
        
        # Extract thesis content
        thesis = thesis_data.get("thesis_summary", "Thesis generation failed")
        
        # Step 6: Critique Thesis
        progress_log.append("🔍 Critiquing the thesis...")
        critique_agent = CritiqueAgent()
        critique_data = await critique_agent.critique_thesis(company, thesis_data, research_data, sentiment_data, valuation_data)
        
        # Extract critique content
        critique = critique_data.get("thesis_validation", "Critique generation failed")
        
        # Step 7: Rewrite Thesis Based on Critique
        progress_log.append("✏️ Rewriting thesis based on critique feedback...")
        rewriter_agent = ThesisRewriteAgent()
        revised_thesis = await rewriter_agent.revise_thesis(thesis, critique, company)
        
        progress_log.append("🎉 Analysis complete!")
        
        return ThesisResponse(
            urls_found=urls,
            scraped_urls=scraped_urls,
            thesis=thesis,
            critique=critique,
            revised_thesis=revised_thesis,
            status="success",
            progress_log=progress_log
        )
    except Exception as e:
        progress_log.append(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating thesis: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001) 