#This file has the chatbot

import os
import pickle
import prompts
from textwrap import dedent
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_core.runnables import RunnablePassthrough


#0. Function used to arrange the search results. Could be used in other code.
def format_docs(docs):
    """
    This function formats the documents for insertion into the RAG prompt
    """
    doc_template_string = dedent("""
    <document source="{the_source}">
    {content}
    </document>""")
    return "\n\n".join(doc_template_string.format(content=doc.page_content,the_source=doc.metadata["source"]) for doc in docs)


if __name__ == "__main__":
    # Optional: Prompt the user for the API key
    #import getpass
    #os.environ["OPENAI_API_KEY"] = getpass.getpass()

    #1. Setup
    model_to_use = "gpt-4o-mini"
    docs_dir = "summarized_docs/"
    docs_pickle_file_name = "texts_and_embeddings.pkl"
    docs_pickle_file_path = os.path.join(docs_dir, docs_pickle_file_name)

    with open(docs_pickle_file_path, "rb") as p_file:  
        text_embedding_metadata_triplets = pickle.load(p_file)


    #2.0 Setting the Langchain objects
    ##2.1 Setting up a Langchain "model" object
    model = ChatOpenAI(model=model_to_use).with_structured_output(None, method="json_mode")
    ##2.2 Setting up our prompt template
    our_prompt_template = ChatPromptTemplate.from_messages(
        [ ("system", prompts.rag_system_prompt), ("user", prompts.rag_user_prompt)]
    )
    #2.3 Set up the embeddings model
    embeddings = OpenAIEmbeddings()

    #3.0 Setting up the retriever
    faiss_vectorstore = FAISS.from_embeddings(text_embedding_metadata_triplets["embeddings"], embeddings,text_embedding_metadata_triplets["meta"])
    retriever = faiss_vectorstore.as_retriever()

    #4.0 Setting up the RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | our_prompt_template
        | model

    )

    #5.0 Calling the RAG chain in a loop to answer question in the terminal
    while True:
        user_question = input("Your question: ")
        rag_answer = rag_chain.invoke(user_question)
        print("\nBot's answer: {0}\n".format(rag_answer["answer"]))
        print("For more details see: {0}\n\n".format(rag_answer["sources"]))
    


