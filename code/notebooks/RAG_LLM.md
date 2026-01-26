---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.19.1
  kernelspec:
    display_name: .venv
    language: python
    name: python3
---

<!-- #region -->
# RAG from Scracth

This notebook goal is to implement a simple [[Retrieval Augmented Generation (RAG)]] using [[Vector#Dot Product|Cosine Simillarity]].

The pipelines goes like this: first you create [[Retrieval Augmented Generation (RAG)#Chunks|Chunks]] for the documents in which you want to search and create [[Embeddings]]. When the user asks a questions, it creates embeddings of the questions and using a similarity score retrieve the top $K$ results, and feed them to the [[Language Models|LM]].

# Requirements

You must have ollama installed. Use this to get the same model as I am.

```bash
ollama run gemma3:4b
```

You also must have authorization from this link: 

# Imports
<!-- #endregion -->

```python
import ollama
from sentence_transformers import SentenceTransformer
import numpy as np
from glob import glob
from IPython.display import Markdown, display

EMBEDDING_MODEL = SentenceTransformer("google/embeddinggemma-300m")
LM_VERSION = "gemma3:4b"
```

For this notebook I will use this obsidian vault as the dataset. I will try to use each separated file as a chunk since there isn't no really big files.

For context of the reader, EE is Exploration vs Exploitation in my notes.

```python
question = "give me two types of EE heuristics"
```

```python
VECTOR_DB = []

def add_chunk_to_database(chunk):
  embedding = EMBEDDING_MODEL.encode(chunk)
  VECTOR_DB.append((chunk, embedding))
```

```python
filepath = glob("../../notes/**/**.md", recursive=True)
filepath
```

```python
# load each file and add it to the database
for file in filepath:
  with open(file, "r") as f:
    content = f.read()
    # append the file name to the chunk
    if content == "": continue
    content = f"File: {file}\n{content}"
    
    add_chunk_to_database(content)

# turn the database into a numpy array
VECTOR_DB_NP = np.array([v[1] for v in VECTOR_DB])
```

```python
# Implement a simple cosine similarity function using numpy
def cosine_similarity(a, b):
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Implement a simple RAG function
def retrival(question, k=5):
  query_embedding = EMBEDDING_MODEL.encode(question)
  similarities = cosine_similarity(VECTOR_DB_NP, query_embedding)
  top_k_indices = np.argsort(similarities)[-k:][::-1]
  top_k_chunks = [VECTOR_DB[i][0] for i in top_k_indices]
  return top_k_chunks

# Test the RAG function
top_k_chunks = retrival(question)
print(top_k_chunks)

```

```python

def RAG(question, k=5):
  top_k_chunks = retrival(question, k)
  print(top_k_chunks)
  k_str = '\n'.join([f' - {chunk}' for chunk in top_k_chunks])
  instruction_prompt = f'''You are a helpful chatbot.
Use only the following pieces of context to answer the question. Don't make up any new information:
{k_str}
'''
  response = ollama.generate(model=LM_VERSION, prompt=instruction_prompt)
  return response

response = RAG(question)
display(Markdown(response.response))
```

```python
# without rag
response = ollama.generate(model=LM_VERSION, prompt=question)
display(Markdown(response.response))
```
