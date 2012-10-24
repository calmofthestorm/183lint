import collections
import os

from django import forms
from django.shortcuts import render

class UploadFileForm(forms.Form):
  file  = forms.FileField()

def upload(request):
  env = {}
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      # Prepare to process their code
      their_code = request.FILES['file'].read()
      their_code_lines = their_code.split('\n')
      lint = collections.defaultdict(list)

      # Execute all plugins
      with open('cpplint/plugins.conf') as plugin_file:
        for plugin in plugin_file:
          plugin = plugin.strip() if plugin[0] != '#' else None

          if plugin:
            stdin, stdout, stderr = os.popen3("bash -c '%s'" % plugin)
            stdin.write(their_code)
            stdin.close()
            for line in stdout:
              filename, line_no, comment = line.split(":", 2)
              lint[max(0, int(line_no) - 1)].append(comment)

      # Format and return the response
      env['lint_count'] = len(lint)
      env['lint_result'] = [{
          'line': line.replace('\t', ' ' * 4),
          'lint': lint[line_no] if line_no in lint else None,
          'line_number': line_no + 1
        } for line_no, line in enumerate(their_code_lines)
      ]

  return render(request, 'templates/submit.htm', env)

