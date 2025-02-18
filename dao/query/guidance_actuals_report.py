from dao.query.mongo_query import MongoQuery
from .base_query import BaseQuery
from dao.models.no_sql.guidance_actuals_report import GuidanceActualsReport
class GuidanceActualsReportQuery(MongoQuery):
    _collection_name = "guidance_actuals_report"
    _model_class = GuidanceActualsReport

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_step(self, step: int):
        self.query_filter["step"] = step
        return self
