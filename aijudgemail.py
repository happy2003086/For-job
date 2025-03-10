# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, accuracy_score

# Example dataset
data = {
    'sentence': [
        # Spam sentences
        "Congratulations! You have just won a $1000 gift card.",
        "Limited time offer! Get free tickets to a concert.",
        "You have been selected for a special prize! Click here.",
        "Earn money fast without leaving your home, sign up now.",
        "Free trial for a premium subscription, act fast!",
        "You qualify for a special lottery prize. Claim it today!",
        "Get a free iPhone by signing up for this promotion.",
        "Invest now in Bitcoin and earn quick profits.",
        "Exclusive offer: Buy one get one free on all products.",
        "Get a payday loan in 24 hours, no credit check required.",
        # Non-spam sentences
        "Hey, how was your weekend? Let me know when you're free.",
        "Looking forward to the meeting tomorrow at 10 AM.",
        "Could you send me the revised document for approval?",
        "Let's catch up for coffee next week, let me know your schedule.",
        "I’ll be in the office around noon today.",
        "Can you please check the attached file for any errors?",
        "We are having a team lunch on Friday, would you like to join?",
        "Please confirm if you're available for a conference call.",
        "I received your email about the upcoming event, sounds great!",
        "Don't forget our project deadline next Wednesday at 5 PM."
    ] * 100,  # Repeat to simulate 1000 sentences

    'label': [
        # Spam labels: 1 indicates spam
        1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
        # Non-spam labels: 0 indicates non-spam
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ] * 100  # Repeat labels to match the number of sentences
}

# Convert to pandas DataFrame
df = pd.DataFrame(data)

# Split dataset into train and test sets (80% train, 20% test)
X = df['sentence']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Text preprocessing and vectorization using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train the Naive Bayes model
nb_model = MultinomialNB()
nb_model.fit(X_train_tfidf, y_train)

# Make predictions
y_pred_nb = nb_model.predict(X_test_tfidf)

# Evaluate the Naive Bayes model
print("Naive Bayes Model Evaluation:")
print(classification_report(y_test, y_pred_nb))
print(f"Accuracy: {accuracy_score(y_test, y_pred_nb)}")

# User input to classify sentence
while True:
    user_input = input("Enter a sentence to classify as spam or not (or type 'exit' to quit): ")
    
    if user_input.lower() == 'exit':
        break

    # Preprocess the user input using the same vectorizer
    user_input_tfidf = vectorizer.transform([user_input])

    # Predict using the trained model
    prediction = nb_model.predict(user_input_tfidf)
    
    # Display the result
    if prediction == 1:
        print("This is a SPAM (junk) message.")
    else:
        print("This is NOT a SPAM (non-junk) message.")
