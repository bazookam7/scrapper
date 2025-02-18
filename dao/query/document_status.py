from dao.models.no_sql.document_status import DocumentStatus
from dao.query.base_query import BaseQuery
from dao.query.mongo_query import MongoQuery


class DocumentStatusQuery(MongoQuery):
    _collection_name = "document_status"
    _model_class = DocumentStatus

    def company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
