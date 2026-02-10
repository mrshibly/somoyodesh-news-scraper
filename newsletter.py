from datetime import datetime

def build_html_newsletter(summarized_articles):
    """Build a premium HTML newsletter for 'সময় ও দেশ' (Somoy o Desh)."""
    
    now = datetime.now()
    date_str = now.strftime("%d %B, %Y")
    
    article_cards = ""
    for i, item in enumerate(summarized_articles, 1):
        title = item.get("title", "শিরোনাম নেই")
        summary = item.get("summary", "প্রতিবেদন পাওয়া যায়নি")
        url = item.get("url", "#")
        source_name = "সংবাদ সূত্র"
        if "prothomalo" in url: source_name = "প্রথম আলো"
        elif "bbc" in url: source_name = "বিবিসি বাংলা"
        elif "thedailystar" in url: source_name = "ডেইলি স্টার"
        elif "jugantor" in url: source_name = "যুগান্তর"

        article_cards += f"""
        <div class="card">
            <div class="card-header">
                <span class="badge" style="background-color: rgba(0, 106, 78, 0.1); color: #006A4E;">{source_name}</span>
                <span class="count">#{i}</span>
            </div>
            <h2 class="article-title">{title}</h2>
            <div class="divider"></div>
            <p class="article-summary">{summary}</p>
            <a href="{url}" class="read-more">বিস্তারিত পড়ুন &rarr;</a>
        </div>
        """

    html_template = f"""
    <!DOCTYPE html>
    <html lang="bn">
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Hind+Siliguri:wght@400;600;700&display=swap');
            
            body {{
                font-family: 'Hind Siliguri', Arial, sans-serif;
                background-color: #f7fafc;
                margin: 0;
                padding: 20px;
                color: #2d3748;
                line-height: 1.6;
            }}
            .container {{
                max-width: 650px;
                margin: 0 auto;
                background: white;
                border-radius: 16px;
                overflow: hidden;
                box-shadow: 0 15px 35px rgba(0,0,0,0.08);
                border: 1px solid #e2e8f0;
            }}
            .header {{
                background-color: #ffffff;
                padding: 40px 20px 25px;
                text-align: center;
                border-bottom: 4px solid #006A4E;
            }}
            .logo {{
                max-width: 250px;
                height: auto;
            }}
            .date-badge {{
                display: inline-block;
                background: #E03C31;
                color: white;
                padding: 4px 18px;
                border-radius: 20px;
                font-size: 14px;
                margin-top: 15px;
                font-weight: 600;
            }}
            .content {{
                padding: 35px 25px;
            }}
            .card {{
                background: #ffffff;
                border: 1px solid #edf2f7;
                border-radius: 12px;
                padding: 24px;
                margin-bottom: 24px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.02);
            }}
            .card-header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 12px;
            }}
            .badge {{
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }}
            .count {{
                color: #cbd5e0;
                font-weight: 700;
                font-size: 14px;
            }}
            .article-title {{
                font-size: 24px;
                margin: 0 0 12px;
                color: #2d3748;
                line-height: 1.4;
            }}
            .divider {{
                height: 4px;
                width: 50px;
                background: #E03C31;
                margin-bottom: 15px;
                border-radius: 2px;
            }}
            .article-summary {{
                font-size: 18px;
                color: #4a5568;
                margin-bottom: 20px;
                text-align: justify;
                line-height: 1.8;
            }}
            .read-more {{
                display: inline-block;
                color: #006A4E;
                text-decoration: none;
                font-weight: 700;
                font-size: 15px;
                border: 1px solid #006A4E;
                padding: 8px 18px;
                border-radius: 6px;
                transition: all 0.2s;
            }}
            .footer {{
                background: #f8fafc;
                padding: 40px 20px;
                text-align: center;
                font-size: 14px;
                color: #718096;
                border-top: 1px solid #e2e8f0;
            }}
            .social-icons-footer {{
                margin-bottom: 25px;
            }}
            .social-icon-btn {{
                background-color: #006A4E;
                color: white !important;
                padding: 10px 20px;
                text-decoration: none;
                border-radius: 25px;
                font-weight: 700;
                margin: 0 5px;
                display: inline-block;
                transition: background 0.3s;
            }}
            .website-link {{
                color: #E03C31;
                font-weight: 700;
                text-decoration: none;
                font-size: 18px;
            }}
            .tagline-footer {{
                color: #006A4E;
                font-size: 18px;
                font-weight: 700;
                margin: 0 0 15px;
            }}
            .headline {{
                font-size: 26px;
                color: #1a202c;
                margin-bottom: 30px;
                text-align: center;
                font-weight: 700;
                border-bottom: 2px solid #edf2f7;
                padding-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <img src="cid:logo" alt="সময় ও দেশ" class="logo">
                <br>
                <div class="date-badge">{date_str}</div>
            </div>
            <div class="content">
                <h2 class="headline">📰 আজকের সংবাদপত্র প্রতিবেদন</h2>
                {article_cards if article_cards else '<p style="text-align:center;">আজ কোনো সংবাদ পাওয়া যায়নি।</p>'}
            </div>
            <div class="footer">
                <p class="tagline-footer">দেশ ও মানুষের কথা বলি</p>
                <div class="social-icons-footer">
                    <a href="https://www.facebook.com/somoyodeshnews/" class="social-icon-btn">ফেসবুক পেজ</a>
                    <a href="https://somoyodesh.com" class="social-icon-btn">আমাদের ওয়েবসাইট</a>
                </div>
                <p>© {now.year} <a href="https://somoyodesh.com" class="website-link">somoyodesh.com</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template

if __name__ == "__main__":
    # Test
    print("Newsletter template refined.")
