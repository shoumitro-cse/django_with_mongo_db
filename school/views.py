from django.views import View
from django.db.models import Sum, Count
from .models import Student
from django.shortcuts import render
from school.models import SchoolClass, Subject, Mark
from django.db.models import Q, F


class DashboardNoSqlView(View):

    def get(self, request, *args, **kwargs):
        context = dict()
        context["subjects"] = Subject.objects.all()
        context["class_list"] = SchoolClass.objects.all()
        class_id = request.GET.get('class_id', 1)
        subject_id = request.GET.get('subject_id', None)
        context["result"] = []
        if not subject_id:
            # for first bar chart
            sub_list = Subject.objects.filter(class_name_id=class_id)
            context['total_student'] = Student.objects.filter(class_name_id=class_id).count()
            for sub in sub_list:
                total_pass_mark = sub.marks.aggregate(total_mark=Sum("mark", distinct=True))["total_mark"]
                total_mark = sub.marks.filter(mark__gt=33) \
                                 .aggregate(total_mark=Count("mark", distinct=True))["total_mark"] * 100
                pass_percentage = int((total_pass_mark * 100) / total_mark) if total_pass_mark else 0
                context["result"].append({
                    "name": sub.name,
                    "pass_percentage": pass_percentage,
                    "total_student": sub.class_name.students.filter(
                        marks__subject__name=sub.name, marks__mark__gt=33).count(),
                })
            print(context["result"])
            print('total_student: ', context["total_student"])
            return render(request, 'chartapp/bar.html', context)
        else:
            # for second bar chart
            mark_objs = Mark.objects.filter(class_name_id=class_id, subject_id=subject_id)
            context['total_student'] = mark_objs.count()
            for d in Mark.GRADE_CHOICES:
                total_student = mark_objs.filter(grade=d[1]).aggregate(total_sum=Count('grade'))["total_sum"]
                percentage = int((total_student * 100) / context['total_student']) if total_student else 0
                context["result"].append({
                    "grade": d[1],
                    "percentage": percentage,
                    "total_student": total_student,
                })
            print(context["result"])
            print('total_student: ', context["total_student"])
            return render(request, 'chartapp/pie.html', context)


class DashboardSqlView(View):

    def get(self, request, *args, **kwargs):
        context = dict()
        context["subjects"] = Subject.objects.all()
        context["class_list"] = SchoolClass.objects.all()
        class_id = request.GET.get('class_id', 1)
        subject_id = request.GET.get('subject_id', None)
        context["result"] = []
        if not subject_id:
            # for first bar chart
            context['result'] = Subject.objects.filter(class_name_id=class_id) \
                .annotate(
                total_student=Count('class_name__students',
                                    filter=Q(class_name__students__marks__mark__gt=33) \
                                           & Q(class_name__students__marks__subject__name=F('name')), distinct=True),
                pass_percentage=(Sum("marks__mark", \
                                     filter=Q(marks__mark__gt=33), \
                                     distinct=True) * 100) / (Count("marks__mark", distinct=True) * 100),
            ).values('name', 'pass_percentage', 'total_student')
            context['total_student'] = Student.objects.filter(class_name_id=class_id).count()

            print(context["result"])
            print('total_student: ', context["total_student"])
            return render(request, 'chartapp/bar.html', context)
        else:
            # for second bar chart
            mark_objs = Mark.objects.filter(class_name_id=class_id, subject_id=subject_id)
            context['total_student'] = mark_objs.count()
            context['result'] = mark_objs.values('grade').annotate(
                total_student=Count('grade'), percentage=(Count('grade') * 100) / context['total_student']).order_by()

            print(context["result"])
            print('total_student: ', context["total_student"])
            return render(request, 'chartapp/pie.html', context)
