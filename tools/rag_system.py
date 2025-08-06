"""
🧠 RAG (Retrieval-Augmented Generation) System
=============================================

Advanced question-answering system with vector storage and intelligent fallback.
Integrates with IntelliVest AI for enhanced user interaction.
"""

import os
import json
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import tiktoken
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RAGSystem:
    """Advanced RAG system for investment analysis Q&A"""
    
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.max_results = 5
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path="./vector_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create collections
        self.reports_collection = self.client.get_or_create_collection(
            name="investment_reports",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.questions_collection = self.client.get_or_create_collection(
            name="question_history",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Session management
        self.current_company = None
        self.current_report_id = None
        
        print("🧠 RAG System Initialized")
        print(f"📊 Vector DB: {self.client.heartbeat()}")
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into meaningful chunks"""
        # Use tiktoken for token counting
        encoding = tiktoken.get_encoding("cl100k_base")
        
        chunks = []
        tokens = encoding.encode(text)
        
        for i in range(0, len(tokens), self.chunk_size - self.chunk_overlap):
            chunk_tokens = tokens[i:i + self.chunk_size]
            chunk_text = encoding.decode(chunk_tokens)
            
            # Clean and validate chunk
            chunk_text = chunk_text.strip()
            if len(chunk_text) > 50:  # Minimum meaningful chunk size
                chunks.append(chunk_text)
        
        return chunks
    
    def store_report(self, company_name: str, report_content: str, report_metadata: Dict[str, Any]) -> str:
        """Store investment report in vector database"""
        try:
            print(f"💾 Storing report for {company_name}")
            
            # Generate unique report ID
            report_id = f"{company_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Chunk the report
            chunks = self.chunk_text(report_content)
            print(f"📝 Created {len(chunks)} chunks from report")
            
            # Generate embeddings for chunks
            embeddings = self.embedding_model.encode(chunks)
            
            # Prepare metadata for each chunk
            chunk_metadatas = []
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    "company_name": company_name,
                    "report_id": report_id,
                    "chunk_index": i,
                    "chunk_type": self._classify_chunk(chunk),
                    "timestamp": datetime.now().isoformat(),
                    **report_metadata
                }
                chunk_metadatas.append(chunk_metadata)
            
            # Store in vector database
            self.reports_collection.add(
                embeddings=embeddings.tolist(),
                documents=chunks,
                metadatas=chunk_metadatas,
                ids=[f"{report_id}_chunk_{i}" for i in range(len(chunks))]
            )
            
            # Update current session
            self.current_company = company_name
            self.current_report_id = report_id
            
            print(f"✅ Successfully stored report with {len(chunks)} chunks")
            return report_id
            
        except Exception as e:
            print(f"❌ Error storing report: {e}")
            return None
    
    def _classify_chunk(self, chunk: str) -> str:
        """Classify chunk type based on content"""
        chunk_lower = chunk.lower()
        
        if any(keyword in chunk_lower for keyword in ['financial', 'revenue', 'profit', 'earnings', 'margin']):
            return "financial_analysis"
        elif any(keyword in chunk_lower for keyword in ['technical', 'price', 'chart', 'momentum', 'support']):
            return "technical_analysis"
        elif any(keyword in chunk_lower for keyword in ['risk', 'challenge', 'threat', 'concern']):
            return "risk_assessment"
        elif any(keyword in chunk_lower for keyword in ['growth', 'opportunity', 'catalyst', 'driver']):
            return "growth_analysis"
        elif any(keyword in chunk_lower for keyword in ['valuation', 'target', 'price', 'multiple']):
            return "valuation_analysis"
        else:
            return "general_analysis"
    
    def search_reports(self, query: str, company_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search for relevant content in stored reports"""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])
            
            # Build where clause for company filtering
            where_clause = {}
            if company_name:
                where_clause["company_name"] = company_name
            
            # Search in vector database
            results = self.reports_collection.query(
                query_embeddings=query_embedding.tolist(),
                n_results=self.max_results,
                where=where_clause if where_clause else None
            )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i, (doc, metadata, distance) in enumerate(zip(
                    results['documents'][0],
                    results['metadatas'][0],
                    results['distances'][0]
                )):
                    formatted_results.append({
                        'content': doc,
                        'metadata': metadata,
                        'similarity_score': 1 - distance,  # Convert distance to similarity
                        'rank': i + 1
                    })
            
            print(f"🔍 Found {len(formatted_results)} relevant chunks for query: '{query}'")
            return formatted_results
            
        except Exception as e:
            print(f"❌ Error searching reports: {e}")
            return []
    
    def answer_question(self, question: str, llm_callback, web_search_callback=None) -> Dict[str, Any]:
        """Answer user question using RAG with intelligent fallback"""
        try:
            print(f"🤔 Processing question: '{question}'")
            
            # Step 1: Search in stored reports
            relevant_chunks = self.search_reports(question, self.current_company)
            
            if relevant_chunks and any(chunk['similarity_score'] > 0.7 for chunk in relevant_chunks):
                # High confidence match found in reports
                print("📊 Using stored report data for answer")
                return self._generate_answer_from_reports(question, relevant_chunks, llm_callback)
            
            elif web_search_callback:
                # Fallback to web search
                print("🌐 Falling back to web search")
                return self._generate_answer_from_web(question, web_search_callback, llm_callback)
            
            else:
                # No relevant data found
                return {
                    'answer': "I don't have enough information to answer this question accurately. Please ensure a company report has been generated first.",
                    'source': 'no_data',
                    'confidence': 0.0,
                    'chunks_used': []
                }
                
        except Exception as e:
            print(f"❌ Error answering question: {e}")
            return {
                'answer': f"Sorry, I encountered an error while processing your question: {str(e)}",
                'source': 'error',
                'confidence': 0.0,
                'chunks_used': []
            }
    
    def _generate_answer_from_reports(self, question: str, chunks: List[Dict[str, Any]], llm_callback) -> Dict[str, Any]:
        """Generate answer from stored report chunks"""
        try:
            # Prepare context from chunks
            context = "\n\n".join([chunk['content'] for chunk in chunks])
            
            # Create prompt for LLM
            prompt = f"""Based on the following investment analysis report for {self.current_company}, please answer the user's question.

REPORT CONTEXT:
{context}

USER QUESTION: {question}

Please provide a comprehensive and accurate answer based on the report data. If the question cannot be fully answered from the provided context, acknowledge this limitation.

Answer:"""
            
            # Get LLM response
            response = llm_callback(prompt)
            
            # Calculate confidence based on chunk similarity scores
            avg_similarity = sum(chunk['similarity_score'] for chunk in chunks) / len(chunks)
            confidence = min(avg_similarity * 1.2, 1.0)  # Boost confidence slightly
            
            return {
                'answer': response,
                'source': 'stored_report',
                'confidence': confidence,
                'chunks_used': chunks,
                'company': self.current_company
            }
            
        except Exception as e:
            print(f"❌ Error generating answer from reports: {e}")
            return {
                'answer': "I encountered an error while generating the answer from stored reports.",
                'source': 'error',
                'confidence': 0.0,
                'chunks_used': chunks
            }
    
    def _generate_answer_from_web(self, question: str, web_search_callback, llm_callback) -> Dict[str, Any]:
        """Generate answer from web search"""
        try:
            # Perform web search
            search_query = f"{self.current_company} {question}" if self.current_company else question
            web_results = web_search_callback(search_query)
            
            if not web_results:
                return {
                    'answer': "I couldn't find relevant information on the web to answer your question.",
                    'source': 'web_search_failed',
                    'confidence': 0.0,
                    'chunks_used': []
                }
            
            # Prepare web context
            web_context = "\n\n".join([result.get('content', '') for result in web_results[:3]])
            
            # Create prompt for LLM
            prompt = f"""Based on the following web search results, please answer the user's question about {self.current_company or 'the company'}.

WEB SEARCH RESULTS:
{web_context}

USER QUESTION: {question}

Please provide a comprehensive answer based on the web search results. Include relevant facts and insights.

Answer:"""
            
            # Get LLM response
            response = llm_callback(prompt)
            
            return {
                'answer': response,
                'source': 'web_search',
                'confidence': 0.6,  # Lower confidence for web search
                'chunks_used': [],
                'web_results': web_results[:3]
            }
            
        except Exception as e:
            print(f"❌ Error generating answer from web: {e}")
            return {
                'answer': "I encountered an error while searching the web for information.",
                'source': 'web_search_error',
                'confidence': 0.0,
                'chunks_used': []
            }
    
    def get_suggested_questions(self) -> List[str]:
        """Get suggested questions based on current company"""
        if not self.current_company:
            return []
        
        suggestions = [
            f"What are the key financial metrics for {self.current_company}?",
            f"What are the main risks facing {self.current_company}?",
            f"What is the growth outlook for {self.current_company}?",
            f"What are the competitive advantages of {self.current_company}?",
            f"What is the current valuation of {self.current_company}?",
            f"What are the recent developments at {self.current_company}?",
            f"What is the market position of {self.current_company}?",
            f"What are the investment recommendations for {self.current_company}?"
        ]
        
        return suggestions
    
    def get_question_history(self, company_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get question history for a company"""
        try:
            where_clause = {}
            if company_name:
                where_clause["company_name"] = company_name
            
            results = self.questions_collection.get(
                where=where_clause if where_clause else None,
                limit=20
            )
            
            history = []
            for i, (doc, metadata) in enumerate(zip(results['documents'], results['metadatas'])):
                history.append({
                    'question': doc,
                    'timestamp': metadata.get('timestamp'),
                    'company': metadata.get('company_name')
                })
            
            return sorted(history, key=lambda x: x['timestamp'], reverse=True)
            
        except Exception as e:
            print(f"❌ Error getting question history: {e}")
            return []
    
    def store_question(self, question: str, answer: str, confidence: float):
        """Store question and answer for history"""
        try:
            if not self.current_company:
                return
            
            # Store question
            question_embedding = self.embedding_model.encode([question])
            
            self.questions_collection.add(
                embeddings=question_embedding.tolist(),
                documents=[question],
                metadatas=[{
                    'company_name': self.current_company,
                    'answer': answer,
                    'confidence': confidence,
                    'timestamp': datetime.now().isoformat()
                }],
                ids=[f"q_{datetime.now().strftime('%Y%m%d_%H%M%S')}"]
            )
            
        except Exception as e:
            print(f"❌ Error storing question: {e}")
    
    def clear_company_data(self, company_name: str):
        """Clear all data for a specific company"""
        try:
            # Delete from reports collection
            self.reports_collection.delete(
                where={"company_name": company_name}
            )
            
            # Delete from questions collection
            self.questions_collection.delete(
                where={"company_name": company_name}
            )
            
            print(f"🗑️ Cleared all data for {company_name}")
            
        except Exception as e:
            print(f"❌ Error clearing company data: {e}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            reports_count = self.reports_collection.count()
            questions_count = self.questions_collection.count()
            
            return {
                'total_reports': reports_count,
                'total_questions': questions_count,
                'current_company': self.current_company,
                'current_report_id': self.current_report_id,
                'vector_db_status': 'healthy' if self.client.heartbeat() else 'error'
            }
            
        except Exception as e:
            print(f"❌ Error getting system stats: {e}")
            return {'error': str(e)} 