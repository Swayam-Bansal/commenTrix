import sys
import json
from transformers import pipeline

print(sys.executable)

sentiment = pipeline("sentiment-analysis")


def retrieve_comments(filepath):
    """
    Opens a JSON file, loads its content, and retrieves the "text" field
    from each object, assuming the JSON data is a list of such objects.

    Args:
        filepath (str): The path to the JSON file.

    Returns:
        list: A list of comment texts.
    """
    comments = []
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict) and "text" in item:
                    comments.append(item["text"])
        else:
            print("Error: JSON data is not a list of objects.")

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return comments


def analyze_and_save_comments(input_filepath, output_filepath):
    """
    Retrieves comments from a JSON file, analyzes their sentiment,
    and saves the comments with their sentiment analysis to a new JSON file.

    Args:
        input_filepath (str): The path to the input JSON file.
        output_filepath (str): The path to the output JSON file.
    """
    comments = retrieve_comments(input_filepath)
    if comments:
        analyzed_comments = []
        for comment in comments:
            sentiment_result = sentiment(comment)[0]  # Get the first result
            analyzed_comments.append({
                "comment": comment,
                "sentiment": sentiment_result["label"],
                "score": sentiment_result["score"]
            })

        try:
            with open(output_filepath, "w", encoding="utf-8") as f:
                json.dump(analyzed_comments, f, ensure_ascii=False, indent=4)
            print(f"Analyzed comments saved to {output_filepath}")
        except Exception as e:
            print(f"Error saving analyzed comments: {e}")
    else:
        print("No comments to analyze.")


# Example usage:
input_file = "test/apiyoutube_comments.json"
output_file = "test/analyzed_comments.json"  # Change to your desired output path
analyze_and_save_comments(input_file, output_file)