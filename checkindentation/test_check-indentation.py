import os
import sys

from check_indentation import check_indentation

FILES = [
  "awful.cpp",
  "bad.cpp",
  "mixed.cpp",
  "perfect.cpp",
  "tabs.cpp"
  ]

RESOURCES = "resources"

def test_files():
  for fn in FILES:
    yield check_file, fn

def check_file(fn):
  """Test that all files output is what should have been emitted
     disregarding order."""
  base = "%s/%s" % (RESOURCES, fn)
  if os.path.exists(base) and os.path.exists("%s.out" % base):
    gold = sorted(filter(None, open("%s.out" % base).read().split("\n")))
    calc = sorted(filter(None, check_indentation(open(base))))
    assert gold == calc
  else:
    print >> sys.stdout, "WARNING: Test %s is redacted and not available." % fn
    assert False
