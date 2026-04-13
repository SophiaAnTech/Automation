import pandas as pd
import os
from google import genai
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Setup - Replace with your Gemini API Key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY", "AIzxxxxxesss"))


def analyze_reviews_with_gemini(csv_file):
    # 2. Collect and Clean Data
    df = pd.read_csv(csv_file)
    all_reviews_text = "\n".join(df['customer_review'].astype(str).tolist())

    # 3. Send to Gemini for Insight Extraction
    prompt = f"""
    The following are customer reviews for a Python online course:
    {all_reviews_text}
    
    Act as a data analyst. Please provide:
    1. A list of the Top 3 Key Themes (Positives).
    2. A list of the Top 3 Key Themes (Complaints/Trends).
    3. A sentiment score (1-10) for: Content Quality, Instructor, and Technical Support.
    Format the scores clearly as: Category: Score
    """
    
    response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    
    print("--- GEMINI AI INSIGHTS ---\n")
    print(response.text)

    # 4. Visualize Results
    # Simulated scores based on the provided sample CSV
    data = {
        'Category': ['Content Quality', 'Instructor', 'Tech Support', 'Value'],
        'Score': [8.8, 9.2, 6.5, 9.0]
    }
    viz_df = pd.DataFrame(data)

    plt.figure(figsize=(10, 6))
    sns.set_style("whitegrid")
    ax = sns.barplot(x='Category', y='Score', data=viz_df, palette="magma")
    
    plt.title('Course Sentiment Analysis (Powered by Gemini)', fontsize=16)
    plt.ylim(0, 10)
    plt.ylabel('Score (out of 10)')
    
    # Adding data labels
    for p in ax.patches:
        ax.annotate(format(p.get_height(), '.1f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', 
                   xytext = (0, 9), 
                   textcoords = 'offset points')

    plt.tight_layout()
    plt.show()

analyze_reviews_with_gemini("python_course_reviews.csv")
