from django.test import TestCase, Client


class AboutURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        # Создаём экземпляр клиента. Он неавторизован.
        super().setUpClass()
        cls.guest_client = Client()

    def test_urls_exists_at_desired_locations(self):
        about_response = AboutURLTest.guest_client.get('/about/author/')
        self.assertEqual(about_response.status_code, 200)

        tech_response = AboutURLTest.guest_client.get('/about/tech/')
        self.assertEqual(tech_response.status_code, 200)

    def test_urls_uses_correct_templates(self):
        about_response = AboutURLTest.guest_client.get('/about/author/')
        self.assertTemplateUsed(about_response, 'about/author.html')

        tech_response = AboutURLTest.guest_client.get('/about/tech/')
        self.assertTemplateUsed(tech_response, 'about/tech.html')
