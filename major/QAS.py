# Install the necessary libraries
'''!pip install transformers
!pip install googlesearch-python
!pip install google
!pip install beautifulsoup4
!pip install requests'''
# Import the necessary libraries
from transformers import pipeline
from googlesearch import search
from bs4 import BeautifulSoup
import requests

# Get the passage from the user
passage = input("Enter the passage: ")

# Create a list of questions from the user
num_questions = int(input("How many questions do you have? "))
questions = []
for i in range(num_questions):
    question = input(f"Enter question {i+1}: ")
    questions.append(question)

# Create the question answering pipeline using the 'distilbert-base-uncased-distilled-squad' model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Loop through each question and find the answer
for i, question in enumerate(questions):
    print(f"\nQ{i+1}: {question}")
    
    # Search for the answer in the given passage
    answer = qa_pipeline(question=question, context=passage)
    
    # If the answer is found in the passage, print it
    if answer["score"] > 0.5:
        print(f"A: {answer['answer']}")
    else:
        # If the answer is not found in the passage, search the internet for the answer
        query = f"{question} {passage}"
        try:
            urls = search(query, num_results=1)
            if urls:
                url = next(urls)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
                }
                res = requests.get(url, headers=headers)
                soup = BeautifulSoup(res.text, "html.parser")
                ans = soup.select_one(".BNeawe i")
                if ans:
                    print(f"A: {ans.get_text()}")
                else:
                    print("A: Answer not available.")
                print(f"Link: {url}")
            else:
                print("A: Answer not available.")
        except:
            print("A: Error occurred while searching for the answer.")
