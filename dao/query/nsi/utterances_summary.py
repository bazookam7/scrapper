from dao.models.nsi.sentiment_utterances_summary import SentimentUtterancesSummary
from dao.query.base_query import BaseQuery
from dao.query.mongo_query import MongoQuery


class SentimentUtterancesSummaryQuery(MongoQuery):
    _collection_name = "sentiment_utterances_summary"
    _model_class = SentimentUtterancesSummary

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self
