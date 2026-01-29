# Supervised Learning

# Reinforcement Learning

# Unsupervised Learning

# LLM
### Recall-Oriented Understudy for Gisting Evaluation (ROUGE)
Normally used for evaluating automatic summarization and machine translation systems, it uses [[N-grams]] matched between reference and generated text. 


### Bilingual Evaluation Understudy (BLUE)
Normally used for evaluating the quality of generated text, specially for translations, it rewards precision and penalizes brevity. It looks at a combination of n-grams. 

## BERTScore
It is a metric to evaluate semantic similarity between generated texts. It uses the [[Language Models#List of Models|BERT Model]] to compare the contextualized [[Embeddings]] of both texts computing a [[Vector#Dot product|Cosine Similarity]] between them. 


