Are a set of techniques for creating better [[Language Models#Prompts|prompts]]. The main topic on it is context, there are many problems involved context, like missing information, bad training data, hallucination, ambiguity, etc.

## Guidelines
Those are 5 main guidelines for creating better prompts.

1. **Clarity:** It must be exact about what you want.
2. **Context**: More information about the subject helps the [[Language Models|LM]] to respond better, but they must be relevant, sufficient and not large as it can be to avoid [[Language Models#Prompts|Context Window]] problems. 
3. **Objective:** Be concise and avoid ambiguity.
4. **Detail:** Detail makes guides better the response.
5. **Purpose:** What is the objective. 

Other useful stuff is to deal with [[Model Learning#Hyperparameters|Hyperparameters]] for instance lower temperature tend to avoid hallucination.