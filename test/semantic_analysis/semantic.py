import re
import nltk
from sentence_transformers import SentenceTransformer, util
from transformers import pipeline
import torch
import numpy as np
import json
import sys

import os
print("Current Working Directory:", os.getcwd())

def download_nltk_data():
    """Checks for punkt tokenizer data and downloads it if not present."""
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK 'punkt' data...")
        nltk.download('punkt')


def load_transcript_from_file(transcript_file_path):
    """Loads transcript from a text file."""
    print(f"Loading transcript from {transcript_file_path}...")
    try:
        with open(transcript_file_path, 'r', encoding='utf-8') as f:
            raw_transcript = f.read()
        print("Transcript loaded successfully.")
        return raw_transcript
    except FileNotFoundError:
        print(f"Error: The transcript file {transcript_file_path} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading {transcript_file_path}: {e}")
        sys.exit(1)


def load_comments_from_json(json_file_path):
    """Loads comments from a JSON file."""
    print(f"Loading comments from {json_file_path}...")
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            comments_data = json.load(f)
            comments = [item['text'] for item in comments_data if 'text' in item]
            if not comments:
                print(f"Warning: No comments found with a 'text' field in {json_file_path}.")
            print(f"Successfully loaded {len(comments)} comments.")
            return comments_data, comments
    except FileNotFoundError:
        print(f"Error: The file {json_file_path} was not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}. Check the file format.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading {json_file_path}: {e}")
        sys.exit(1)


def preprocess_text(text):
    """Basic text cleaning."""
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    print (f"successfully preprocessed text.")
    return text

def generate_embeddings(transcript_segments_processed, comments_processed):
    """Generates embeddings for transcript and comments."""
    print("\nLoading embedding model...")
    embedder = SentenceTransformer('all-MiniLM-L6-v2')
    if comments_processed:
        print("Generating embeddings...")
        transcript_embeddings = embedder.encode(transcript_segments_processed, convert_to_tensor=True)
        comment_embeddings = embedder.encode(comments_processed, convert_to_tensor=True)
        print("Embeddings generated.")
        return transcript_embeddings, comment_embeddings
    else:
        print("Skipping embedding generation as no comments were loaded.")
        return None, None


def link_comments_to_transcript(comment_embeddings, transcript_embeddings):
    """Links comments to transcript using semantic similarity."""
    if comment_embeddings is not None and transcript_embeddings is not None:
        print("\nLinking comments to transcript segments...")
        similarity_results = util.semantic_search(comment_embeddings, transcript_embeddings, top_k=1)
        return similarity_results
    else:
        print("Skipping linking as embeddings were not generated.")
        return []


def analyze_sentiment(comments):
    """Performs sentiment analysis on comments."""
    sentiments = []
    if comments:
        print("\nLoading sentiment analysis model...")
        device = 0 if torch.cuda.is_available() else -1
        sentiment_analyzer = pipeline("sentiment-analysis",model="finiteautomata/bertweet-base-sentiment-analysis", device=device)
        print("Analyzing sentiment of comments...")
        for i, comment_text in enumerate(comments):
            try:
                if not isinstance(comment_text, str):
                    raise TypeError("Comment text is not a string")
                result = sentiment_analyzer(comment_text[:512])
                sentiments.append(result[0])
                print(f"analyzed comment {i}") # <--- Added print statement
            except Exception as e:
                print(f"Could not analyze sentiment for comment {i}: '{comment_text[:50]}...'. Error: {e}")
                print(f"Comment that caused error: {comment_text}") # <--- Added print statement
                sentiments.append({'label': 'ERROR', 'score': 0.0})
        print("Sentiment analysis complete.")
    else:
        print("Skipping sentiment analysis as no comments were loaded.")
    return sentiments


def combine_and_display_results(comments_data, similarity_results, sentiments, transcript_segments, comments_processed):
    """Combines and displays analysis results."""
    results = []
    if comments_data and similarity_results and sentiments:
        print("\n--- Analysis Results ---")
        for i, comment_obj in enumerate(comments_data):
            if i < len(similarity_results) and i < len(sentiments) and i < len(comments_processed):
                original_text = comment_obj.get("text", "[Missing Text]")
                author = comment_obj.get("author", "[No Author]")
                published_at = comment_obj.get("publishedAt", "[No Date]")
                processed_text = comments_processed[i]
                linked_segment_index = similarity_results[i][0]['corpus_id']
                similarity_score = similarity_results[i][0]['score']
                linked_segment = transcript_segments[linked_segment_index]
                sentiment_label = sentiments[i]['label']
                sentiment_score = sentiments[i]['score']
                results.append({
                    "comment_original": original_text,
                    "comment_author": author,
                    "comment_published_at": published_at,
                    "comment_processed": processed_text,
                    "linked_transcript_segment": linked_segment.strip(),
                    "similarity_score": round(similarity_score, 4),
                    "sentiment_label": sentiment_label,
                    "sentiment_score": round(sentiment_score, 4)
                })
            else:
                print(f"Warning: Skipping result combination for comment index {i} due to mismatched list lengths.")
        for res in results:
            print(f"\nComment: \"{res['comment_original']}\" (by {res['comment_author']} at {res['comment_published_at']})")
            print(f"  -> Linked Transcript Segment (Score: {res['similarity_score']}): \"{res['linked_transcript_segment']}\"")
            print(f"  -> Sentiment: {res['sentiment_label']} (Score: {res['sentiment_score']})")
        return results
    else:
        if not comments_data:
            print("\nNo comments were loaded, cannot display results.")
        else:
            print("\nAnalysis could not be fully completed (check errors above), cannot display results.")
        return []

def save_sentiment_to_json(results):
    """Saves sentiment analysis results to a JSON file."""
    if results:
        sentiment_data = [{"comment": res["comment_original"], "sentiment": {"label": res["sentiment_label"], "score": res["sentiment_score"]}} for res in results]
        sentiment_json_path = "test/analyzed_comments.json"
        try:
            with open(sentiment_json_path, 'w', encoding='utf-8') as f:
                json.dump(sentiment_data, f, ensure_ascii=False, indent=4)
            print(f"\nSentiment analysis saved to {sentiment_json_path}")
        except Exception as e:
            print(f"Error saving sentiment analysis to JSON: {e}")
    else:
        print("\nNo sentiment data to save.")

def main():
    """Main function to orchestrate the analysis."""

    download_nltk_data()
    raw_transcript = load_transcript_from_file('/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/HACKPSU/commenTrix/test/api/transcript2.txt')
    comments_data, comments = load_comments_from_json('/Users/aviralbansal/Library/CloudStorage/OneDrive-ThePennsylvaniaStateUniversity/HACKPSU/commenTrix/test/apiyoutube_comments.json')

    transcript_segments = nltk.sent_tokenize(raw_transcript)
    transcript_segments_processed = [preprocess_text(seg) for seg in transcript_segments if seg.strip()]
    comments_processed = [preprocess_text(comment) for comment in comments]

    transcript_embeddings, comment_embeddings = generate_embeddings(transcript_segments_processed, comments_processed)
    similarity_results = link_comments_to_transcript(comment_embeddings, transcript_embeddings)
    sentiments = analyze_sentiment(comments)
    results = combine_and_display_results(comments_data, similarity_results, sentiments, transcript_segments, comments_processed)
    save_sentiment_to_json(results)
    print("\n--- End of Analysis ---")

if __name__ == "__main__":
    main()