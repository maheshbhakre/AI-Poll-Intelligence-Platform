"""
Text Feedback Analysis Module for AI Poll Results Visualizer.
Processes survey text comments:
  - Character and word length statistics
  - Stopword filtering and most frequent word extraction
  - Sentiment polarity classification (TextBlob)
Generates:
  - outputs/text_feedback_report.csv
  - outputs/sentiment_summary.csv
"""

import os
import re
import pandas as pd
from collections import Counter

# Standard stopwords list without heavy external downloads
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can",
    "can't", "cannot", "could", "did", "do", "does", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him", "himself",
    "his", "how", "i", "if", "in", "into", "is", "isn't", "it", "its", "itself", "let's", "me", "more", "most",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "she", "should", "so", "some", "such", "than", "that", "the", "their",
    "theirs", "them", "themselves", "then", "there", "these", "they", "this", "those", "through", "to", "too", "under",
    "until", "up", "very", "was", "wasn't", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "with", "won't", "would", "you", "your", "yours", "yourself", "yourselves"
}


def clean_tokens(text):
    """Tokenize and filter alphanumeric words without stopwords."""
    words = re.findall(r'\b[a-zA-Z]{2,}\b', str(text).lower())
    return [w for w in words if w not in STOPWORDS]


def compute_sentiment(text):
    """Computes sentiment score and label using TextBlob with fallback."""
    try:
        from textblob import TextBlob
        polarity = TextBlob(str(text)).sentiment.polarity
    except Exception:
        polarity = 0.0
        
    if polarity > 0.05:
        return "Positive", polarity
    elif polarity < -0.05:
        return "Negative", polarity
    else:
        return "Neutral", polarity


def run_text_analysis(data_path="data/cleaned_poll_data.csv",
                      feedback_report_path="outputs/text_feedback_report.csv",
                      sentiment_summary_path="outputs/sentiment_summary.csv"):
    """
    Analyzes text comments from survey data and exports structured text reports.
    """
    if not os.path.exists(data_path):
        data_path = "data/poll_data.csv"
        
    df = pd.read_csv(data_path)
    if "Feedback" not in df.columns:
        df["Feedback"] = "No feedback provided"

    feedbacks = df["Feedback"].fillna("").astype(str)
    
    # 1. Feedback length statistics
    char_lengths = feedbacks.apply(len)
    word_lengths = feedbacks.apply(lambda s: len(s.split()))

    total_comments = len(feedbacks)
    non_empty = int((char_lengths > 0).sum())
    mean_char_len = round(float(char_lengths.mean()), 2)
    median_char_len = round(float(char_lengths.median()), 2)
    min_char_len = int(char_lengths.min())
    max_char_len = int(char_lengths.max())

    mean_word_count = round(float(word_lengths.mean()), 2)
    max_word_count = int(word_lengths.max())

    # 2. Token frequency analysis
    all_tokens = []
    for comment in feedbacks:
        all_tokens.extend(clean_tokens(comment))
        
    word_freq = Counter(all_tokens)
    top_10_words = word_freq.most_common(10)

    # Build text feedback report rows
    report_rows = [
        {"Section": "Summary Statistics", "Metric": "Total Feedback Submissions", "Value": str(total_comments)},
        {"Section": "Summary Statistics", "Metric": "Non-Empty Submissions", "Value": str(non_empty)},
        {"Section": "Summary Statistics", "Metric": "Average Character Length", "Value": str(mean_char_len)},
        {"Section": "Summary Statistics", "Metric": "Median Character Length", "Value": str(median_char_len)},
        {"Section": "Summary Statistics", "Metric": "Min Character Length", "Value": str(min_char_len)},
        {"Section": "Summary Statistics", "Metric": "Max Character Length", "Value": str(max_char_len)},
        {"Section": "Summary Statistics", "Metric": "Average Word Count", "Value": str(mean_word_count)},
        {"Section": "Summary Statistics", "Metric": "Total Clean Vocabulary Count", "Value": str(len(set(all_tokens)))}
    ]

    for rank, (word, count) in enumerate(top_10_words, start=1):
        pct = round((count / len(all_tokens) * 100), 2) if all_tokens else 0.0
        report_rows.append({
            "Section": "Top Keywords",
            "Metric": f"Keyword #{rank}: '{word}'",
            "Value": f"{count} occurrences ({pct}%)"
        })

    report_df = pd.DataFrame(report_rows)
    os.makedirs(os.path.dirname(feedback_report_path), exist_ok=True)
    report_df.to_csv(feedback_report_path, index=False)

    # 3. Sentiment Analysis
    sentiments = []
    polarities = []
    for comment in feedbacks:
        s_label, s_pol = compute_sentiment(comment)
        sentiments.append(s_label)
        polarities.append(s_pol)

    df["Sentiment"] = sentiments
    df["Polarity"] = polarities

    sent_counts = df["Sentiment"].value_counts()
    sent_rows = []
    for sentiment_label in ["Positive", "Neutral", "Negative"]:
        cnt = int(sent_counts.get(sentiment_label, 0))
        pct = round((cnt / total_comments * 100), 2) if total_comments > 0 else 0.0
        subset_polarity = df[df["Sentiment"] == sentiment_label]["Polarity"]
        avg_pol = round(float(subset_polarity.mean()), 3) if not subset_polarity.empty else 0.0
        
        sent_rows.append({
            "Sentiment Class": sentiment_label,
            "Count": cnt,
            "Percentage Share": f"{pct}%",
            "Average Polarity": avg_pol
        })

    sent_df = pd.DataFrame(sent_rows)
    os.makedirs(os.path.dirname(sentiment_summary_path), exist_ok=True)
    sent_df.to_csv(sentiment_summary_path, index=False)

    return report_df, sent_df


if __name__ == "__main__":
    print("=" * 60)
    print("Executing Text Feedback & Sentiment Analysis...")
    print("=" * 60)
    r_df, s_df = run_text_analysis()
    print(r_df.to_string(index=False))
    print("\n" + "=" * 60)
    print("Sentiment Summary:")
    print("=" * 60)
    print(s_df.to_string(index=False))
    print("\n[SUCCESS] Generated outputs/text_feedback_report.csv and outputs/sentiment_summary.csv")
