#This file has the prompts

#This is the prompt for summarizing and augmenting the docs
summarize_and_augment_prompt = """
The document in the "document" XML tags is part of the documentation for a CI/CD tool called SemaphoreCI.
The path in the "path_to_document" XML tags is path to that particular document. Pay attention to the file and folder names because they suggest the purpose of the document.
Semaphore is a CI/CD solution to streamline developer workflows.
Semaphore features Continuous Integration and Pipelines, Deployments and Automation, Metrics and Observability, Security and Compliance, a Developer Toolkit, Test Reports, Monorepos, and Self-hosted build agents.
Semaphore works in the cloud, on-premises, and in the hybrid cloud.

<path_to_document>
{path}
</path_to_document>

<document>
{doc}
</document>

The document in the "document" XML tags is part of the documentation for a CI/CD tool called Semaphore.
The path in the "path_to_document" XML tags is path to that particular document. Pay attention to the file and folder names because they suggest the purpose of the document.

Summarize the document. Add context to the document as well. You will need to explain what task it is useful for. And where this document fits into the broader documentation.
Use the following JSON template.
{{
    "what_path_suggests": Look at the path to the document. What does the path suggest about this document's purpose?
    "what_is_the_document_about": What is this document about? How does it help us use SempahoreCI?
    "summarize_document": Summarize the document. If the document has a lot of text, then write many paragraphs. If the document has code or a template, describe what you think tha template is for. What language is the code or template in?
}}
"""

#This is the prompt for the RAG 
rag_system_prompt = """
You are helping me find my way through the Semaphore CI documentation. 
You answer my questions based on the context. And then you direct to the source of the document, where I can read more.
You must answer based on the context only. Do not use your general knowledge.
If you don't know the answer then reply with "I don't know".
You are always very optimistic and encouraging.

"""


rag_user_prompt = """
The question is in the "question" XML tags.
The context is in the "context" XML tags.
The context is made up of documents. Each "document" is delimited by its own XML tag.
Each document has a "source" property. You need to direct me to the source of the document. Because the source of the document will have more details.
Answer the question based on the context. If you don't know the answer then reply with "I don't know".

<context>
{context}
</context>


<question>
{question}
</question>

The question is in the "question" XML tags.
The context is in the "context" XML tags.
The context is made up of documents. Each "document" is delimited by its own XML tag.
Each document has a "source" property. You need to direct me to the source of the document. Because the source of the document will have more details.
Answer the question based on the context. If you don't know the answer then reply with "I don't know".

Use the following JSON template for your reply. Write valid JSON.
{{
    "answer": Answer the question. Make sure that you explain where I can find more information - in the source of the relevant documents.
    "sources": [Output the sources of the documents that you used to answer the question into this array.]
}}
"""