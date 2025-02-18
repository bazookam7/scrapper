from dao.models.nsi.chunks_utterances import ChunksUtterances
from dao.query.base_query import BaseQuery
from dao.query.mongo_query import MongoQuery


class ChunksUtterancesQuery(MongoQuery):
    _collection_name = "chunks_utterances"
    _model_class = ChunksUtterances

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self
    
    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self
    
    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    