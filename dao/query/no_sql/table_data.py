from dao.query.mongo_query import MongoQuery
from dao.models.no_sql.table_data import TableData

class TableDataQuery(MongoQuery):
    _collection_name = "table_data"
    _model_class = TableData

    def by_document_id(self, document_id: str):
        self.query_filter["document_id"] = document_id
        return self

    def by_page_number(self, page_number: int):
        self.query_filter["page"] = page_number
        return self

