#!/usr/bin/env python3
"""
Bangla News Scraper Pipeline
Scrapes Bangla news, summarizes, and sends via email
"""

import os
from dotenv import load_dotenv
from scraper import scrape_news
from summarizer import summarize_articles
from newsletter import build_html_newsletter
from email_sender import send_email

def main():
    """Main pipeline execution."""
    
    # Load environment variables (for local testing)
    load_dotenv()
    
    print("🚀 Starting Bangla News Pipeline...")
    print("=" * 50)
    
    # Step 1: Scrape news articles
    print("\n📰 Step 1: Scraping news articles...")
    articles = scrape_news()
    
    if not articles:
        print("⚠️  No articles found. Exiting.")
        return
    
    print(f"✅ Found {len(articles)} articles")
    
    # Step 2: Summarize articles
    print("\n🤖 Step 2: Summarizing articles...")
    summarized = summarize_articles(articles)
    print(f"✅ Summarized {len(summarized)} articles")
    
    # Step 3: Build newsletter
    print("\n📝 Step 3: Building newsletter...")
    newsletter = build_html_newsletter(summarized)
    print("✅ Newsletter built")
    
    # Step 4: Send email
    print("\n📧 Step 4: Sending email...")
    logo_path = os.path.join(os.path.dirname(__file__), "Untitled-design-18.png")
    success = send_email(newsletter, logo_path=logo_path)
    
    if success:
        print("\n🎉 Pipeline completed successfully!")
    else:
        print("\n❌ Pipeline completed with errors")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
