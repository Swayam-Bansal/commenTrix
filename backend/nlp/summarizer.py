# Summarizes the pipeline
# backend/nlp/summarization_model.py
from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def generate_summary(text: str, max_length=150, min_length=30):
    """
    Generates a summary of the given text using the BART model.
    """
    try:
        if not text:
            return "No text to summarize."
        summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
        return summary
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "Could not generate summary."

if __name__ == "__main__":
    # Example usage
    sample_text = """
        The Orbiter Discovery, STS-128 mission is the 128th mission of the Space Shuttle program,
        and the 33rd flight of Discovery. It launched on August 29, 2009 at 23:59 UTC.
        The seven-member crew is headed by commander Rick Sturckow and pilot Kevin Ford.
        The mission is delivering the Multi-Purpose Logistics Module (MPLM) Leonardo,
        carrying science and storage racks, as well as the Lightweight Multi-Purpose Experiment Support Structure (LMPESS).
        Two spacewalks are planned to install the experiments outside the European Columbus laboratory.
        Guglielmo Verrechia from the European Space Agency (ESA) and Nicole Stott will perform these spacewalks.
        Stott will join the Expedition 20 crew on the International Space Station (ISS) and return on STS-129.
    """
    summary = generate_summary(sample_text)
    print("Original Text:\n", sample_text)
    print("\nSummary:\n", summary)