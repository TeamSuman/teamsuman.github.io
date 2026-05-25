from django.test import TestCase, Client
from django.urls import reverse
# from .models import HomePageConfiguration, HeroSlide
# Need to import models, but ensure they are available

class HomePageTest(TestCase):
    def test_home_page_config(self):
        from .models import HomePageConfiguration, HeroSlide

        # Create Config
        config = HomePageConfiguration.objects.create(
            about_title="Test About",
            about_content="<p>Test Content</p>",
            research_title="Test Research",
            research_heading="Test Heading",
            research_description="<p>Test Description</p>"
        )

        # Create Slides
        slide1 = HeroSlide.objects.create(caption_title="Slide 1", my_order=1)
        slide2 = HeroSlide.objects.create(caption_title="Slide 2", my_order=0)

        # Test View
        client = Client()
        response = client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['home_config'], config)
        self.assertEqual(list(response.context['slides']), [slide2, slide1])

        # Check content in content
        content = response.content.decode('utf-8')
        self.assertIn("Test About", content)
        self.assertIn("Test Heading", content)
        self.assertIn("Slide 1", content)
