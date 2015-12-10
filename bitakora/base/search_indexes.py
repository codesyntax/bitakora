import datetime
from haystack import indexes
from bitakora.base.models import Article


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    user_blog = indexes.CharField(model_attr='blog')
    pub_date = indexes.DateTimeField(model_attr='publish_date')

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())