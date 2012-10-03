from django.db import models
from django.contrib.admin.models import User

import annoying.fields
import django.core.exceptions

# Create your models here.
class Student(models.Model):
  """Represents one EECS 183 student."""
  name = models.CharField(max_length=200)
  uniqname = models.CharField(max_length=200)

  def __unicode__(self):
    return unicode(self.uniqname)

class Project(models.Model):
  """Represents a single assigned project."""
  name = models.CharField(max_length=200)
  points = models.IntegerField()

  def __unicode__(self):
    return unicode(self.name)

class Submission(models.Model):
  """Represents one student's submission to a project."""
  student = annoying.fields.AutoOneToOneField(Student)
  date = models.DateTimeField('date submitted')
  project = models.ForeignKey(Project)
  grader = models.ForeignKey(User, null=True)

  def __unicode__(self):
    try:
      return u"%s's %s" % (self.student.uniqname, self.project.name)
    except django.core.exceptions.ObjectDoesNotExist:
      return u"Broken"

class SubmissionGrade(models.Model):
  """Represents one grader's grading one project."""
  grader = annoying.fields.AutoOneToOneField(User)
  submission = models.ForeignKey(Submission)
  comments = models.TextField(null=True)
  adjustment = models.IntegerField(default=0)
  complete = models.BooleanField(default=False)

  def __unicode__(self):
    try:
      return u"<graded %s %i/%i>" % (unicode(self.submission), self.total_score,
                                     self.submission.project.points)
    except django.core.exceptions.ObjectDoesNotExist:
      return u"Broken"

class LineItem(models.Model):
  """Represents one item on a project and the best possible score for it."""
  project = models.ForeignKey(Project)
  name = models.CharField(max_length=200)
  description = models.TextField()
  points = models.IntegerField()

  def __unicode__(self):
    try:
      return u"%s: up to %i" % (self.name, self.points)
    except django.core.exceptions.ObjectDoesNotExist:
      return u"Broken"

class LineGrade(models.Model):
  """Represents one student's points earned on one item."""
  submissiongrade = models.ForeignKey(SubmissionGrade)
  lineitem = annoying.fields.AutoOneToOneField(LineItem)
  points = models.IntegerField()

  def __unicode__(self):
    try:
      return u"%s: %i/%i" % (self.lineitem.name, self.points, self.lineitem.points)
    except django.core.exceptions.ObjectDoesNotExist:
      return u"Broken"
