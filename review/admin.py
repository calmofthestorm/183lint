from review.models import Student, Project, Submission, SubmissionGrade, \
                          LineItem, LineGrade
from django.contrib import admin
import django.utils.encoding

admin.site.register(Student)
admin.site.register(Submission)
admin.site.register(LineGrade)

class LineItemInline(admin.TabularInline):
  fields = ["name", "points", "description"]
  model = LineItem
  extra = 3

class ProjectAdmin(admin.ModelAdmin):
  inlines = [LineItemInline]
  list_display = ["name", "points"]

###

class LineGradeInline(admin.TabularInline):
  fields = ["points", "description"]
  readonly_fields = ["description"]
  model = LineGrade
  extra = 0

  def description(self, obj):
    return obj.lineitem.description

class SubmissionGradeAdmin(admin.ModelAdmin):
  inlines = [LineGradeInline]
  list_display = ["__unicode__", "submission", "complete"]
  list_filter = ["grader", "complete"]

admin.site.register(Project, ProjectAdmin)
admin.site.register(SubmissionGrade, SubmissionGradeAdmin)
