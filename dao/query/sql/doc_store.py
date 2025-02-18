from typing import List
from dao.query.sql_query import SQLQuery
from dao.models.sql.doc_store import DocStoreMetadata

class DocStoreQuery(SQLQuery):
    _model_class = DocStoreMetadata


    def by_companies(self, companies: List[str]):
        self._sql_query = self._sql_query.where(self._model_class.company_name.in_(companies))
        return self
    
    def by_company_name(self, company_name: str):
        self._sql_query = self._sql_query.where(self._model_class.company_name == company_name)
        return self


    def by_document_type(self, document_type: str):
        self._sql_query = self._sql_query.where(self._model_class.document_type == document_type)
        return self
    
    def by_timeperiod(self, timeperiod: str):
        self._sql_query = self._sql_query.where(self._model_class.timeperiod == timeperiod)
        return self
    
    def by_doc_id(self, doc_id: str):
        self._sql_query = self._sql_query.where(self._model_class.doc_id == doc_id)
        return self


    def by_doc_ids(self, doc_ids: list[str]):
        self._sql_query = self._sql_query.where(self._model_class.doc_id.in_(doc_ids))
        return self
    
    def by_doc_status(self, doc_status: str):
        self._sql_query = self._sql_query.where(self._model_class.doc_status == doc_status)
        return self
    
    def by_file_category(self, file_category: str):
        self._sql_query = self._sql_query.where(self._model_class.file_category == file_category)
        return self
    
    def by_document_types(self, document_types: List[str]):
        self._sql_query = self._sql_query.where(self._model_class.document_type.in_(document_types))
        return self
    
    def by_s3_key(self, s3_key: str):
        self._sql_query = self._sql_query.where(self._model_class.s3_key == s3_key)

        return self

    





