import os
import pickle
import faiss
import numpy as np
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer


class FitnessRAG:

    def __init__(
        self,
        pdf_folder="knowledge",
        embedding_model="all-MiniLM-L6-v2",
        chunk_size=500,
        overlap=100,
    ):

        self.pdf_folder = pdf_folder
        self.chunk_size = chunk_size
        self.overlap = overlap

        print("Loading Embedding Model...")
        self.model = SentenceTransformer(embedding_model)

        self.index = None
        self.chunks = []

        self.index_file = "fitness.index"
        self.chunk_file = "chunks.pkl"

        self.build_vector_database()

    ###########################################################
    # LOAD ALL PDFS
    ###########################################################

    def load_pdfs(self):

        text = ""

        for file in os.listdir(self.pdf_folder):

            if file.endswith(".pdf"):

                pdf_path = os.path.join(self.pdf_folder, file)

                print("Loading:", file)

                reader = PdfReader(pdf_path)

                for page in reader.pages:

                    page_text = page.extract_text()

                    if page_text:

                        text += page_text + "\n"

        return text

    ###########################################################
    # CHUNK TEXT
    ###########################################################

    def chunk_text(self, text):

        chunks = []

        start = 0

        while start < len(text):

            end = start + self.chunk_size

            chunks.append(text[start:end])

            start += self.chunk_size - self.overlap

        return chunks

    ###########################################################
    # BUILD VECTOR DATABASE
    ###########################################################

    def build_vector_database(self):

        if os.path.exists(self.index_file) and os.path.exists(self.chunk_file):

            print("Loading Existing Vector Store...")

            self.index = faiss.read_index(self.index_file)

            with open(self.chunk_file, "rb") as f:

                self.chunks = pickle.load(f)

            return

        print("Creating New Vector Store...")

        text = self.load_pdfs()

        self.chunks = self.chunk_text(text)

        embeddings = self.model.encode(

            self.chunks,

            convert_to_numpy=True,

            show_progress_bar=True,

        )

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        faiss.write_index(self.index, self.index_file)

        with open(self.chunk_file, "wb") as f:

            pickle.dump(self.chunks, f)

        print("Vector Store Saved Successfully")

    ###########################################################
    # RETRIEVE
    ###########################################################

    def retrieve(self, query, top_k=5):

        query_embedding = self.model.encode(

            [query],

            convert_to_numpy=True,

        )

        distances, indices = self.index.search(

            query_embedding,

            top_k,

        )

        context = []

        for idx in indices[0]:

            if idx != -1:

                context.append(self.chunks[idx])

        return "\n\n".join(context)

    ###########################################################
    # SEARCH WITH DISTANCE
    ###########################################################

    def retrieve_with_scores(self, query, top_k=5):

        query_embedding = self.model.encode(

            [query],

            convert_to_numpy=True,

        )

        distances, indices = self.index.search(

            query_embedding,

            top_k,

        )

        results = []

        for d, idx in zip(distances[0], indices[0]):

            if idx != -1:

                results.append(

                    {

                        "distance": float(d),

                        "text": self.chunks[idx],

                    }

                )

        return results

    ###########################################################
    # GET CONTEXT
    ###########################################################

    def get_context(self, question):

        context = self.retrieve(question)

        return context
if __name__ == "__main__":

    rag = FitnessRAG()

    print("\nVector Store Created Successfully!")

    print(f"Total Chunks: {len(rag.chunks)}")

    query = input("\nAsk a question: ")

    context = rag.get_context(query)

    print("\nRetrieved Context:\n")

    print(context)    