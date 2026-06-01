from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post


class BlogTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@email.com',
            password='secret'
        )

        # Modelda Body katta harf bilan bo'lgani uchun bu yerda ham Body yozamiz
        self.post = Post.objects.create(
            title='Yangi post',
            Body='Post matni',
            author=self.user,
        )

    def test_string_representation(self):
        post = Post(title='Post mavzusi')
        self.assertEqual(str(post), post.title)

    def test_post_content(self):
        self.assertEqual(f'{self.post.title}', 'Yangi post')
        self.assertEqual(f'{self.post.author}', 'testuser')
        self.assertEqual(f'{self.post.body}', 'Post matni')  # Katta B harfi bilan

    def test_post_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post matni')
        self.assertTemplateUsed(response, 'home.html')

    def test_post_detail_view(self):
        # Dinamik ravishda post ID si orqali URL olamiz (xavfsiz yo'l)
        response = self.client.get(reverse('post_detail'))
        no_response = self.client.get('/post/100000/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)

        # Sahifa ichida 'Yangi post' sarlavhasi borligini tekshiramiz
        self.assertContains(response, 'Yangi post')
        self.assertTemplateUsed(response, 'post_detail.html')