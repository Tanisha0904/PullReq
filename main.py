import json
import spacy
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict

# Load the spaCy English model
nlp = spacy.load("en_core_web_md")

# Load the JSON document
with open("D:\BMC\Pull_Req\data_2.json", "r") as file:
    data = json.load(file)

# Create a mapping of document numbers to titles
doc_numbers_to_titles = {fact["number"]: fact["title"] for fact in data}

# Preprocess the data and tokenize the text
documents = {}
print("Tokenizing the documents...")

for fact in data:
    # doc = nlp(fact["title"] + " " + fact["body"] + fact['changes_made'])
    doc = nlp(fact["title"] + " " + " ".join(fact["labels"]))
    # print(doc, end="---")
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    documents[fact["number"]] = " ".join(tokens)

# Tokenize and vectorize the query
def preprocess_query(query):
    print("Tokenizing the query...")
    doc = nlp(query)
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct]
    return " ".join(tokens)

# Compute cosine similarity between the query and each document
def compute_similarity(query, documents):
    print("Computing the similarity...")
    query_vector = nlp(preprocess_query(query)).vector
    similarity_scores = defaultdict(float)
    for doc_number, doc_text in documents.items():
        doc_vector = nlp(doc_text).vector
        # Compute cosine similarity between query vector and document vector
        sim = cosine_similarity([query_vector], [doc_vector])[0][0]
        # if sim >0.5:
        similarity_scores[doc_number] = sim
    return similarity_scores

# Search function
def search(query, documents):
    similarity_scores = compute_similarity(query, documents)
    sorted_results = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_results

# Example usage
query = input("Enter your query: ")
results = search(query, documents)

# Output the results
print("\nRelevant facts (sorted by relevance):")
for doc_number, similarity_score in results:
    if doc_number in doc_numbers_to_titles:  # Check if doc_number is a valid key in the mapping
        print(f"Number: {doc_number} ")
        print(f"Title: {doc_numbers_to_titles[doc_number]} \nSimilarity Score: {similarity_score}")
        print()
    else:
        print(f"Document with number {doc_number} does not exist in the data.")
