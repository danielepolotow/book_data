import subprocess


def run_script(script_name):
    """ Function to run a python script using subprocess """
    try:
        subprocess.check_call(['python', script_name])
        print(f"Successfully ran {script_name}")
    except subprocess.CalledProcessError:
        print(f"Failed to run {script_name}")


scripts = [
    'preprocess_books_data.py',
    'author_sentiment.py',
    'author_sentiment_distribution.py',
    'relevant_reviews.py',
    'relevant_users.py'
]

for script in scripts:
    run_script(script)
