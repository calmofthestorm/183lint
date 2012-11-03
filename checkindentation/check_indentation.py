#!/usr/bin/python

# Extremely fast and crude script to approximately check indentation. We make
# a lot of bad assumptions here but it's better than nothing.

import os, sys, collections, re

indent_regex = re.compile("^([ \t]*)")
statement_end_regex = re.compile("^.*(?:\\;|{)[ \t]*(?://)?[ \t]*$")
label_regex = re.compile("[ \t]*[_0-9a-zA-Z]\\:")
array_decl_regex = re.compile("\\[[0-9]*\\]")

def warning(line, text):
  return "-:%i:%s" % (line + 1, text)

SYMS = (("4 spaces", "    "),
        ("3 spaces", "   "),
        ("2 spaces", "  ") ,
        ("tabs", "\t"))

def check_indentation(infile):
  # Count indents
  count = collections.defaultdict(list)
  enforce_indent = True
  level = 0
  for lineno, line in enumerate(infile):
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
        yield warning(lineno, "Tabs and spaces found on same line. Pick a style"
                              "and stick with it.")
      else:
        # Keep track of number of lines indented each style. This lets us
        # check for inconsistencies and warn about them.
        for (k, v) in SYMS:
          if level == 0:
            break
          elif ind == v * level:
            count[k].append((lineno, level))
            break
        else:
          # Crude array check
          if (not array_decl_regex.search(line) and
              line.count("}") == line.count("{")):
            yield warning(lineno, "Does this line have a standard indentation? "
                                  "I think it should be indented %i times. "
                                  "(disregard this warning if this is a switch "
                                  "statement case)" % level)

    enforce_indent = statement_end_regex.match(line)

    level += line.count("{")
    if level < 0:
      yield warning(lineno, "Mismatched {} found; can't continue to check indent")

  # Warn if any inconsistancy
  if count and len(max(count.values(), key=len)) != sum(map(len, count.values())):
    choices = sorted(count.items(), key=lambda (name, occur): len(occur))
    fav, _ = choices[-1]
    yield warning(0, "You have a mixed indentation style. Any of 2, 3, 4 "
                     "spaces or tabs are fine but you need to be consistent.")
    yield warning(0, "You seem to have used: " + 
                     ', '.join("%i '%s'" % (len(occur), name) for (name, occur) 
                                            in reversed(choices)) +
                     ". Since %s is your favorite, showing all others as "
                     "warnings." % fav)

    for name, occur in count.items():
      if name != fav:
        for (lineno, level) in occur:
          yield warning(lineno, "Did you mean to indent %s %i "
                                "times here?" % (fav, level))

def main():
  for msg in check_indentation(sys.stdin):
    print msg

if __name__ == "__main__":
  main()
