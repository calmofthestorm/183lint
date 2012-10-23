import collections
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

      their_code_lines = their_code.split('\n')

      lint = collections.defaultdict(list)
      with open('cpplint/plugins.conf') as plugin_file:
        for plugin in plugin_file:
          plugin = plugin.strip() if plugin[0] != '#' else None
          if plugin:
            stdin, stdout, stderr = os.popen3("bash -c '%s'" % plugin)
            stdin.write(their_code)
            stdin.close()
            for line in stdout:
              fn, line_no, comment = line.split(":", 2)
              lint[max(0, int(line_no) - 1)].append(comment)

      env['lint_count'] = len(lint)
      env['lint_result'] = [{
          'line': line.replace('\t', ' ' * 4),
          'lint': lint[line_no] if line_no in lint else None,
          'line_number': line_no + 1
        } for line_no, line in enumerate(their_code_lines)
      ]

  return render(request, 'templates/submit.htm', env)

