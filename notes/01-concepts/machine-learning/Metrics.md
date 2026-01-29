
# [[Model Learning|ML]] models metric
## Supervised Learning

## Reinforcement Learning

## Unsupervised Learning

## LLM
### Recall-Oriented Understudy for Gisting Evaluation (ROUGE)
Normally used for evaluating automatic summarization and machine translation systems, it uses [[N-grams]] matched between reference and generated text. 
### Bilingual Evaluation Understudy (BLUE)
Normally used for evaluating the quality of generated text, specially for translations, it rewards precision and penalizes brevity. It looks at a combination of n-grams. 

### BERTScore
It is a metric to evaluate semantic similarity between generated texts. It uses the [[Language Models#List of Models|BERT Model]] to compare the contextualized [[Embeddings]] of both texts computing a [[Vector#Dot product|Cosine Similarity]] between them. 

### Perplexity
It reads the [[Neural Networks (NN)#Multi Layer Perceptron (MLP)|Output Layer]] and compute the confidence score. A lower perplexity value is better.  


# Business metrics for ML
1. User satisfaction
2. Average Revenue per user (ARPU)
3. Cross-Domain Performance (model's ability to perform tasks across different domains)
4. Conversion rate (recommendation to purchase)
5. Efficiency (price payed for running it)
