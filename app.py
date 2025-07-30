# app.py

import streamlit as st
import asyncio
from agents.crawler_agent import CrawlerAgent
from agents.sentiment_agent import SentimentAgent
from agents.valuation_agent import ValuationAgent
from agents.thesis_writer_agent import ThesisWriterAgent
from agents.critic_agent import CriticAgent
from agents.thesis_rewrite_agent import ThesisRewriteAgent
from utils.search import search_company_news

st.set_page_config(page_title="IntelliVest AI", layout="wide")
st.title("🚀 IntelliVest AI — Investment Thesis Builder")

company = st.text_input("Enter a company or stock name (e.g., Amazon, TCS, Nvidia)", value="")

if st.button("Generate Thesis") and company:
    with st.spinner("🔍 Searching Tavily for latest news..."):
        urls = search_company_news(company)
        st.success(f"✅ Found {len(urls)} live URLs.")
        
        # Display the live URLs found
        if urls:
            st.subheader("📰 Live URLs Found")
            for i, url in enumerate(urls, 1):
                st.write(f"**{i}.** {url}")
            st.write("---")

    if urls:
        async def run_pipeline():
            try:
                # Create progress containers
                progress_container = st.container()
                status_container = st.container()
                
                with progress_container:
                    st.info("🌐 Crawling articles...")
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                
                crawler = CrawlerAgent()
                documents = await crawler.crawl_multiple(urls)
                
                # Update progress
                progress_bar.progress(100)
                status_text.text("✅ Crawling completed!")
                
                # Filter out error documents and show results
                valid_documents = [doc for doc in documents if doc.get("markdown") and not doc["markdown"].startswith("❌")]
                error_documents = [doc for doc in documents if doc.get("markdown") and doc["markdown"].startswith("❌")]
                
                with status_container:
                    st.success(f"✅ Successfully crawled {len(valid_documents)} out of {len(urls)} URLs")
                    if error_documents:
                        st.warning(f"⚠️ Failed to crawl {len(error_documents)} URLs")
                        with st.expander("See failed URLs"):
                            for doc in error_documents:
                                st.write(f"**{doc['url']}**: {doc['markdown']}")
                
                if not valid_documents:
                    st.error("❌ No valid content extracted from any URLs. Please try a different company or check the URLs.")
                    return
                
                combined_md = "\n\n".join([doc["markdown"] for doc in valid_documents])
                
                if not combined_md.strip():
                    st.error("❌ No valid content extracted.")
                    return

                st.info("🧠 Running Sentiment Analysis...")
                sentiment_agent = SentimentAgent()
                sentiment = await sentiment_agent.analyze_sentiment(combined_md)

                st.info("💸 Running Valuation...")
                valuation_agent = ValuationAgent()
                valuation = await valuation_agent.estimate_valuation(combined_md)

                st.info("📄 Generating Thesis...")
                thesis_agent = ThesisWriterAgent()
                thesis = await thesis_agent.generate_thesis(
                    content=combined_md,
                    sentiment=sentiment,
                    valuation=valuation,
                    company_name=company
                )

                st.info("🧐 Running Critique...")
                critic_agent = CriticAgent()
                critique = await critic_agent.critique_thesis(thesis_markdown=thesis, company_name=company)

                st.info("🛠 Rewriting Thesis...")
                rewriter_agent = ThesisRewriteAgent()
                revised = await rewriter_agent.revise_thesis(
                    thesis_markdown=thesis,
                    critique=critique,
                    company_name=company
                )

                st.subheader("📌 Final Investment Thesis")
                st.markdown(revised)

                st.subheader("🗒 Critique Summary")
                st.markdown(critique)

            except Exception as e:
                st.error(f"❌ Error: {e}")
                st.exception(e)

        asyncio.run(run_pipeline())
