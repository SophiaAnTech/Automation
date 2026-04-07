!pip install feedparser google-generativeai requests

import feedparser
import requests
from datetime import datetime
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key='xxxxxxx') #replace this with your api key
model = genai.GenerativeModel('gemini-2.5-flash')

# RSS feeds
TECHCRUNCH_RSS = 'https://techcrunch.com/feed/'
VERGE_RSS = 'https://www.theverge.com/rss/index.xml'

def fetch_articles(rss_url, source_name, limit=5):
    """Fetch latest articles from RSS feed"""
    feed = feedparser.parse(rss_url)
    articles = []
    
    for entry in feed.entries[:limit]:
        articles.append({
            'source': source_name,
            'title': entry.title,
            'link': entry.link,
            'published': entry.get('published', 'N/A')
        })
    
    return articles

def summarize_with_gemini(articles):
    """Send articles to Gemini for summarization and parse response"""
    # Prepare article text with numbers
    article_text = ""
    for i, article in enumerate(articles, 1):
        article_text += f"\n{i}. {article['title']}\n   Source: {article['source']}\n"
    
    # Prompt for Gemini
    prompt = f"""You are a tech news analyst. For each of these {len(articles)} articles, provide:
1. A 2-sentence summary
2. One key insight (max 10 words)

Format your response EXACTLY like this for each article:

**Article 1**
Summary: [2 sentences here]
Key insight: [short phrase here]

**Article 2**
Summary: [2 sentences here]
Key insight: [short phrase here]

And so on.

Articles:
{article_text}"""
    
    # Get summary from Gemini
    response = model.generate_content(prompt)
    
    # Parse response and add to articles
    summaries = parse_gemini_response(response.text, len(articles))
    
    # Add summaries to articles
    for i, article in enumerate(articles):
        if i < len(summaries):
            article['ai_summary'] = summaries[i]['summary']
            article['ai_insight'] = summaries[i]['insight']
        else:
            article['ai_summary'] = "Summary not available"
            article['ai_insight'] = "N/A"
    
    return articles

def parse_gemini_response(response_text, num_articles):
    """Parse Gemini response to extract summaries and insights"""
    summaries = []
    
    # Split by "**Article" markers
    sections = response_text.split('**Article')[1:]  # Skip first empty part
    
    for section in sections[:num_articles]:
        try:
            # Extract summary
            if 'Summary:' in section:
                summary_part = section.split('Summary:')[1].split('Key insight:')[0].strip()
            else:
                summary_part = "Summary not available"
            
            # Extract key insight
            if 'Key insight:' in section:
                insight_part = section.split('Key insight:')[1].strip()
                # Remove any ** at the end
                insight_part = insight_part.replace('**', '').strip()
            else:
                insight_part = "N/A"
            
            summaries.append({
                'summary': summary_part,
                'insight': insight_part
            })
        except:
            summaries.append({
                'summary': "Summary not available",
                'insight': "N/A"
            })
    
    return summaries

def create_html_dashboard(articles):
    """Create HTML dashboard with integrated summaries"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Tech News Dashboard - {datetime.now().strftime('%B %d, %Y')}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            margin: 0 0 10px 0;
            font-size: 32px;
        }}
        .header p {{
            margin: 0;
            opacity: 0.9;
        }}
        .articles {{
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .article {{
            margin-bottom: 30px;
            padding-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .article:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .source {{
            display: inline-block;
            background: #667eea;
            color: white;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 12px;
        }}
        .article h3 {{
            margin: 8px 0 12px 0;
            font-size: 22px;
            line-height: 1.4;
        }}
        .article a {{
            color: #2c3e50;
            text-decoration: none;
            transition: color 0.2s;
        }}
        .article a:hover {{
            color: #667eea;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
            margin-bottom: 16px;
        }}
        .ai-summary {{
            background: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            margin-top: 12px;
            border-left: 4px solid #667eea;
        }}
        .ai-summary p {{
            margin: 0 0 12px 0;
            line-height: 1.6;
            color: #2c3e50;
        }}
        .ai-summary p:last-child {{
            margin-bottom: 0;
        }}
        .insight {{
            display: inline-block;
            background: #fff3cd;
            color: #856404;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 13px;
            font-weight: 600;
            margin-top: 8px;
        }}
        .insight::before {{
            content: "💡 ";
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 Tech & AI News Dashboard</h1>
        <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
    </div>
    
    <div class="articles">
"""
    
    for article in articles:
        html += f"""
        <div class="article">
            <span class="source">{article['source']}</span>
            <h3><a href="{article['link']}" target="_blank">{article['title']}</a></h3>
            <p class="meta">📅 Published: {article['published']}</p>
            <div class="ai-summary">
                <p><strong>Summary:</strong> {article.get('ai_summary', 'Summary not available')}</p>
                <span class="insight">{article.get('ai_insight', 'N/A')}</span>
            </div>
        </div>
"""
    
    html += """
    </div>
</body>
</html>
"""
    
    return html

def main():
    print("🔄 Fetching latest tech news...")
    
    # Fetch articles
    techcrunch_articles = fetch_articles(TECHCRUNCH_RSS, 'TechCrunch', limit=5)
    verge_articles = fetch_articles(VERGE_RSS, 'The Verge', limit=5)
    all_articles = techcrunch_articles + verge_articles
    
    print(f"✅ Fetched {len(all_articles)} articles")
    
    # Summarize with Gemini and add to articles
    print("🤖 Generating AI summaries with Gemini...")
    articles_with_summaries = summarize_with_gemini(all_articles)
    print("✅ Summaries generated")
    
    # Create dashboard
    print("📊 Creating dashboard...")
    html_dashboard = create_html_dashboard(articles_with_summaries)
    
    # Save to file
    filename = f"tech_news_dashboard_{datetime.now().strftime('%Y%m%d')}.html"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_dashboard)
    print(f"✅ Dashboard saved: {filename}")
    
    # Open in browser
    import webbrowser
    webbrowser.open(filename)

if __name__ == "__main__":
    main()

    
'''
# schedule daily run 

# on mac - edit crontab
crontab -e

# Add this line (runs daily at 8 AM)
0 8 * * * /usr/bin/python3 /path/to/your/script.py

# on windows - use Task Scheduler 
Create task that runs python script.py daily at 8 AM
'''
    
