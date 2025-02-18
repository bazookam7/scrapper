from dao.models.no_sql.management_insights import ManagementInsights
from dao.query.mongo_query import MongoQuery


class ManagementInsightsQuery(MongoQuery):
    _collection_name = "management_insights"
    _model_class = ManagementInsights

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self
    
