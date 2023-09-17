import os
import pandas as pd
import numpy as np
import json
from src.job_description_fetch import load_job_descriptions
from src.candidate_job_matching import get_text_embeddings, match_candidates_to_jobs


def preprocess_job_descriptions(jobs):
    model_responses = []
    for desc in jobs:
        de = json.loads(desc)
        features = [de["Core Responsibilities"], de["Required Skills"], de["Educational Requirements"], de["Experience Level"]]
        res = ', '.join(features)
        model_responses.append(str(res))
    
    return model_responses

preprocessed_data_directory = 'data/preprocessed_data/'

if __name__ == "__main__":
    job_descriptions = load_job_descriptions()
    if job_descriptions:
        job_descriptions = pd.DataFrame(job_descriptions)
        output_csv_path = os.path.join(preprocessed_data_directory,'job_descriptions', 'all_job_descriptions.csv')
        job_descriptions.to_csv(output_csv_path, index=False)
    else:
        print("Job description loading failed.")


    # Load job descriptions and candidate CVs as text
    job_descriptions = pd.read_csv('data/preprocessed_data/job_descriptions/all_job_descriptions.csv')
    job_descs = job_descriptions['model_response'].tolist()
    job_descs = preprocess_job_descriptions(job_descs)


    candidate_cvs = pd.read_csv('data/preprocessed_data/cv_details/all_cv_details.csv')
    candidate_cvs = candidate_cvs[candidate_cvs.Education!='not available']
    candi_cvs = candidate_cvs['Skills'].tolist()
    candi_cvs = [str(cv) for cv in candi_cvs]

    # Get embeddings for job descriptions and candidate CVs
    job_description_embeddings = get_text_embeddings(job_descs)
    candidate_cv_embeddings = get_text_embeddings(candi_cvs)

    # Match candidates to jobs
    similarity_scores = match_candidates_to_jobs(candidate_cv_embeddings, job_description_embeddings)

    position_titles = job_descriptions['position_title'].tolist()
    candi_pdfs = candidate_cvs['Name'].tolist()

    # Rank candidates for each job
    for job_idx, scores in enumerate(similarity_scores):
        ranked_candidates = np.argsort(scores)[::-1]  # Sort in descending order
        top_candidates = ranked_candidates[:5]  # Get the top 5 candidates
        print(f"{position_titles[job_idx]}:")
        for rank, candidate_idx in enumerate(top_candidates):
            print(f"Rank {rank + 1}: {candi_pdfs[candidate_idx]}, Similarity Score: {scores[candidate_idx]}")