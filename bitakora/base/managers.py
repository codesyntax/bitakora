from django.db.models import Manager
from django.utils.timezone import now
from django.db.models import Q, Sum
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from datetime import timedelta
from itertools import chain


class PublishedManager(Manager):
    """
    Provides filter for restricting items returned by status and
    publish date when the given user is not a staff member.
    """

    def published(self, for_blog=None, for_slug=None):
        """
        For non-staff users, return items with a published status and
        whose publish and expiry dates fall before and after the
        current date when specified.
        """
        from bitakora.base.models import CONTENT_STATUS_PUBLISHED
        if for_blog:
            return self.filter(Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True),
            Q(status=CONTENT_STATUS_PUBLISHED),Q(blog=for_blog))
        return self.filter(
            Q(publish_date__lte=now()) | Q(publish_date__isnull=True),
            Q(expiry_date__gte=now()) | Q(expiry_date__isnull=True),
            Q(status=CONTENT_STATUS_PUBLISHED))

    def top_stories(self, limit=20):
        from bitakora.base.models import Article
        from bitakora.base.models import CONTENT_STATUS_PUBLISHED

        now = datetime.now()
        month_ago = now - timedelta(days=30)
        last_articles = Article.objects.filter(Q(publish_date__lte=now) & Q(publish_date__gte=month_ago) & Q(status=CONTENT_STATUS_PUBLISHED))
        return sorted(last_articles, key = lambda art: (art.get_reverse_rating(), art.get_reverse_timestamp()))

    def bookmarks(self, user, limit=25):
        from voting.models import Vote
        from bitakora.base.models import Article
        if user.is_authenticated:
            ctype = ContentType.objects.get_for_model(Article)
            results = Vote.objects.filter(content_type=ctype,time_stamp__lt=datetime.now(),user=user).values('object_id')
            return Article.objects.filter(pk__in=[item['object_id'] for item in results[:limit]]).order_by("-publish_date")
        return None

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)