from dao.query.mongo_query import MongoQuery
from dao.models.no_sql.transcript_metrics import TranscriptMetrics

class TranscriptMetricsQuery(MongoQuery):
    _collection_name = "transcript_metrics"
    _model_class = TranscriptMetrics

    def by_company_name(self, company_name: str):
        self.query_filter["company_name"] = company_name
        return self
