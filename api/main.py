# api/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import uvicorn
from agents.crawler_agent import CrawlerAgent
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_writer_agent import ThesisWriterAgent
from agents.critic_agent import CriticAgent
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
        
        # Step 2: Crawl URLs
        progress_log.append("🌐 Starting to crawl websites...")
        crawler = CrawlerAgent()
        documents = await crawler.crawl_multiple(urls)
        
        # Track successful scrapes
        scraped_urls = []
        valid_documents = []
        failed_urls = []
        
        for i, doc in enumerate(documents):
            if doc.get("markdown") and not doc["markdown"].startswith("❌"):
                valid_documents.append(doc)
                scraped_urls.append(doc["url"])
                progress_log.append(f"✅ Successfully scraped: {doc['url']}")
            else:
                failed_urls.append(doc["url"])
                progress_log.append(f"❌ Failed to scrape: {doc['url']}")
        
        if not valid_documents:
            raise HTTPException(status_code=500, detail="No valid content extracted from URLs")
        
        progress_log.append(f"📊 Successfully scraped {len(valid_documents)} out of {len(urls)} URLs")
        
        # Step 3: Combine content
        progress_log.append("📝 Combining and analyzing content...")
        combined_md = "\n\n".join([doc["markdown"] for doc in valid_documents])
        
        # Step 4: Sentiment Analysis
        progress_log.append("😊 Analyzing sentiment...")
        sentiment_agent = SentimentAgent()
        sentiment = await sentiment_agent.analyze_sentiment(combined_md)
        
        # Step 5: Valuation Analysis
        progress_log.append("💰 Estimating valuation...")
        valuation_agent = ValuationAgent()
        valuation = await valuation_agent.estimate_valuation(combined_md)
        
        # Step 6: Generate Thesis
        progress_log.append("📈 Generating investment thesis...")
        thesis_agent = ThesisWriterAgent()
        thesis = await thesis_agent.generate_thesis(
            content=combined_md, sentiment=sentiment, valuation=valuation, company_name=company
        )
        
        # Step 7: Critique Thesis
        progress_log.append("🔍 Critiquing the thesis...")
        critic_agent = CriticAgent()
        critique = await critic_agent.critique_thesis(thesis_markdown=thesis, company_name=company)
        
        # Step 8: Revise Thesis
        progress_log.append("✏️ Revising thesis based on critique...")
        rewriter_agent = ThesisRewriteAgent()
        revised_thesis = await rewriter_agent.revise_thesis(
            thesis_markdown=thesis, critique=critique, company_name=company
        )
        
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