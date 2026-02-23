#!/usr/bin/env python
"""
Tests unitaires pour le backend Django.
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'sportsbooking.settings'
    django.setup()
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    
    # Tests pour l'app authentication
    failures = test_runner.run_tests([
        "apps.auth_app.tests",
        "apps.sites.tests",
        "apps.courts.tests",
        "apps.reservations.tests",
        "apps.payments.tests",
    ])
    
    sys.exit(bool(failures))
