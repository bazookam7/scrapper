from dao.models.no_sql.company import Company
from dao.query.mongo_query import MongoQuery


class CompanyQuery(MongoQuery):
    _model_class = Company
    _collection_name = "company"

    def by_industry(self, industry: str):
        self.query_filter["industry"] = industry
        return self
    
    def by_company_name(self, name: str):
        self.query_filter["name"] = name
        return self