import os
import glob
import pandas as pd
from pyresparser import ResumeParser

# Base directory where CVs are stored
cv_base_directory = 'data/cv_dataset/data/'
preprocessed_data_directory = 'data/preprocessed_data/'
all_cv_details = []

# Function to process CVs using pyresparser
def process_cvs_with_pyresparser():
    job_role_directories = glob.glob(os.path.join(cv_base_directory, '*'))

    for job_role_directory in job_role_directories:
        job_role = os.path.basename(job_role_directory)
        cv_files = glob.glob(os.path.join(job_role_directory, '*.pdf'))

        for cv_file in cv_files:
            cv_filename = os.path.basename(cv_file)
            
            # Use pyresparser to extract resume information
            data = ResumeParser(cv_file).get_extracted_data()

            # Extract relevant details
            skills = data.get("skills", [])
            skills = ', '.join(skills)

            if data.get('degree', []):
                education = data.get("degree", [])
                education = ', '.join(education)
            else:
                education = 'not available'
            
            # Create a dictionary with extracted details
            cv_details = {
                'Name': cv_filename,
                'Job Role': job_role,
                'Skills': skills,
                'Education': education
            }
            # Save the extracted details to a CSV or other structured format
            # You can also store these details in a database or other storage
            all_cv_details.append(cv_details)
    return all_cv_details

if __name__ == "__main__":
    # Call the function to process CVs and extract details
    all_cv_details_df = pd.DataFrame(process_cvs_with_pyresparser())

    # Save all CV details to a single CSV file
    output_csv_path = os.path.join(preprocessed_data_directory,'cv_details', 'all_cv_details.csv')
    all_cv_details_df.to_csv(output_csv_path, index=False)