# rag.py

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    Chroma
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)


class DocumentRAG:

    def __init__(self):

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.vectorstore = None

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=100
        )

    def add_documents(
        self,
        file_path: str,
        file_type: str
    ):

        if file_type == "pdf":
            loader = PyPDFLoader(file_path)
        else:
            loader = TextLoader(file_path)

        docs = loader.load()

        splits = self.text_splitter.split_documents(
            docs
        )

        if self.vectorstore is None:

            self.vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=self.embeddings
            )

        else:

            self.vectorstore.add_documents(
                splits
            )

    def retrieve(
        self,
        query: str,
        k: int = 4
    ) -> str:

        if self.vectorstore is None:
            return "No documents have been uploaded yet."

        docs = self.vectorstore.similarity_search(
            query,
            k=k
        )

        return "\n\n".join(
            [
                doc.page_content
                for doc in docs
            ]
        )