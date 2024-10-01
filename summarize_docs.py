#This file summarizes the documents, creates embeddings, and saves the data to a pickle file.

import os
import pickle
import prompts
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate

#1. Setup
# Define the directory containing the markdown files
clickable_url_prefix = "https://github.com/semaphoreci/semaphore/tree/main/docs/"
docs_directory = "../semaphore/docs/"
output_dir = "summarized_docs/"
model_to_use = "gpt-4o-mini"
output_pickle_file_name = "texts_and_embeddings.pkl"
output_pickle_file_path = os.path.join(output_dir, output_pickle_file_name)

# Check if output_dir is missing. mkdir if missing.
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

summaries = []
summary_metadata = []

# Optional: Prompt the user for the API key
#import getpass
#os.environ["OPENAI_API_KEY"] = getpass.getpass()

#2.0 Setting the Langchain objects
##2.1 Setting up a Langchain "model" object
model = ChatOpenAI(model=model_to_use).with_structured_output(None, method="json_mode")
##2.2 Setting up our prompt template
our_prompt_template = ChatPromptTemplate.from_messages(
    [ ("user", prompts.summarize_and_augment_prompt)]
)
#2.3 Set up the embeddings model
embeddings = OpenAIEmbeddings()

#3.0 Loop through and summarize the markdown files.
for root, dirs, files in os.walk(docs_directory):
    #3.1 We loop through the markdown files only
    for filename in [ fi for fi in files if fi.endswith(".md") ]:        
        file_path = os.path.join(root, filename)
        #3.2 Read the contents of the markdown file
        with open(file_path, "r") as file:
            content = file.read()
            #3.3 Use the LLM to summarize the markdown file
            our_path = file_path.replace(docs_directory,"")
            clickable_url = clickable_url_prefix + our_path
            chain = our_prompt_template | model 
            json_formatted = chain.invoke({"path": our_path, "doc": content})
            #3.4 Append to the summary and path to the lists
            the_summary = json_formatted["what_path_suggests"]
            the_summary += "\n"
            the_summary += json_formatted["what_is_the_document_about"]
            the_summary += "\n"
            the_summary += json_formatted["summarize_document"]
            the_summary += "\n"
            summaries.append(the_summary)
            summary_metadata.append({"source": clickable_url})
            #3.5 Optional: Write the sumarised file to disk
            s_file_name = os.path.join(output_dir, our_path.replace("/","_"))
            with open(s_file_name, "w") as s_file:
                print(s_file_name)
                path_spec_text = "Path to file: {0} \n\n".format(our_path)
                s_file.write(the_summary)

#4.0 Generate the embeddings
print("Embedding summaries...")
summary_embeddings = embeddings.embed_documents(summaries)
#5.0 zip everything together and save to disk
text_embedding_metadata_triplets = {"embeddings":zip(summaries, summary_embeddings), "meta": summary_metadata}
with open(output_pickle_file_path, "wb") as p_file:
    pickle.dump(text_embedding_metadata_triplets, p_file)
