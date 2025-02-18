

from dao.models.no_sql.child_chunks import ChildChunk
from dao.query.mongo_query import MongoQuery


class ChildChunksQuery(MongoQuery):
    _collection_name = "child_chunks"
    _model_class = ChildChunk

    def by_parent_chunk_id(self, parent_chunk_id: str):
        self.query_filter["parent_id"] = parent_chunk_id
        return self

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self

    def by_document_type(self, document_type: str):
        self.query_filter["document_type"] = document_type
        return self

    def by_timeperiod(self, timeperiod: str):
        self.query_filter["timeperiod"] = timeperiod
        return self
    
    def by_chunk_type(self, chunk_type: str):
        self.query_filter["chunk_type"] = chunk_type
        return self

