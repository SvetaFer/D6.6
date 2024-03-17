from django.urls import path
# Импортируем созданное нами представление
from .views import CategoryList
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
      path('', CategoryList.as_view(), name='home'),
      path('news/', PostList.as_view(), name='news'),
      path('news/<int:post_id>', PostDetail.as_view(), name='post_detail'),
      path('news/create/', PostCreate.as_view(), name='post_create'),
      path('article/create/', PostCreate.as_view(), name='article_create'),
      path('news/<int:pk>/update/', PostUpdate.as_view(), name='product_update'),
      path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
      path('news/search', PostSearch.as_view(), name='search'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


