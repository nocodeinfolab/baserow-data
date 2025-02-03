import json
import matplotlib.pyplot as plt
import pandas as pd
from transformers import pipeline

# Load data from the exported file
with open('data.json', 'r') as file:
    data = json.load(file)

# Initialize Hugging Face sentiment analysis pipeline
classifier = pipeline("sentiment-analysis")

# Analyze data using Hugging Face
analysis_results = []
for row in data['results']:
    text = row['your_text_field']  # Replace with your actual field name
    result = classifier(text)[0]
    analysis_results.append({
        "row_id": row['id'],
        "text": text,
        "sentiment": result['label'],
        "score": result['score']
    })

# Save analysis results to a JSON file
with open('analysis_results.json', 'w') as file:
    json.dump(analysis_results, file, indent=4)

# Generate a chart (example: sentiment distribution)
df = pd.DataFrame(analysis_results)
sentiment_counts = df['sentiment'].value_counts()

plt.figure(figsize=(8, 6))
sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.savefig('chart.png')  # Save the chart as an image
