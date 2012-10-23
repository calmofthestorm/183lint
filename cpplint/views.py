import os
import string

from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.template.defaultfilters import escape

from verifycppbraces.BraceVerify.brace_verify import get_brace_matching
from verifycppbraces.BraceVerify.brace_verify import BLOCK
from verifycppbraces.BraceVerify.brace_verify import EGYPTIAN
from verifycppbraces.BraceVerify.brace_verify import UNKNOWN

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def invalid(request):
  return HttpResponse("Upload was not successful. <a href='/cpplint>Try again</a>")

def upload(request):
  env = {}
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      their_code = request.FILES['file'].read()
      # TODO: put this in some sort of config
      stdin, stdout, stderr = os.popen3("python %s/cpplint/cpplint.py --filter=-legal,-readability/streams,-whitespace/newline,-readability/constructors,-runtime/arrays,-build/namespaces,-runtime/string,-readability/casting,-runtime/references,-readability/streams,-whitespace/labels,-readability/todo,-runtime/threadsafe_fn,-readability/header_guard,-whitespace/braces_google,-build/include_directory -" % os.getcwd())
      stdin.write(their_code)
      stdin.close()

      their_code_lines = their_code.split('\n')

      lint = {}
      for line in stdout:
        if line.startswith("Done processing") or line.startswith("Total errors found"):
          continue
        line_no, comment = line[2:].split(":", 1)
        lint_index = max(0, int(line_no) - 1)
        if not lint_index in lint:
          lint[lint_index] = []
        lint[lint_index].append(string.strip(comment))

      braces = get_brace_matching(their_code_lines)

      brace_counts = {
          EGYPTIAN: 0,
          BLOCK: 0,
          UNKNOWN: 0
      }
      for brace in braces:
        brace_counts[brace.start_brace.brace_type] += 1

        # unknown braces
        if brace.start_brace.brace_type == UNKNOWN:
          for line_no in [brace.start_brace.line_number, brace.end_line_number]:
            line_index = line_no - 1
            if not line_index in lint:
              lint[line_index] = []
            lint[line_index].append(
              'Unknown brace type? start %s end %s' % (
                brace.start_brace.line_number,
                brace.end_line_number
              )
            )

        if brace.start_brace.index != brace.end_index:
          for line_no in [brace.start_brace.line_number, brace.end_line_number]:
            line_index = line_no - 1
            if not line_index in lint:
              lint[line_index] = []
            lint[line_index].append(
              'Mismatched brace indent. Start Line %s@%s End Line %s@%s' % (
                brace.start_brace.line_number,
                brace.start_brace.index,
                brace.end_line_number,
                brace.end_index
              )
            )

      if bool(brace_counts[EGYPTIAN]) == bool(brace_counts[BLOCK]):
        if not 0 in lint:
          lint[0] = []
        lint[0].append(
          'Inconsistent brace usage.  Egyptian: %s, Block: %s' % (
            brace_counts[EGYPTIAN],
            brace_counts[BLOCK]
          )
        )

      env['lint_count'] = len(lint)
      env['lint_result'] = [{
          'line': line.replace('\t', ' ' * 4),
          'lint': lint[line_no] if line_no in lint else None,
          'line_number': line_no + 1
        } for line_no, line in enumerate(their_code_lines)
      ]

  return render(request, 'templates/submit.htm', env)
