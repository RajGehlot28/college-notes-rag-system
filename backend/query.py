from rag_retrieval import RAGRetrieval

async def answer_query(query, vector_store, embedding_manager, llm_manager):
    # Retrieval Pipeline :-

    # step-1 creating vector embedding for query and retrieving relevant embeddings from vectorDB
    rag_retrieval = RAGRetrieval(vector_store, embedding_manager)
    results = await rag_retrieval.retrieve(query)

    # sending (query + retrieved-documents) to LLM and ask to generate output
    context = ""
    if len(results) == 0:
        context = "NO_CONTEXT_FOUND"
    else:
        for result in results:
            context += result.payload["text"] + "\n\n"

    prompt = f"""
            Answer the question as per the retrieved context only.
            If context is empty then return answer as - "I cannot find the answer to this question in the provided documents."

            Constraints :-
            - No extra information just give answer
            - Briefly answer question as per the retrieved context only

            Question:
            {query}
            
            Retrieved Context:
            {context}

            FINAL ANSWER:
        """
    
    answer = await llm_manager.invoke(prompt)
    return answer
