from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from helpers.pr import pr

from . import services


class CourseListView(View):
    def get(self, request: HttpRequest):
        courses = services.get_published_courses()
        context = pr({"courses": courses}, "CourseListView.get")
        return render(request, "courses/list.html", context)


class CourseDetailView(View):
    def get(self, request: HttpRequest, id: int):
        course = services.get_course_detail(id)
        if course is None:
            raise Http404()
        context = pr({"course": course}, "CourseDetailView.get")
        return render(request, "courses/detail.html", context)


class LessonDetailView(View):
    def get(self, request: HttpRequest, id: int):
        lesson = services.get_lesson_detail(id)
        if lesson is None:
            raise Http404()
        context = pr({"lesson": lesson}, "LessonDetailView.get")
        return render(request, "courses/lesson.html", context)
