import json
from django.test import TestCase, Client
from django.urls import reverse

class HealthCheckTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_health_check_endpoint_success(self):
        """
        Test that the health check endpoint responds with the correct JSON structure.
        """
        # Test both /health/ and /api/health/
        for url_name in ['health_check', 'api_health_check']:
            url = reverse(url_name)
            response = self.client.get(url)
            
            # Since the DBs are configured and running in test environment, status code should be 200 (or 503 if DB fails)
            self.assertIn(response.status_code, [200, 503])
            
            # Verify response is JSON
            self.assertEqual(response.headers['Content-Type'], 'application/json')
            
            # Parse response JSON
            data = json.loads(response.content.decode('utf-8'))
            
            # Verify root keys
            self.assertIn('status', data)
            self.assertIn('timestamp', data)
            self.assertIn('environment', data)
            self.assertIn('components', data)
            self.assertIn('system_metrics', data)
            self.assertIn('dependencies', data)
            
            # Verify overall status values
            self.assertIn(data['status'], ['healthy', 'degraded', 'unhealthy'])
            
            # Verify components check structure
            components = data['components']
            self.assertIn('database_sqlalchemy', components)
            self.assertIn('database_django', components)
            self.assertIn('stripe_payment', components)
            self.assertIn('smtp_email', components)
            
            # Check SQLAlchemy component detail keys
            self.assertIn('status', components['database_sqlalchemy'])
            self.assertIn('latency_ms', components['database_sqlalchemy'])
            
            # Check Django component detail keys
            self.assertIn('status', components['database_django'])
            self.assertIn('latency_ms', components['database_django'])
            
            # Check SMTP component detail keys
            self.assertIn('status', components['smtp_email'])
            
            # Verify system metrics structure
            sys_metrics = data['system_metrics']
            self.assertIn('disk_usage', sys_metrics)
            self.assertIn('memory_usage', sys_metrics)
            self.assertIn('load_average', sys_metrics)
            
            # Verify dependencies check contains major packages
            deps = data['dependencies']
            self.assertIn('django', deps)
            self.assertIn('sqlalchemy', deps)
            self.assertIn('stripe', deps)
