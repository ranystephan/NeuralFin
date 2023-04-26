from django.test import TestCase, RequestFactory
from .views import PortfolioView
from .models import User, Stock, Portfolio
from users.serializers import UserSerializer

class PortfolioViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.stock = Stock.objects.create(symbol='AAPL', company_name='Apple Inc.')
        self.portfolio = Portfolio.objects.create(user=self.user, stock=self.stock, shares=10)

    def test_get_portfolio(self):
        request = self.factory.get('/portfolio/')
        request.user = self.user
        response = PortfolioView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn('user', response.data)
        self.assertIn('stock', response.data)
        self.assertIn('shares', response.data)
