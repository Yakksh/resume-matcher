### Creating the Virtual Environment

```bash
pip install virtualenv
virtualenv venv
venv/Scripts/activate
```

### Installing the Requirements

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Using the Resume-Matcher

#### Step 1: Extract the required candidates details from their CVs

The directory `data/cv_dataset` contains all the pdfs of candidates CVs.

This will extract all the required detials for you and will store in `data/preprocessed_data/cv_details`.

```bash
python -u src/pdf_extraction.py
```

#### Step 2: Run main.py to get your Top 5 Candidates for every job Description you have.

```bash
python -u main.py
```
