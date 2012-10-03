#! /usr/bin/env python

import sys
import os
import random

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

from review.models import *

def main(argv=None):
  if argv is None:
    argv = sys.argv

  if len(argv) < 5:
    print "Usage: %s <PROJNAME> <P-DIR> <LIST_OF_GRADERS_WITH_PROPORTIONS> <ASSIGNMENT_OUTDIR>" % argv[0]
    return

  # Read projects
  projects = os.listdir(sys.argv[2])
  random.shuffle(projects)

  # Read graders
  graders = [line.split() for line in open(sys.argv[3])]
  graders = [(uniqname, float(prop)) for (uniqname, prop) in graders]
  assert len(set(zip(*graders)[0])) == len(graders)

  # Figure out how many projects to each grader
  weight = sum(zip(*graders)[1])
  graders = [(uniqname, int(round(len(projects) * prop / weight))) \
             for (uniqname, prop) in graders]
  graders[-1] = (graders[-1][0], len(projects) - sum(zip(*graders)[1][:-1]))
  assert sum(zip(*graders)[1]) == len(projects)

  # Divide up the work
  work = {}
  pkill = projects[:]
  for (grader, count) in graders:
    work[grader] = pkill[:count]
    del pkill[:count]
  assert sum(map(len, work.values())) == len(projects)

  # Outdir must be empty or not exist
  if not os.path.exists(sys.argv[4]):
    os.mkdir(sys.argv[4])
  elif not os.listdir(sys.argv[4]):
    pass
  else:
    assert False

  # Project must already exist in database.
  project = Project.objects.get(name=sys.argv[1])

  # Confirm
  print "About to assign:"
  for (grader, p) in work.iteritems():
    print "\t%i projects to %s" % (len(p), grader)
  print "Will write the code for them to read to", sys.argv[4]
  print

  print "Will add these submissions to project \"%s\"" % project.name
  lost_subs = project.submission_set.count()
  lost_grades = sum((sub.submissiongrade_set.count() for sub in project.submission_set.all()))
  print "\tThis project has %i line items in its rubric. Please finalize the rubric BEFORE loading the submissions or Baddness will happen:" % project.lineitem_set.count()
  for li in project.lineitem_set.all():
    print "\t\t%s: (out of %i points)" % (li.name, li.points)
  if lost_subs != 0 or lost_grades != 0:
    print "\tWill drop %i existing submissions and %i submission grades" % (lost_subs, lost_grades)
    print "\tConfirmation needed. Type yes to continue."
    if raw_input() != "yes":
      print "Bailing out because user wisely rejected data loss."
      return
  else:
    print "\tNo data will be lost by this load."

  print
  print "OK to proceed? (y/n)"
  if raw_input() != "y":
    print "OK, no changes will be made."
    return

if __name__ == '__main__':
    main()
