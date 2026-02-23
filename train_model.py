import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import os

# Get the directory where this script is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load dataset from CSV file
csv_path = os.path.join(SCRIPT_DIR, "Fake Postings.csv")
print(f"Loading data from: {csv_path}")
df = pd.read_csv(csv_path)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Label distribution:\n{df['fraudulent'].value_counts()}")

# Combine all text fields into a single text column for training
text_columns = ['title', 'description', 'requirements', 'company_profile', 'location', 
                'salary_range', 'employment_type', 'industry', 'benefits']

def combine_text(row):
    """Combine all text fields into a single string for NLP processing."""
    parts = []
    for col in text_columns:
        if pd.notna(row[col]):
            parts.append(str(row[col]))
    return " ".join(parts)

df["text"] = df.apply(combine_text, axis=1)

# Prepare features and labels
X = df["text"]
y = df["fraudulent"]

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTraining set size: {len(X_train)}")
print(f"Test set size: {len(X_test)}")

# Preprocess and vectorize text data
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000, ngram_range=(1, 2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Train logistic regression model
print("\nTraining model...")
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_vec, y_train)

# Evaluate the model
y_pred = model.predict(X_test_vec)
print("\n=== Model Evaluation ===")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["Legitimate", "Scam"]))

# Save the model and vectorizer
model_path = os.path.join(SCRIPT_DIR, "model.pkl")
vectorizer_path = os.path.join(SCRIPT_DIR, "vectorizer.pkl")

joblib.dump(model, model_path)
joblib.dump(vectorizer, vectorizer_path)

print(f"\nModel saved to: {model_path}")
print(f"Vectorizer saved to: {vectorizer_path}")
print("Model trained and saved successfully!")