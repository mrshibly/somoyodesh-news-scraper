# 📰 Shomoy o desh News Scraper

Automated daily Bangla news reporter for **সময় ও দেশ** (somoyodesh.com). It scrapes, summarizes in professional journalism tone, and delivers a branded newsletter via email.

> **Tagline:** দেশ ও মানুষের কথা বলি

## 🎯 Features

- **Professional Reporting:** Articles are summarized into a cohesive "News Report" format by AI.
- **Journalism Tone:** Enforced strictly Bangla reports and titles with a professional journalism style.
- **Premium Newsletter:** Red/Green/White themed HTML newsletter with mobile-responsive design.
- **Multi-Recipient Support:** Deliver to multiple email addresses simultaneously.
- **Resilient AI Pipeline:** Dual-API setup (Gemini + Groq fallback) with robust rate-limit handling.
- **Automated Execution:** Fully integrated with GitHub Actions for daily delivery.

## 🚀 Setup

### 1. Credentials Setup

#### Gmail App Password

1. Enable 2FA on your Google Account.
2. Generate an [App Password](https://myaccount.google.com/apppasswords) for "Mail".

#### API Keys

1. **Google Gemini:** Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. **Groq:** Get an API key from [Groq Console](https://console.groq.com/keys).
3. **Tavily:** Get a search API key from [Tavily AI](https://tavily.com/).

### 2. GitHub Configuration

1. **Push to GitHub:** Fork or push this repository to your account.
2. **Add Secrets:** Go to **Settings → Secrets and variables → Actions** and add:
   - `EMAIL`: Your sender Gmail address.
   - `APP_PASSWORD`: Your Gmail app password.
   - `GEMINI_API_KEY`: Your Google Gemini key.
   - `GROQ_API_KEY`: Your Groq key (fallback).
   - `TAVILY_API_KEY`: Your Tavily search key.
   - `RECIPIENT_EMAIL`: Comma-separated list of recipient emails (e.g., `user1@me.com, user2@me.com`).

### 3. Workflow Schedule

The newsletter is sent daily at **9:00 AM Bangladesh Time** (03:00 UTC). You can change this in `.github/workflows/daily-news.yml`.

## 📁 Project Structure

- `main.py`: Orchestrates the scraping, summarization, and emailing.
- `scraper.py`: Handles article discovery via direct scraping and Tavily.
- `summarizer.py`: High-quality Bangla summarization with journalism tone.
- `newsletter.py`: Builds the premium HTML newsletter template.
- `email_sender.py`: Handles multi-recipient email delivery with inline logo.
- `Untitled-design-18.png`: The official agency logo used in the newsletter.

## ⚠️ Requirements

- Python 3.10+
- All dependencies listed in `requirements.txt`.

## 📝 License

MIT
