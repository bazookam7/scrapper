from dao.models.nsi.tone_overall_summary import ToneOverallSummary
from dao.query.base_query import BaseQuery


class ToneOverallSummaryQuery(BaseQuery):
    _collection_name = "tone_overall_summary"
    _model_class = ToneOverallSummary

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
    
    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self
