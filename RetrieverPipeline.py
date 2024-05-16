from haystack.components.retrievers.in_memory import InMemoryBM25Retriever, InMemoryEmbeddingRetriever
from haystack.components.embedders import SentenceTransformersTextEmbedder
from haystack.components.joiners import DocumentJoiner
from haystack.components.rankers import TransformersSimilarityRanker
from haystack import Pipeline
from haystack.utils import ComponentDevice

class RetrieverPipeline(Pipeline):
    
    def __init__(self, textEmbedderModel, rankModel, embeddedDocumentStore):
        self.__textEmbedderModel = textEmbedderModel
        self.__rankModel = rankModel
        self.__embeddedDocumentStore = embeddedDocumentStore
        super().__init__()
        
    def execute(self):
        
        text_embedder = SentenceTransformersTextEmbedder(model = self.__textEmbedderModel, device = ComponentDevice.from_str("cuda: 0"), batch_size = 1)
        
        embedding_retriever = InMemoryEmbeddingRetriever(self.__embeddedDocumentStore, top_k=20)
        
        bm25_retriever = InMemoryBM25Retriever(self.__embeddedDocumentStore, top_k=20)
        
        document_joiner = DocumentJoiner(top_k = 20)
        
        ranker = TransformersSimilarityRanker(model = self.__rankModel, top_k = 20)
        
        self.add_component("text_embedder", text_embedder)
        self.add_component("embedding_retriever", embedding_retriever)
        self.add_component("bm25_retriever", bm25_retriever)
        self.add_component("document_joiner", document_joiner)
        self.add_component("ranker", ranker)

        self.connect("text_embedder","embedding_retriever")
        self.connect("embedding_retriever", "document_joiner")
        self.connect("bm25_retriever", "document_joiner")
        self.connect("document_joiner","ranker")