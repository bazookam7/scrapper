from dao.query.base_query import BaseQuery
from dao.models.no_sql.chunks import Chunk
from dao.query.mongo_query import MongoQuery


class ChunksQuery(MongoQuery):
    _collection_name = "chunks"
    _model_class = Chunk

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self
    
    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_document_types(self, document_types: list[str]):
        self.query_filter["document_type"] = {"$in": document_types}
        return self
    
    def by_ids(self, ids: list[str]):
        self.query_filter["_id"] = {"$in": ids}
        return self
    
    def by_timeperiod(self, timeperiods: list[str]):
        self.query_filter["timeperiod"] = {"$in": timeperiods}
        return self
    
    def by_company_and_document_type(self, company_name: str, document_type: str):
        self.query_filter["company_name"] = company_name
        self.query_filter["document_type"] = document_type
        return self
    
    def by_chunk_source(self, chunk_source: str):
        self.query_filter["chunk_source"] = chunk_source
        return self
    
    def by_indx(self, start: int, end: int = None):
        if end is not None:
            self.query_filter["idx"] = {"$gte": start, "$lte": end}
        else:
            self.query_filter["idx"] = {"$gte": start}
        return self
    
    ##chunk_source:{ $nin: ["MANUAL_TRANSCRIPT"] },

    def by_chunk_source_not_in(self, chunk_source: list[str]):
        self.query_filter["chunk_source"] = {"$nin": chunk_source}
        return self

