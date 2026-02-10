import os
import time
from google import genai
from google.genai import types
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def get_gemini_api_key():
    """Get Gemini API key from environment."""
    return os.getenv("GEMINI_API_KEY")

def get_groq_api_key():
    """Get Groq API key from environment."""
    return os.getenv("GROQ_API_KEY")

def summarize_with_gemini(title, text, retries=1):
    """Generate a Bangla news report using Gemini with minimal retries for speed."""
    for attempt in range(retries + 1):
        try:
            api_key = get_gemini_api_key()
            if not api_key: return None
                
            client = genai.Client(api_key=api_key)
            prompt = f"""
            আপনি 'সময় ও দেশ' (somoyodesh.com) নিউজ এজেন্সির একজন পেশাদার সংবাদ প্রতিনিধি (Reporter)। 
            আপনার এজেন্সির মূলমন্ত্র: "দেশ ও মানুষের কথা বলি"।
            
            নিচের সংবাদটি পড়ুন এবং এটি নিয়ে একটি আকর্ষণীয় সংবাদ প্রতিবেদন লিখুন। 
            
            শর্তাবলী:
            ১. মূল শিরোনাম এবং প্রতিবেদন—উভয়ই অবশ্যই সম্পূর্ণ বাংলায় হতে হবে।
            ২. রিপোর্টটি অন্তত ৩-৪টি বাক্যের একটি সুন্দর অনুচ্ছেডে লিখুন।
            ৩. টোনটি তথ্যবহুল এবং সংবাদসুলভ হতে হবে।
            ৪. নিচের ফরমেটে উত্তর দিন:
            শিরোনাম: [বাংলার শিরোনাম]
            প্রতিবেদন: [বাংলার প্রতিবেদন]
            
            মূল শিরোনাম: {title}
            সংবাদ (Source Text): {text}
            """
            
            response = client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            
            output = response.text.strip()
            if output:
                print("  ✓ Gemini API")
                return output
            return None
            
        except Exception as e:
            err_str = str(e)
            if ("429" in err_str or "exhausted" in err_str.lower()) and attempt < retries:
                print(f"  ⏳ Gemini rate limit, quick retry in 5s...")
                time.sleep(5)
                continue
            print(f"  ⚠️  Gemini failed: {err_str[:50]}...")
            return None

def summarize_with_groq(title, text, retries=1):
    """Generate a Bangla news report using Groq with minimal retries."""
    for attempt in range(retries + 1):
        try:
            api_key = get_groq_api_key()
            if not api_key: return None
                
            client = Groq(api_key=api_key)
            prompt = f"""
            আপনি 'সময় ও দেশ' (somoyodesh.com) নিউজ এজেন্সির একজন পেশাদার সংবাদ প্রতিনিধি (Reporter)। 
            আপনার এজেন্সির মূলমন্ত্র: "দেশ ও মানুষের কথা বলি"।
            
            নিচের সংবাদটি পড়ুন এবং এটি নিয়ে একটি আকর্ষণীয় সংবাদ প্রতিবেদন লিখুন। 
            
            শর্তাবলী:
            ১. মূল শিরোনাম এবং প্রতিবেদন—উভয়ই অবশ্যই সম্পূর্ণ বাংলায় হতে হবে।
            ২. রিপোর্টটি অন্তত ৩-৪টি বাক্যের একটি সুন্দর অনুচ্ছেদে লিখুন।
            ৩. টোনটি হবে পেশাদার সংবাদ প্রতিনিধির মতো।
            ৪. নিচের ফরমেটে উত্তর দিন:
            শিরোনাম: [বাংলার শিরোনাম]
            প্রতিবেদন: [বাংলার প্রতিবেদন]
            
            মূল শিরোনাম: {title}
            সংবাদ (Source Text): {text}
            """
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a professional reporter. Respond strictly in Bangla."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            output = response.choices[0].message.content.strip()
            if output:
                print("  ✓ Groq API (fallback)")
                return output
            return None
            
        except Exception as e:
            err_str = str(e)
            if ("429" in err_str or "rate_limit" in err_str.lower()) and attempt < retries:
                print(f"  ⏳ Groq rate limit, quick retry in 3s...")
                time.sleep(3)
                continue
            print(f"  ⚠️  Groq failed: {err_str[:50]}...")
            return None

def fallback_summarize(text):
    """Simple fallback: Use first 2-3 sentences."""
    sentences = text.split('।')
    summary = '।'.join(sentences[:2]).strip()
    if summary:
        summary += '।'
    else:
        summary = text[:150] + '...'
    print("  ⚠️  Using simple truncation (fast fallback)")
    return summary

def process_article(article_title, article_text):
    """Process an article to ensure title and report are in Bangla."""
    # Try Gemini
    result = summarize_with_gemini(article_title, article_text)
    
    # Try Groq
    if not result:
        result = summarize_with_groq(article_title, article_text)
        
    if result:
        lines = result.split('\n')
        final_title = article_title
        final_report = ""
        
        for line in lines:
            line_clean = line.strip()
            if "শিরোনাম:" in line_clean or "শিরোনাম :" in line_clean:
                final_title = line_clean.split(":", 1)[1].strip()
            elif "প্রতিবেদন:" in line_clean or "প্রতিবেদন :" in line_clean:
                final_report = line_clean.split(":", 1)[1].strip()
            elif line_clean and not final_report and not any(tag in line_clean for tag in ["শিরোনাম:", "শিরোনাম :", "সংবাদ:", "সংবাদ :"]):
                final_report += line_clean + " "
        
        if final_report:
            final_title = final_title.replace("**", "").replace("#", "").strip()
            final_report = final_report.replace("**", "").strip()
            return final_title, final_report

    return article_title, fallback_summarize(article_text)

def summarize_articles(articles):
    """Summarize articles with minimal delay for high speed."""
    summarized = []
    
    for i, article in enumerate(articles, 1):
        print(f"Processing article {i}/{len(articles)}: {article['title'][:50]}...")
        
        title, report = process_article(article["title"], article["text"])
        
        summarized.append({
            "title": title,
            "summary": report,
            "url": article["url"]
        })
        
        # Reduced delay from 6s to 1s for much faster execution
        time.sleep(1)
    
    return summarized

if __name__ == "__main__":
    sample = "রাজধানী ঢাকায় মেট্রো রেলের নতুন লাইন উদ্বোধন করা হয়েছে।"
    title, report = process_article("Metro Update", sample)
    print(f"\nTitle: {title}\nReport: {report}")
