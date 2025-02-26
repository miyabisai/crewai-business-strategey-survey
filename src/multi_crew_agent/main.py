#!/usr/bin/env python
import os
import shutil
import sys
import warnings
from crew import MultiCrewAgent
from datetime import datetime


warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def delete_old_files():
  
    result_dir = "./result"
    knowledge_dir = "./knowledge"

    for dir in [result_dir, knowledge_dir]:
        if os.path.exists(dir):
            for filename in os.listdir(dir):
                file_path = os.path.join(dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print('Failed to delete %s. Reason: %s' % (file_path, e))

def run():
    """
    Run the crew.
    """
    inputs = {
        'topic': 'TSMC',
    }
    
    try:
        MultiCrewAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

run()

def main():
    delete_old_files()
    run()

if __name__ == "__main__":
    main()