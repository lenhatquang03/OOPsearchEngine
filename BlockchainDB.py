import pandas as pd
from haystack import Document

class BlockchainDB:
    def __init__(self, fileDestination, docs = []):
        self._fileDestination = fileDestination
        self._docs = docs
    
    def process_data(self):
        pass
    
    def getAllArticles(self):
        return self._docs
    
    def getArticle(self, id):
        check = False
        for doc in self._docs:
            if doc.id == id:
                check = True
                return doc
        if check is False:
            return "No article found!!" 
    
    def addArticle(self, doc):
        if not type(doc) is Document:
            raise TypeError("Only documents are allowed")
        self._docs.append(doc)
        return
    
    def deleteArticle(self, id):
        check = False
        for doc in self._docs:
            if doc.id == id:
                check = True
                del self._docs[self._docs.index(doc)]
        if check is False:
            return "Article not found to be deleted!!"
        return
    
    def getIndex(self, lst: list, top_k: int) -> list:
        if top_k < 0:
            raise ValueError("top_k must be a non-negative integer!!")
        df = pd.read_csv(self._fileDestination)
        idx = list(df["id"])
        titles = list(df["title"])
        order = dict(zip(titles, idx))
        desired = [order[i] for i in lst]
        if len(desired) <= top_k:
            return desired
        else:
            return desired[:top_k]
        
class ExcelDB(BlockchainDB):
    def __init__(self, fileDestination, docs = []):
        super().__init__(fileDestination, docs)
    
    # Override 
    def process_data(self, numberOfArticles):
        if numberOfArticles <= 0:
            raise ValueError("Number of articles in the database must be postive!!")
        df = pd.read_csv(self._fileDestination)
        for i in range(numberOfArticles):
            self._docs.append(Document(content = df.iloc[i]["title"] + ". " + df.iloc[i]["content"], meta={"id": df.iloc[i]["id"], "title": df.iloc[i]["title"], "summary": df.iloc[i]["summary"], "publishDate": df.iloc[i]["publishDate"].split('T')[0], "tags": df.iloc[i]["tags"], "category": df.iloc[i]["category"]}))