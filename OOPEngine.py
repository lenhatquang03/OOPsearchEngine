class SearchEngine:
    def __init__(self, query, retrievePipeline):
        self.__query = query
        self.__retrievePipeline = retrievePipeline
        
    def search(self):
        self.__retrievePipeline.execute()
        
        result = self.__retrievePipeline.run(
        {"text_embedder": {"text": self.__query}, "bm25_retriever": {"query": self.__query}, "ranker": {"query": self.__query}})
        
        return [doc.meta["title"] for doc in result["ranker"]["documents"]]
    
    @staticmethod
    def filter(lst: list) -> list:
        out = []
        for i in lst:
            if i not in out:
                out.append(i)
            else: continue
        return out    