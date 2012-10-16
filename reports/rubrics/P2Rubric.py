rubric = \
{"Indentation":
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
for (item, levels) in rubric.iteritems():
  if min(levels.iterkeys()) >= -1:
    levels[-2] = None
  for i in range(-1, 3):
    levels.setdefault(i, None)
