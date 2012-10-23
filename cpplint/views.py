import os
import string

from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import render
from django.template.defaultfilters import escape

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

      lint = {}
      for line in stdout:
        if line.startswith("Done processing") or line.startswith("Total errors found"):
          continue
        line_no, comment = line[2:].split(":", 1)
        lint[max(0, int(line_no) - 1)] = string.strip(comment)

      env['lint_count'] = len(lint)
      env['lint_result'] = [{
          'line': line.replace('\t', ' ' * 4),
          'lint': lint[line_no] if line_no in lint else None,
          'line_number': line_no + 1
        } for line_no, line in enumerate(their_code.split('\n'))
      ]

  return render(request, 'templates/submit.htm', env)
