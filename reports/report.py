#! /usr/bin/env python

import sys
import os
import random
import datetime
import shutil

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

# Report generation constants. This must match the rubric on the database.
items = {"Indentation":
           {-1:("Terrible indentation", "Red"),
             0:("Needs work", "Maroon"),
             1:("A few slipups", "Teal"),
             2:("Consistent and good", "Green")},

         "Whitespace around operators":
           { 2:("Correct: one space on both sides of all operators", "Green"),
             1:("A few slipups", "Teal"),
             0:("Wrong/inconsistant", "Maroon")},

         "Good Comments":
           { 2:("Helpful comments of good quality, quantity", "Green"),
             1:("Need to work on quality, quantity, helpful", "Teal"),
             0:("Few or no useful comments", "Maroon"),
            -1:("Distracting, useless, excessive, wrong", "Red")},

         "Identifier name formatting":
           { 1:("Pick a reasonable formatting and stick with it, i.e., myVarName, my_var_name, etc", "Green"),
             0:"Fair to poor identifier formatting"},

         "Identifier names helpful":
           { 1:("Descriptive identifiers -- improves readability", "Green"),
             0:"Identifiers not descriptive or helpful"},

         "Long lines":
           { 1:("No lines over 80 chars", "Green"),
             0:"Only a few lines longer than 80 chars",
            -1:"ANY lines over 90 chars or many lines over 80 chars"},

         "Brace placement (including use for single-statement blocks)":
           {-2:"Against our guideline - makes code difficult to follow",
            -1:"inconsistent",
             0:"mostly consistent",
             1:("very consistent", "Green")},

         "Magic numbers":
           {-1:"Magic numbers present",
             0:("No magic numbers", "Green")},

         "Goto":
           {-20:"ANY use of goto whatsoever (lose half pts on entire project)",
              0:("Goto not used", "Green")},

         "Global variables":
           {-40:"ANY use of (non-const) global variables (lose full pts on entire project)",
              0:("Global variables not used", "Green")},

         "Break and Continue":
           { 0:("Do not use break or continue OR use is sparing and actively contributes to readability", "Green"),
            -1:"Excessive or irresponsible use of break/continue"},

         "Conditionals":
           {-1:"Code on same line as conditional tests, loops, etc",
             0:("Conditionals formatted properly", "Green")},
         }

# Add automatic elements
for (item, levels) in items.iteritems():
  if min(levels.iterkeys()) >= -1:
    levels[-2] = None

  for i in range(-1, 3):
    levels.setdefault(i, None)

def make_report(sg):
  """Pass in a SubmissionGrade from Django."""
  T = HTML.Table()

  # Iterate over all items on rubric
  for (item, levels) in items.iteritems():
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

    report = "<h1>EECS 183 %s style grade</h1><h2>%s</h2><h3>Grade: %i/%i</h3><p>%s</p>" % \
                 (sg.submission.project.name, sg.submission.student.name, grade,
                  sg.submission.project.points, sg.comments.replace("\n", "<br/>"))

  return report + str(T)

def main():
  pass

if __name__ == "__main__":
  main()
