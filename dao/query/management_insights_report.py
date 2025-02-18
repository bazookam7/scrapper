from dao.query.mongo_query import MongoQuery


class ManagementInsightsReportQuery(MongoQuery):
    _collection_name = "management_insights_report"
    

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self
    
