from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post
from .forms import PostForm

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Тестовый заголовок',
            content='Тестовое содержимое',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Тестовый заголовок')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(str(self.post), 'Тестовый заголовок')

class PostFormTest(TestCase):
    def test_valid_form(self):
        form_data = {'title': 'Новый пост', 'content': 'Содержимое'}
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_title(self):
        form_data = {'title': '', 'content': 'Содержимое'}
        form = PostForm(data=form_data)
        self.assertFalse(form.is_valid())

class PostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Тест',
            content='Контент',
            author=self.user
        )

    def test_post_list_view(self):
        response = self.client.get(reverse('post_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест')
        self.assertTemplateUsed(response, 'posts/post_list.html')

    def test_post_detail_view(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тест')
        self.assertTemplateUsed(response, 'posts/post_detail.html')

    def test_post_create_view_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('post_create'))
        self.assertEqual(response.status_code, 302)  # редирект на логин

    def test_post_create_view_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('post_create'), {
            'title': 'Новый пост',
            'content': 'Новое содержимое'
        })
        self.assertEqual(response.status_code, 302)  # редирект после создания
        self.assertEqual(Post.objects.count(), 2)