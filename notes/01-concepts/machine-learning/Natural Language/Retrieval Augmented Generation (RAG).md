It's a technique for semantic searching in a large scopes of data to enhance the context of the [[Language Models]]. It has three parts, a pre-processing the retrieval and generation.
# Pre-processing
First a [[Model Learning|Machine Learning Model]] is used for doing Text to [[Vector]], this models are [[Embeddings]] models that turn the files of the context of the application into Vectors and then that is stored in a [[Vector DB|Vector Databases]]. For big files the system might opt for creating chunks, this chunks are then separately passed through the embedding. 

Modernly this processed can be made using files that not only text-based, but also audio-based or video-based, this requires different types of [[Embeddings]] models, there is also a Multi Modal Embeddings that instead of using different types of Embeddings they use the same model, and the key advantage of doing this is that they are mapped to the same [[Vector Spaces]]. 

# Chunks
A problem with the Embedding models is that it has a fixed Input, and inputs can be larger then it, therefore the input is separated into chunks, there are a few types of strategies to do chunking, some of them are:
- **Fixed Size**: You maintain all chunking at a fixed size with cropping.
- **Recursive**: You separate the chunks using separator characters, like new line, spaces, tabs and etc.
- **Semantic**: Use embeddings to evaluate two sequential separated chunked using a similarity score and re chunk if the separated chunks are too low. 
- **Agentic**: Uses [[Language Models]] to analyse and divide the input into chunks. 

# Retrieval
When a new query is made by the user, it is passed through the embedding model and it is searched using some kind of similarity score (for instance normalized [[Vector#Dot product|Dot Product]]) for retrieving a top $K$ most similar results. 

# Augmented Generation
The system takes the top $K$ results of retrieval and places its chunks inputs into the original user prompt (normally using the [[Prompt Engineering#Roles|role]] of assistant) and gives a response with the context.

# Comments
There is a few problems with this approach, therefore there are some improvements that can be done on this process. One of which is to use a limiting similarity, such as if the similarity is too low (usually meaning is something too off-topic) you might want to ignore the retrieval. Oppositely it might have too many important results, which you can make an exception to use more then the original $K$. 

There is also a prompt engineering challenge on doing that since it can increase heavily the [[Tokenizers|Tokens]] used.