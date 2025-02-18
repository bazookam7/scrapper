from dao.models.nsi.tone_utterances_summary import ToneUtterancesSummary
from dao.query.base_query import BaseQuery


class ToneUtterancesSummaryQuery(BaseQuery):
    _collection_name = "tone_utterances_summary"
    _model_class = ToneUtterancesSummary

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self
