#! /usr/bin/env python

import sys
import os
import numpy
import random
import datetime
import shutil

import scipy.stats
import matplotlib.pyplot

import HTML


sys.path.extend(("..", "../stylist"))

def setup_environment():
  pathname = os.path.dirname(sys.argv[0])
  sys.path.append(os.path.abspath(pathname))
  sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
  sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../stylist')))
  os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Must set up environment before imports.
setup_environment()

from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.db.models.aggregates import *

from review.models import *

default_color = {-2:"Red", -20:"Red", -40:"Red", -1:"Red",
                  0:"Maroon", 1:"Teal", 2:"Green"}

def make_report(sg, rubric):
  """Pass in a SubmissionGrade from Django."""
  T = HTML.Table()

  # Iterate over all items on rubric
  for (item, levels) in rubric.iteritems():
    item = sg.linegrade_set.get(lineitem__name=item)

    # Catch graders' invalid scores
    assert levels.get(item.points, None) is not None
    row = [item.lineitem.name]

    # Iterate over all valid values for item on rubric
    for (val, level) in sorted(levels.iteritems()):
      if level:
        # Score is valid to give
        if isinstance(level, basestring):
          color = default_color[val]
          desc = level
        else:
          desc, color = level
          
        if val == item.points:
          # This is the score they got, color it appropriately
          row.append(HTML.TableCell("<font color=White>%s</font>" % desc, bgcolor=color))
        else:
          # They did not get this score. Leave it default.
          row.append(HTML.TableCell(desc))
      else:
        # This is not a valid score so just draw a grey box.
        row.append(HTML.TableCell("", bgcolor="Gray"))

    T.rows.append(row)

    # Compute their final grade
    agg = sg.linegrade_set.aggregate(Min("points"), Sum("points"))

    # Did they commit a major sin?
    if agg["points__min"] < -2:
      # Yes. They lose lots of points and don't have any further effect.
      grade = agg["points__min"]
    else:
      # Grade is a simple sum, but we won't give a negative grade for minor sins.
      grade = max(agg["points__sum"] + sg.adjustment, 0)

    report = "<h1>EECS 183 %s style grade</h1><h2>%s</h2><h3>Grade: %%i/%i <font color=RED>P2 only -- NOT included in course grade (future projects will be)</font></h3><p>%s</p>" % \
                 (sg.submission.project.name, sg.submission.student.name,
                  sg.submission.project.points, sg.comments.replace("\n", "<br/>"))

  return report + str(T), grade

def main():
  if len(sys.argv) != 4:
    print "Usage: %s project_name rubric_dict out_dir" % sys.argv[0]
    return

  _, project, rubric, outdir = sys.argv
  rubric = __import__(rubric[:-3]).rubric

  assert not os.path.exists(outdir), "Out dir must not exist."
  os.mkdir(outdir)

  grades = {}
  zeroes = {}
  reports = {}

  # Generate reports and compute curve.
#  for sg in random.sample(SubmissionGrade.objects.filter(submission__project__name=project).all(), 50):
  for sg in SubmissionGrade.objects.filter(submission__project__name=project):
    name = sg.submission.student.name
    report, grade = make_report(sg, rubric)
    reports[name] = report, grade, sg.grader.username 

    grades.setdefault(sg.grader.username, [])
    if grade > 0:
      grades[sg.grader.username].append(grade)
    else:
      zeroes.setdefault(sg.grader.username, 0)
      zeroes[sg.grader.username] += 1

  for k, v in grades.items():
    print "%s: median=%f mean=%f (sigma=%f) [awarded %i non-positives and %i perfects]" % (k, numpy.median(v), numpy.mean(v), numpy.std(v), zeroes[k], v.count(10))
    matplotlib.pyplot.clf()
    matplotlib.pyplot.hist(v)
    matplotlib.pyplot.title("Grader %s %s positive grades." % (k, project))
    matplotlib.pyplot.savefig("%s.png" % k)

  print
  median, mean, std, curve_grader, curve = max(((numpy.median(v), numpy.mean(v), -numpy.std(v), k, v) \
                                          for (k, v) in grades.items()))
  print "Curving up to median %f (std %f) (grader %s) proportionally." % (median, -std, curve_grader)

  curved_grades = {}
  gifts = []
  for (name, (report, orig_grade, grader)) in reports.iteritems():
    if orig_grade > 0:
      percentile = scipy.stats.percentileofscore(grades[grader], orig_grade)
      new_score = scipy.stats.scoreatpercentile(grades[curve_grader], percentile)
      new_score = min(max(orig_grade, int(round(new_score))), sg.submission.project.points)
      gifts.append(new_score - orig_grade)
      curved_grades.setdefault(grader, [])
      curved_grades[grader].append(new_score)

      grades[name] = (report, new_score, grader)

  print "\nPost curve:"
  for k, v in curved_grades.items():
    print "%s: median=%f mean=%f (sigma=%f) [awarded %i non-positives and %i perfects]" % (k, numpy.median(v), numpy.mean(v), numpy.std(v), zeroes[k], v.count(10))

  print

  print "Curves given:"
  for curve in set(gifts):
    print "\t %i - to %i students" % (curve, gifts.count(curve))

  for (name, (report, grade, grader)) in reports.iteritems():
    os.mkdir("%s/%s" % (outdir, name))
    open("%s/%s/report.html" % (outdir, name), 'w').write(report % grade)

if __name__ == "__main__":
  main()
