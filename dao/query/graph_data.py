from dao.models.no_sql.graph_data import GraphData
from dao.query.base_query import BaseQuery
from dao.query.mongo_query import MongoQuery

class GraphQuery(MongoQuery):
    _collection_name="graph_data"
    _model_class =GraphData

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_page_number(self, page_number: int):
        self.query_filter["page_number"] = page_number
        return self
    
    def by_timeperiod(self, timeperiods: list[str]):
        self.query_filter["timeperiod"] = {"$in": timeperiods}
        return self
     