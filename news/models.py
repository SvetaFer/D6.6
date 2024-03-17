from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse



class Author(models.Model):
    full_name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating_com'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating_com'), 0))
        self.rating = author_posts_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] \
                    + author_post_comment_rating['comments_rating_sum']
        self.save()
    def __str__(self):
        return self.full_name.title()

sport = 'SP'
politics = 'PO'
economics = 'EC'
weather = 'WE'

CATEGORY_TYPES = [
    (sport, 'Спорт'),
    (politics, 'Политика'),
    (economics, 'Экономика'),
    (weather, 'Погода'),
]


class Category(models.Model):
    name = models.CharField(max_length=2, unique=True, choices=CATEGORY_TYPES, default=weather)

    def __str__(self):
        return self.name.title()


article = 'AR'
news_ = 'NW'
TYPES = [
    (article, 'Статья'),
    (news_, 'Новость')
]


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPES, default=news_)
    time_in = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    header = models.CharField(max_length=255)
    content = models.TextField(default="...")
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.header.title()}: {self.content[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'




class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    content_com = models.TextField()
    time_in_com = models.DateTimeField(auto_now_add=True)
    rating_com = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating_com += 1
        self.save()

    def dislike(self):
        self.rating_com -= 1
        self.save()
