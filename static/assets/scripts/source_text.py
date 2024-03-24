from langchain_community.document_loaders import TextLoader
import textwrap
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub

from dotenv import load_dotenv
load_dotenv()


def parse_source_file(filepath:str, query:str):
    loader = TextLoader(filepath)
    document = loader.load()
    # print(document)


    # Preprocessing Data
    def wrap_text_preserve_newline(text, width=110):
        lines = text.split("\n")  # split the input into lines based on newline characters
        wrapped_lines = [
            textwrap.fill(line, width=width) for line in lines
        ]  # wrap each line individually
        wrapped_text = "\n".join(
            wrapped_lines
        )  # join the wrap lines back using the newline char
        return wrapped_text


    # Text Splitting
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(document)

    # Embedding
    embeddings = HuggingFaceEmbeddings()
    db = FAISS.from_documents(docs, embeddings)

    # query = "What is love?"
    # What are relationships and love form the intricate tapestry of human connection
    # doc = db.similarity_search(query)
    # return wrap_text_preserve_newline(str(doc[0].page_content))

    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.8, "max_length":512})
    chain=load_qa_chain(llm, chain_type="stuff")

    the_answer = ""
    try:
        print("running")
        docsResult = db.similarity_search(query)
        the_answer = chain.run(input_documents=docsResult, question = query)
    except Exception as e:
        print(f"Error: {e}")
    
    return the_answer


if __name__ == "__main__":
    # import os
    ass = parse_source_file("/home/billy/what_is_love.txt", query="how to prevent global warming?")
    print("\n"*10)
    print(ass)
