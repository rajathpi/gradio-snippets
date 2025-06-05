import PyPDF2
import pathlib
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

# Setup NLTK
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# --- Step 1: Extract Text from PDFs ---
# folder_path = input("Enter the path to the folder containing PDFs: ").strip()
folder_path = r"C:\Users\A495346\Downloads\project_info"


# for file_name in folder_path:
    # print(file_name)
extracted_chunks = []

for file in pathlib.Path(folder_path).rglob('*.pdf'):
    try:
        reader = PyPDF2.PdfReader(str(file))
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                # Break into smaller chunks for accuracy
                paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]
                for para in paragraphs:
                    extracted_chunks.append((file.name, i + 1, para))
    except Exception as e:
        print(f"Error reading {file.name}: {e}")

# --- Step 2: Keyword Matching ---
def extract_keywords(text):
    words = word_tokenize(text.lower())
    return [word for word in words if word.isalnum() and word not in stop_words]

# --- Step 3: Ranking Chunks Based on Keyword Overlap ---
def rank_answers(query, chunks, top_k=5):
    query_keywords = extract_keywords(query)
    scores = []

    for filename, page_num, chunk in chunks:
        chunk_keywords = extract_keywords(chunk)
        common = set(query_keywords) & set(chunk_keywords)
        score = len(common)
        if score > 0:
            scores.append((score, filename, page_num, chunk))

    # Sort by score (descending) and return top results
    top_matches = sorted(scores, reverse=True)[:top_k]
    return top_matches

# --- Step 4: User Input & Result ---
user_query = input("\nEnter your question: ").strip()
top_answers = rank_answers(user_query, extracted_chunks)

if not top_answers:
    print("No relevant information found.")
else:
    print("\nTop Relevant Passages:\n")
    for score, filename, page, chunk in top_answers:
        print(f"📄 {filename} (Page {page}) — Score: {score}")
        print(f"{chunk[:500].strip()}...\n{'-'*60}\n")
