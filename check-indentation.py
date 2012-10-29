#!/usr/bin/python

# Extremely fast and crude script to approximately check indentation. We make
# a lot of bad assumptions here but it's better than nothing.

import os, sys, collections, re

indent_regex = re.compile("^([ \t]*)")
statement_end_regex = re.compile("^.*(?:\\;|{)[ \t]*(?://)?[ \t]*$")
label_regex = re.compile("[ \t]*[_0-9a-zA-Z]\\:")
array_decl_regex = re.compile("\\[[0-9]*\\]")

def warn(line, text):
  print "-:%i:%s" % (line + 1, text)

def main():
  # Count indents
  count = collections.defaultdict(list)
  enforce_indent = True
  level = 0
  for lineno, line in enumerate(sys.stdin):
    if not line.strip():
      continue

    # Extremely crude and error prone, but should be good enough for the course.
    level -= line.count("}")

    if enforce_indent:
      ind = indent_regex.match(line)
      if ind is None:
        ind = ""
      else:
        ind = ind.groups()[0]

      if "\t" in ind and " " in ind:
        warn(lineno, "Tabs and spaces found on same line. Pick a style and stick with it.")
      elif ind == "\t" * level:
        count["tabs"].append(lineno)
      elif ind == "  " * level:
        count["2 spaces"].append(lineno)
      elif ind == "   " * level:
        count["3 spaces"].append(lineno)
      elif ind == "    " * level:
        count["4 spaces"].append(lineno)
      else:
        # Crude array check
        if not array_decl_regex.search(line) and line.count("}") == line.count("{"):
          warn(lineno, "Does this line have a standard indentation? (disregard this warning if this is a switch statement case)")

    enforce_indent = statement_end_regex.match(line)

    level += line.count("{")
    if level < 0:
      warn(lineno, "Mismatched {} found; can't continue to check indent")

if __name__ == "__main__":
  main()
