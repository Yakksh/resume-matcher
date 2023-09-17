from datasets import load_dataset

preprocessed_data_directory = 'data/preprocessed_data/'

# Function to load job descriptions from the Hugging Face dataset
def load_job_descriptions():
    try:
        # Load the job descriptions dataset
        dataset = load_dataset("jacob-hugging-face/job-descriptions", split="train")

        # Extract a subset of job descriptions
        initial = 20
        num_descriptions = min(10, len(dataset))
        job_descriptions = dataset[initial:initial+num_descriptions]

        return job_descriptions

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
