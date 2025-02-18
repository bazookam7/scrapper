from dao.models.no_sql.guidance_actualy import GuidanceActuals
from dao.query.mongo_query import MongoQuery


class GuidanceActualsQuery(MongoQuery):
    _collection_name = "guidance_actuals"
    _model_class = GuidanceActuals
    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self
    
    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
