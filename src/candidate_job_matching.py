from transformers import DistilBertTokenizer, DistilBertModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load the DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertModel.from_pretrained('distilbert-base-uncased')

# Function to preprocess and obtain embeddings for text
def get_text_embeddings(text):
    # Tokenize the text
    input_ids = tokenizer(text, return_tensors="pt", padding=True, truncation=True)['input_ids']

    # Get model embeddings
    with torch.no_grad():
        embeddings = model(input_ids)[0]

    # Average pooling to obtain a single vector for the text
    embeddings = torch.mean(embeddings, dim=1).numpy()

    return embeddings

# Function to perform candidate-job matching
def match_candidates_to_jobs(candidate_cv_embeddings, job_description_embeddings):
    similarity_scores = cosine_similarity(job_description_embeddings, candidate_cv_embeddings)
    return similarity_scores
