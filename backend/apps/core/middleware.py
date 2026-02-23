"""
Middleware personnalisé pour l'API.
"""

import logging

logger = logging.getLogger(__name__)


class LoggingMiddleware:
    """Middleware pour logger les requêtes API."""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        logger.info(f"{request.method} {request.path}")
        response = self.get_response(request)
        logger.info(f"Status: {response.status_code}")
        return response
