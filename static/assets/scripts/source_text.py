from langchain_community.document_loaders import TextLoader
import textwrap
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


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
    doc = db.similarity_search(query)
    return wrap_text_preserve_newline(str(doc[0].page_content))


if __name__ == "__main__":
    # import os
    ass = parse_source_file("../../../uploads/climate.txt", query="is global warming bad?")
    print("\n"*10)
    print(ass)
