from .. import jwt
from ..exception import Unauthorized
from ..exception import Forbidden


class ScopesFetcher:

    def fetch_scopes(self, request, security, required_scopes):
        if security == 'fermata.jwt':
            headers = [('x-required-scopes', ','.join(required_scopes))]
            try:
                authorized = bool(request.identity)
                scopes = request.identity.scopes
                return authorized, scopes
            except jwt.ExpiredToken:
                raise Unauthorized('the token is expired', headers=headers)
            except jwt.InvalidToken:
                raise Unauthorized('invalid token', headers=headers)
        return True, required_scopes


class Authorizer:

    def __init__(self, securities, scopes_fetcher=None):
        self.securities = securities
        self.scopes_fetcher = scopes_fetcher

    def authorize(self, request):
        for s in  self.securities:
            for security, required_scopes in s.items():
                required_scopes = set(required_scopes)
                authorized, scopes = self.scopes_fetcher.fetch_scopes(
                    request, security, required_scopes)
                scopes = set(scopes)
                headers = [
                    ('x-required-scopes', ','.join(required_scopes)), 
                    ('x-gained-scopes', ','.join(scopes))]
                if not authorized:
                    raise Unauthorized(headers=headers)
                if not required_scopes.issubset(scopes):
                    raise Forbidden(
                        f'require scopes: ({" ".join(required_scopes)}), '
                        f'gained scopes: ({" ".join(scopes)})',
                        headers=headers)
                return headers
        return []