from haystack.components.writers import DocumentWriter
from haystack.components.embedders import SentenceTransformersDocumentEmbedder
from haystack.components.preprocessors import DocumentSplitter
from haystack.utils import ComponentDevice
from haystack import Pipeline

class IndexPipeline(Pipeline):

    def __init__(self, docEmbedderModel, docs, documentStore):
        self.__docEmbedderModel = docEmbedderModel
        self.__documentStore = documentStore
        self.__docs = docs
        super().__init__()
    
    def getDocumentStore(self):
        return self.__documentStore
    
    def execute(self):
        
        document_splitter = DocumentSplitter(split_by = "word", split_length = 30, split_overlap=5)
        
        document_embedder = SentenceTransformersDocumentEmbedder(model = self.__docEmbedderModel, batch_size = 5, device = ComponentDevice.from_str("cuda: 0"))
        
        document_writer = DocumentWriter(self.__documentStore)
        
        self.add_component("document_splitter", document_splitter)
        self.add_component("document_embedder", document_embedder)
        self.add_component("document_writer", document_writer)
        
        self.connect("document_splitter", "document_embedder")
        self.connect("document_embedder", "document_writer")
        
        self.run({"document_splitter": {"documents": self.__docs}})