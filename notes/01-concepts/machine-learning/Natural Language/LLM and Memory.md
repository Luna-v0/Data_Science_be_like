There are two main types of memory for LLM in **LangChain**, a conversational memory and [[Vector DB]].

## Conversational

### Window Memory
Maintains only the N last messages. 

### Full history
Keeps all the messages. 

### Summarization Memory
When going over the limit it makes a summarization of the messages.

### Token Buffer
