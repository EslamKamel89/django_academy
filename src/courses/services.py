from courses.models import Course, Lesson, PublishStatus


def get_published_courses():
    courses = Course.objects.filter(status=PublishStatus.PUBLISHED)
    return courses


def get_course_detail(id: int | None):
    if not id:
        return None
    course = Course.objects.filter(id=id, status=PublishStatus.PUBLISHED).first()
    return course


def get_lesson_detail(id: int | None):
    if not id:
        return None
    lesson = Lesson.objects.filter(
        id=id,
        status=PublishStatus.PUBLISHED,
        course__status=PublishStatus.PUBLISHED,
    ).first()
    return lesson
