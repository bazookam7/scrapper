from dao.models.nsi.sentiment_overall_summary import SentimentOverallSummary
from dao.query.base_query import BaseQuery
from dao.query.mongo_query import MongoQuery


class SentimentOverallSummaryQuery(MongoQuery):
    _collection_name = "sentiment_overall_summary"
    _model_class = SentimentOverallSummary

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self
