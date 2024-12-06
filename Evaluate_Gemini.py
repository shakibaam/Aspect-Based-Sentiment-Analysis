import xml.etree.ElementTree as ET
import json
from sklearn.metrics import precision_score, recall_score, f1_score

# Function to parse the XML file and convert it to the desired JSON format
def xml_to_json(xml_file, json_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Initialize a list to store sentence entries
    sentences_data = []
    
    # Iterate over sentences in the XML
    for sentence in root.findall('sentence'):
        sentence_text = sentence.find('text').text
        aspects = {}
        
        # Find aspect terms
        aspect_terms_element = sentence.find('aspectTerms')
        if aspect_terms_element is not None:
            for aspect_term in aspect_terms_element.findall('aspectTerm'):
                term = aspect_term.get('term')
                polarity = aspect_term.get('polarity')
                aspects[term] = polarity
        
        # Append the sentence and its aspects to the data list
        sentences_data.append({
            "Sentence": sentence_text,
            "Aspects": aspects
        })
    
    # Write the JSON data to a file
    with open(json_file, 'w') as f:
        json.dump(sentences_data, f, indent=4)
    print(f"JSON file saved to {json_file}")

# Specify input XML file and output JSON file
xml_file = "laptops-trial.xml"  # Replace with the path to your XML file
json_file = "laptops-trial.json"  # Replace with the desired output JSON file name



def compare_json_files(ground_truth_file, predictions_file):
    import json

    # Load the JSON files
    with open(ground_truth_file, 'r') as gt_file:
        ground_truth_data = json.load(gt_file)
    
    with open(predictions_file, 'r') as pred_file:
        predictions_data = json.load(pred_file)

    # Initialize metrics
    total_aspects = 0
    total_predicted_aspects = 0
    correct_aspects = 0
    correct_aspect_sentiments = 0

    # For separate accuracy calculations
    aspect_correct_sentences = 0  # Correctly extracted all aspects in a sentence
    sentiment_correct_sentences = 0  # Correctly predicted sentiments for all aspects in a sentence
    total_sentences = len(ground_truth_data)

    mismatched_sentences = []

    for gt_sentence, pred_sentence in zip(ground_truth_data, predictions_data):
        gt_aspects = gt_sentence.get("Aspects", {})
        pred_aspects = pred_sentence.get("Aspects", {})

        # For calculating metrics
        total_aspects += len(gt_aspects)
        total_predicted_aspects += len(pred_aspects)

        aspect_correct = True  # Flag for aspect extraction correctness
        sentiment_correct = True  # Flag for sentiment correctness

        for aspect, sentiment in gt_aspects.items():
            if aspect in pred_aspects:
                correct_aspects += 1
                if pred_aspects[aspect] == sentiment:
                    correct_aspect_sentiments += 1
                else:
                    sentiment_correct = False
            else:
                aspect_correct = False

        # Check if aspects and sentiments match completely
        if aspect_correct and len(gt_aspects) == len(pred_aspects):
            aspect_correct_sentences += 1
        if sentiment_correct and aspect_correct and len(gt_aspects) == len(pred_aspects):
            sentiment_correct_sentences += 1

        # Collect mismatched sentences
        if not (aspect_correct and sentiment_correct):
            mismatched_sentences.append({
                "Sentence": gt_sentence["Sentence"],
                "Ground Truth": gt_aspects,
                "Prediction": pred_aspects
            })

    # Calculate sentence-level accuracy for each task
    aspect_accuracy = aspect_correct_sentences / total_sentences if total_sentences > 0 else 0
    sentiment_accuracy = sentiment_correct_sentences / total_sentences if total_sentences > 0 else 0

    # Calculate precision, recall, and F1 for aspect detection
    aspect_precision = correct_aspects / total_predicted_aspects if total_predicted_aspects > 0 else 0
    aspect_recall = correct_aspects / total_aspects if total_aspects > 0 else 0
    aspect_f1 = (
        2 * aspect_precision * aspect_recall / (aspect_precision + aspect_recall)
        if (aspect_precision + aspect_recall) > 0 else 0
    )

    # Calculate precision, recall, and F1 for sentiment analysis
    sentiment_precision = correct_aspect_sentiments / total_predicted_aspects if total_predicted_aspects > 0 else 0
    sentiment_recall = correct_aspect_sentiments / total_aspects if total_aspects > 0 else 0
    sentiment_f1 = (
        2 * sentiment_precision * sentiment_recall / (sentiment_precision + sentiment_recall)
        if (sentiment_precision + sentiment_recall) > 0 else 0
    )

    # Print results
    print("Aspect Extraction Accuracy:")
    print(f"  Aspect Sentence Accuracy: {aspect_accuracy:.2f}")

    print("\nAspect Sentiment Accuracy:")
    print(f"  Sentiment Sentence Accuracy: {sentiment_accuracy:.2f}")

    print("\nAspect Detection Metrics:")
    print(f"  Precision: {aspect_precision:.2f}")
    print(f"  Recall: {aspect_recall:.2f}")
    print(f"  F1-Score: {aspect_f1:.2f}")

    print("\nAspect Sentiment Metrics:")
    print(f"  Precision: {sentiment_precision:.2f}")
    print(f"  Recall: {sentiment_recall:.2f}")
    print(f"  F1-Score: {sentiment_f1:.2f}")

    if mismatched_sentences:
        print("\nMismatched Sentences:")
        for mismatch in mismatched_sentences:
            print(f"Sentence: {mismatch['Sentence']}")
            print(f"  Ground Truth: {mismatch['Ground Truth']}")
            print(f"  Prediction: {mismatch['Prediction']}\n")

def find_missing_sentences(ground_truth_file, predictions_file):
    """
    Find sentences present in the ground truth but missing in the predictions.

    Args:
        ground_truth_file (str): Path to the ground truth JSON file.
        predictions_file (str): Path to the predictions JSON file.

    Returns:
        List[str]: A list of sentences missing in the predictions.
    """
    # Load the JSON files
    with open(ground_truth_file, 'r') as gt_file:
        ground_truth_data = json.load(gt_file)
    
    with open(predictions_file, 'r') as pred_file:
        predictions_data = json.load(pred_file)

    # Extract sentences from both files
    ground_truth_sentences = {item["Sentence"] for item in ground_truth_data}
    prediction_sentences = {item["Sentence"] for item in predictions_data}

    # Find missing sentences
    missing_sentences = ground_truth_sentences - prediction_sentences

    return list(missing_sentences)

if __name__=="__main__":

    # Define the paths to your JSON files
    ground_truth_file = "laptops-trial.json"  # JSON file generated from the XML data
    predictions_file = "gemini_result.json"  # JSON file generated from Gemini


    # Example Usage
    missing = find_missing_sentences("laptops-trial.json", "gemini_result.json")

    # Print missing sentences
    if missing:
        print("Missing Sentences:")
        for sentence in missing:
            print(f"- {sentence}")
    else:

        print("No sentences are missing.")


    compare_json_files(ground_truth_file, predictions_file)