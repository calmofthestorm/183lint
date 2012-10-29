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

SYMS = {"tabs":"\t", "2 spaces":"  ", "3 spaces":"   ", "4 spaces":"    "}

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
      else:
        for (k, v) in SYMS.items():
          if ind == v * level:
            count[k].append((lineno, level))
            break
        else:
          # Crude array check
          if not array_decl_regex.search(line) and line.count("}") == line.count("{"):
            warn(lineno, "Does this line have a standard indentation? I think it should be indented %i times. (disregard this warning if this is a switch statement case)" % level)

    enforce_indent = statement_end_regex.match(line)

    level += line.count("{")
    if level < 0:
      warn(lineno, "Mismatched {} found; can't continue to check indent")

  # Warn if any inconsistancy
  if max(count.values(), key=len) != sum(map(len, count.values())):
    print >> sys.stderr, "HI"
    choices = sorted(count.items(), key=lambda (name, occur): len(occur))
    fav, _ = choices[-1]
    warn(0, "You have a mixed indentation style. Any of 2, 3, 4 spaces or tabs are fine but you need to be consistent.")
    warn(0, "You seem to have used: " + ', '.join("%i '%s'" % (len(occur), name)
                                                  for (name, occur)
                                                  in reversed(choices)) +
            ". Since %s is your favorite, showing all others as warnings." % fav)

    for name, occur in count.items():
      if name != fav:
        for (lineno, level) in occur:
          warn(lineno, "Did you mean to indent %s %i times here?" % (fav, level))

if __name__ == "__main__":
  main()
