from dao.query.mongo_query import MongoQuery
from .base_query import BaseQuery
from dao.models.no_sql.guidance_actuals_summaries import GuidanceActualsSummaries
class GuidanceActualsSummariesQuery(MongoQuery):
    _collection_name = "guidance_actuals_summaries"
    _model_class = GuidanceActualsSummaries

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
