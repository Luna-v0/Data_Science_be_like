It is a type of database optimized for querying [[Vector]] structures.

## Implementations
They are normally implemented as extensions of traditional [[Dataset#DS vs DB|Database]], like [[Relational DB#Implementations|Postgres]], [[Document DB#Implementations|Mongo]] or [[Key Value DB#Implementations|Redis]]. Some of them are:

- **[[AWS]] OpenSearch**: Normally used for search & analytics dabase real time similarities queries, scalable index management, and fast compute of [[K nearest neighbors (kNN)|kNN]]. 
- **[[AWS]] Aurora DB**: Re implemented PostgreSQL, good if the goal is to already use SQL and AWS.
- **[[AWS]] Neptune Analytics**: Graph based DB for high performance graph analytics for [[GraphRAG]].
- **[[AWS]] S3 Vectors**: Cost effective and durable storage with sub-second query performance. 
- Redis
- Postgres
- Mongo
- Pinecone