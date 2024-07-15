import subprocess
import os


def run_script(script_name):
    """ Function to run a python script using subprocess """
    try:
        subprocess.check_call(['python', script_name])
        print(f"Successfully ran {script_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to run {script_name}")


def ensure_directory(directory):
    """ Ensure the directory exists, and if not, create it """
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")


ensure_directory('processed_data')

scripts = [
    'preprocess_books_data.py',
    'author_sentiment.py',
    'author_sentiment_distribution.py',
    'relevant_reviews.py',
    'relevant_users.py'
]

for script in scripts:
    run_script(script)
