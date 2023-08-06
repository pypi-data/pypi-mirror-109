# =============================================================================
# Minet CrowdTangle API Client
# =============================================================================
#
# A unified CrowdTangle API client that can be used to keep an eye on the
# rate limit and the used token etc.
#
from minet.utils import (
    RateLimiterState,
    rate_limited_method
)
from minet.web import create_pool
from minet.crowdtangle.constants import (
    CROWDTANGLE_DEFAULT_TIMEOUT,
    CROWDTANGLE_DEFAULT_RATE_LIMIT,
    CROWDTANGLE_LINKS_DEFAULT_RATE_LIMIT
)
from minet.crowdtangle.leaderboard import crowdtangle_leaderboard
from minet.crowdtangle.lists import crowdtangle_lists
from minet.crowdtangle.post import crowdtangle_post
from minet.crowdtangle.posts import crowdtangle_posts
from minet.crowdtangle.search import crowdtangle_search
from minet.crowdtangle.summary import crowdtangle_summary


class CrowdTangleAPIClient(object):
    def __init__(self, token, rate_limit=None):
        if rate_limit is None:
            rate_limit = CROWDTANGLE_DEFAULT_RATE_LIMIT
            summary_rate_limit = CROWDTANGLE_LINKS_DEFAULT_RATE_LIMIT
        else:
            rate_limit = rate_limit
            summary_rate_limit = rate_limit

        self.token = token
        self.rate_limiter_state = RateLimiterState(rate_limit, period=60)
        self.summary_rate_limiter_state = RateLimiterState(summary_rate_limit, period=60)
        self.pool = create_pool(timeout=CROWDTANGLE_DEFAULT_TIMEOUT)

    def leaderboard(self, **kwargs):
        return crowdtangle_leaderboard(
            self.pool,
            token=self.token,
            rate_limiter_state=self.rate_limiter_state,
            **kwargs
        )

    @rate_limited_method('rate_limiter_state')
    def lists(self, **kwargs):
        return crowdtangle_lists(
            self.pool,
            token=self.token,
            **kwargs
        )

    @rate_limited_method('rate_limiter_state')
    def post(self, post_id, **kwargs):
        return crowdtangle_post(
            self.pool,
            post_id,
            token=self.token,
            **kwargs
        )

    def posts(self, sort_by='date', **kwargs):
        return crowdtangle_posts(
            self.pool,
            token=self.token,
            rate_limiter_state=self.rate_limiter_state,
            sort_by=sort_by,
            **kwargs
        )

    def search(self, terms, sort_by='date', **kwargs):
        return crowdtangle_search(
            self.pool,
            token=self.token,
            rate_limiter_state=self.rate_limiter_state,
            terms=terms,
            sort_by=sort_by,
            **kwargs
        )

    @rate_limited_method('summary_rate_limiter_state')
    def summary(self, link, **kwargs):
        return crowdtangle_summary(
            self.pool,
            link,
            token=self.token,
            **kwargs
        )
