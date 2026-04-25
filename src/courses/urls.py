from django.urls import URLPattern, URLResolver, path

from . import views

urlpatterns: list[URLPattern | URLResolver] = [
    path("", views.HomeView.as_view(), name="home"),
    path("courses/", views.CourseListView.as_view(), name="courses-list"),
    path("courses/<int:id>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("lessons/<int:id>/", views.LessonDetailView.as_view(), name="lesson-detail"),
]
