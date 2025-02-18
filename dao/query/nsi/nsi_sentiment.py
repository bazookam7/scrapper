from dao.models.nsi.nsi_sentiment import NsiSentiment
from dao.query.base_query import BaseQuery
from dao.query.mongo_query import MongoQuery


class NsiSentimentQuery(MongoQuery):
    _collection_name = "nsi_sentiment"
    _model_class = NsiSentiment

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self

    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self

