from dao.models.nsi.nsi_sentiment import NsiSentiment
from dao.models.nsi.nsi_tone import NsiTone
from dao.query.base_query import BaseQuery


class NsiToneQuery(BaseQuery):
    _collection_name = "nsi_tone"
    _model_class = NsiTone

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self

    def by_time_period(self, time_period: str):
        self.query_filter["time_period"] = time_period
        return self

