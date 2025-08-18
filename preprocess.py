## Joson stores ban phrases; shuffle randomizes data to stop order bias 
import json
from collections import Counter
from sklearn.svm import SVC
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.exceptions import NotFittedError
from  sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#from your_module import bannedSpeechPreprocessor, process_banned_speech
## Makes it so no all speech is at the same level of severity 
SEVERITY_LEVELS = {
    0: {"name": "Safe", "threshold" : 0.0, "action" : "allow", "examples": []},
    1: {"name": "Meduim", "threshold" : 0.3, "action" : "flag", "examples": ["I hate them all"]},
    2: {"name": "High", "threshold" : 0.6, "action" : "review", "examples": ["I want to slit my wrists"]},
    3: {"name": "Extreme", "threshold" : 0.9, "action" : "block", "examples": ["I hope you get raped and die"]} 
}
## OR if file mock code for upload file 
def load_and_process_hateexplain_data(filepath = "hate_speech.json"): 
    
    messages = []
    categories = []

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Please ensure the 'hate_speech.json' file is in the correct directory.")
        return [], []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. Check file integrity.")
        return [], []

    for post_id, post_data in data.items():
        # Join tokens to form the full message
        message = " ".join(post_data['post_tokens'])
        
        # Get labels from all annotators for this post
        annotator_labels = [ann['label'] for ann in post_data['annotators']]
        
        # Map HateXplain labels to your 'BAD'/'Good' categories
        mapped_labels = []
        for label in annotator_labels:
            if label.lower() in ["hatespeech", "offensive"]:
                mapped_labels.append("BAD")
            elif label.lower() == "normal":
                mapped_labels.append("Good")
            # Ignore any other unexpected labels
        
        if not mapped_labels: # Skip if no valid labels were found
            continue

        # Determine the final label by majority vote
        label_counts = Counter(mapped_labels)
        
        # Prioritize 'BAD' if it's the majority or a tie
        if label_counts.get("BAD", 0) >= label_counts.get("Good", 0):
            final_label = "BAD"
        else:
            final_label = "Good"
            
        messages.append(message)
        categories.append(final_label)

    return messages, categories
# Print the loaded banned speech to verify
#print(banned_speech)
## Converts the banned speech into categories for training recognition 
## RETURNS: data list list of text samples and the same for categories but for each text sample
def process_banned_speech(use_file=True, filename="hate_speech.json"):
    if use_file and filename:
        messages, categories = load_and_process_hateexplain_data(filename)
        return messages, categories
    else:
        print("Using written data (hardcoded defaults).")
        banned_data_dict = {
            "BAD": [...],
            "Good": [...]
        }
        max_samples = min(len(banned_data_dict["BAD"]), len(banned_data_dict["Good"]))
        balanced_messages = []
        balanced_categories = []
        for i in range(max_samples):
            balanced_messages.append(banned_data_dict["BAD"][i].lower().strip())
            balanced_categories.append("BAD")
            balanced_messages.append(banned_data_dict["Good"][i].lower().strip())
            balanced_categories.append("Good")
        balanced_messages, balanced_categories = shuffle(balanced_messages, balanced_categories, random_state=42)
        return balanced_messages, balanced_categories

    else: 
            print("Using written data (hardcoded defaults).")
            banned_data_dict = {
                "BAD" :[
                    "I feel like killing myself ", "I want to hurt myself",
                    "I want to end it all", "I want to die", "I want to hurt others",
                    "Violence is the answer", "Do you think I should kill",
                        "I'm going to kill myself tonight", "I want to slit my wrists",
                        "Ending my life seems like the only option",
                        "I can't stop thinking about suicide",
                        "I'll murder you in your sleep",
                        "Someone should shoot up that place",
                        "Let's burn them alive",
                        "I hope you get raped and die",
                        "All [racial slur] should be exterminated",
                        "Death to all [religious group]",
                        "[Group] are subhuman and deserve torture"
                    ], 
                    "Good": [
                        "I want help", "I need support", "I feel sad",
                        "I'm feeling much better today", "Talking to someone helped me",
                        "I'm working through my problems", "Life is worth living",
                        "I want to talk about my feelings", "Let's solve this peacefully",
                        "I disagree but respect your view", "Violence is never the answer",
                        "We can find common ground", "I appreciate your concern",
                        "How can I help you?", "You're not alone in this",
                        "Things will get better", "I care about your wellbeing"
                    ]
                }
            
    # Balance the hardcoded data
    max_samples = min(len(banned_data_dict["BAD"]), len(banned_data_dict["Good"]))
        
    balanced_messages = []
    balanced_categories = []

    for i in range(max_samples):
        balanced_messages.append(banned_data_dict["BAD"][i].lower().strip())
        balanced_categories.append("BAD") 
        balanced_messages.append(banned_data_dict["Good"][i].lower().strip())
        balanced_categories.append("Good") 
            
    balanced_messages, balanced_categories = shuffle(balanced_messages, balanced_categories, random_state=42)
    return balanced_messages, balanced_categories
## Ignore Unnecessary words 
class BannedSpeechPreprocessor: # Class names typically start with a capital letter
    ## JSON stores ban phrases; shuffle randomizes data to stop order bias

## Defines severity levels and suggested actions
    SEVERITY_LEVELS = {
        0: {"name": "Safe", "threshold": 0.0, "action": "allow", "examples": []},
        1: {"name": "Medium", "threshold": 0.3, "action": "flag", "examples": ["I hate them all"]},
        2: {"name": "High", "threshold": 0.6, "action": "review", "examples": ["I want to slit my wrists"]},
        3: {"name": "Extreme", "threshold": 0.9, "action": "block", "examples": ["I hope you get raped and die"]}
    }

def load_and_process_hateexplain_data(filepath="hate_speech.json"):
    messages, categories = [], []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: {filepath} not found. Please ensure it's in the correct directory.")
        return [], []
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}. Check file integrity.")
        return [], []

    for post_id, post_data in data.i:

        def __init__(self):
            self.pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(
                    stop_words='english',  # stops words like "the, etc."
                    ngram_range=(1, 2)  # checks single words and pairs of words
                )),
                # Default classifier; can be replaced by auto_train_model
                ('classifier', RandomForestClassifier(
                    class_weight='balanced',
                    random_state=42
                ))
            ])
    #Adding key words that add
    def key_severity_boost(self, text):
        extreme_words = { 
            "kill", "killing", "murder", "burn", "burned", "burning",
            "shoot", "shooting", "shot", "stab", "stabbed", "hang",
            "bomb", "explode", "explosion", "rape", "raped", "raping",
            "slaughter", "massacre", "terrorist", "terrorism",
            "die", "dying", "suicide", "self-harm", "cut", "cutting",
            "abuse", "abusive", "molest", "molested", "molesting",
            "assault", "threat", "threaten", "lynch", "genocide",
            "hate", "hatred", "torture", "suffocate", "strangle",
            "destroy", "eliminate", "eradicate", "execute", "crucify"}
        
        words = text.lower().split()
        count = sum(1 for words in words if words in extreme_words)
        boost = min(0.05*count, 0.2) # Ensures boost does not exceed 40% 
        return boost
    
        
    def train(self, messages, categories):
    #Trains Classification Pipeline
    # messages: list of strings (text messages)
    # categories: list of corresponding labels (e.g., 0 for benign, 1 for banned)
        print("Training begins...")
        self.pipeline.fit(messages, categories)   
        print("Training Complete")
        
    def calc_confidence(self, proba):
        "Calculates a confidence score of the severity of the text "
        thresholds = [level["threshold"] for level in SEVERITY_LEVELS.values()]
        
        if not thresholds:
            return 0.0 # Default 
        # Confidence logic: closer to a threshold boundary means lower confidence in that specific level assignment.
        # Further from a threshold means higher confidence.
        # Max distance from a threshold is 0.5 (e.g., proba 0.25 and threshold 0 or 0.5)
        # So 1 - abs(probability - nearest_threshold) gives 0.5 to 1.0 range.
        nearest_threshold = min(thresholds, key=lambda x: abs(x - proba))
        return round(1 - abs(proba - nearest_threshold), 4) 
    
    def  predict_severity(self, text):
        try:
            # Predict probability of the text being "bad" (class 1)
            proba = self.pipeline.predict_proba([text])[0][1]
        except NotFittedError:
            return {
                "text": text,
                "badness_proba": 0.0,
                "severity_level": "Error",
                "action": "Model not trained. Please train the model first.",
                "confidence": 0.0
            }
        except Exception as e:
            return {
                "text": text,
                "badness_proba": 0.0,
                "severity_level": "Error",
                "action": f"Prediction failed: {e}",
                "confidence": 0.0
            }

        # This line was incorrectly placed inside the exception block before.
        boost = self.key_severity_boost(text)  # Optional boosting function
        proba = min(proba + boost, 1.0)  # Cap at 100%

        # Determine the severity level based on probability thresholds
        sorted_levels = sorted(SEVERITY_LEVELS.keys(), key=lambda k: SEVERITY_LEVELS[k]["threshold"], reverse=True)
        severity_info = SEVERITY_LEVELS[0]  # Default to "Safe"

        for level_key in sorted_levels:
            info = SEVERITY_LEVELS[level_key]
            if proba >= info["threshold"]:
                severity_info = info
                break

        return {
            "text": text,
            "badness_proba": round(proba * 100, 2),
            "severity_level": severity_info["name"],
            "action": severity_info["action"],
            "confidence": self.calc_confidence(proba)
        }
    def auto_train_model(self, messages, categories):
        """
        Automatically trains the model based on provided messages and categories.

        Args:
            messages (_type_): _description_
            categories (_type_): _description_
        """
        print("Auto-training model with classifiers...")
        X_train, X_val, y_train, y_val = train_test_split(messages, categories, test_size=0.2, random_state=42)

        classifiers = { 
            "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
            "SVC": SVC(probability=True, kernel='linear', class_weight='balanced'),
            "Logistic Regression": LogisticRegression(class_weight='balanced', max_iter=1000)
        }
        best_model = None 
        best_score = 0.0
        best_name = "" 
        
        for name, model in classifiers.items():
            pipeline = Pipeline([
                ('vectorizer', TfidfVectorizer(stop_words='english', ngram_range=(1, 2))),
                ('classifier', model)
            ])
            pipeline.fit(X_train, y_train) 
            preds = pipeline.predict(X_val)
            score = accuracy_score(y_val, preds)
            
            print(f"{name.upper()} accuracy: {score:.4f}")
            if score > best_score:
                best_score = score
                best_model = pipeline
                best_name = name
        if best_model is not None:
            self.pipeline = best_model
            print(f"Selected model: {best_name.upper()} with accuracy {best_score:.4f}")
    
preprocessor =  BannedSpeechPreprocessor()
messages_to_train, categories_to_train = process_banned_speech(use_file=True, filename="banned_speech.json")
preprocessor.auto_train_model(messages_to_train, categories_to_train)
test_messages = [
        "Let's burn them alive",
        "I hope you get raped and die",
        "Can I tell you something important.",
        "Life is worth living",
        "I want to talk about my feelings",
        "Let's solve this peacefully",
        "I disagree but respect your view",
        "Violence is never the answer",
        "We can find common ground",
        "I appreciate your concern",
        "How can I help you?",
        "I want to burn it all down."
    ]
preprocessor.auto_train_model(messages_to_train, categories_to_train)
for text_message in test_messages:
        result = preprocessor.predict_severity(text_message)
        print(f"\nAnalyzing: '{result['text']}'")
        print(f"  Probability of badness: {result['badness_proba']}%")
        print(f"  Severity Level: {result['severity_level']}")
        print(f"  Recommended Action: {result['action']}")
        print(f"  Confidence: {result['confidence']:.2f}")

        if result["action"] == "block":
            print(f"  --> MESSAGE BLOCKED: '{result['text']}'")
        elif result["action"] == "review":
            print(f"  --> MESSAGE FLAGGED FOR REVIEW: '{result['text']}'")
        elif result["action"] == "flag":
            print(f"  --> MESSAGE FLAGGED: '{result['text']}'")
        else: # "allow"
            print(f"  --> MESSAGE ALLOWED: '{result['text']}'")
    
if __name__ == "__main__": 
    print("Testing data from the hate_speech.json file...")
    hatexplain_messages, hatexplain_categories = load_and_process_hateexplain_data("hate_speech.json")

    print(f"Loaded {len(hatexplain_messages)} messages from HateXplain.")
    print(f"Sample HateXplain message: {hatexplain_messages[0]} -> Label: {hatexplain_categories[0]}")
    