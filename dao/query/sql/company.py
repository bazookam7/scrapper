from dao.models.sql.company import Company
from dao.query.sql_query import SQLQuery



class CompanyQuery(SQLQuery):
    _model_class = Company


    def by_industry(self, industry: str):
        self._sql_query = self._sql_query.where(self._model_class.industry == industry)
        return self
    
    def by_company_name(self, name: str):
        self._sql_query = self._sql_query.where(self._model_class.name == name)
        return self
    
    def by_rag_available(self, rag_available: int):
        self._sql_query = self._sql_query.where(self._model_class.rag_available == rag_available)
        return self
    
    def by_work_station_available(self, work_station_available: int):
        self._sql_query = self._sql_query.where(self._model_class.work_station_available == work_station_available)
        return self
