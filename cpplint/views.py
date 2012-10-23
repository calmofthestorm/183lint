from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.template.defaultfilters import escape

import collections

def space_escape(s):
  return escape(s).replace("\t", "&nbsp;&nbsp;").replace(" ", "&nbsp;")

import os

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file  = forms.FileField()

def invalid(request):
  return HttpResponse("Upload was not successful. <a href='/cpplint/submit>Try again</a>")

def submit(request):
  return HttpResponse("""<form method='POST' enctype='multipart/form-data' action='/cpplint/upload'>
File to upload: <input type=file name=file id=id_file><br>
<br>
<input type=hidden name=title it=id_title value=foo />
<input type=submit value=Press> to upload the file!
</form>""")

def upload(request):
  print os.getcwd()
  if request.method == 'POST':
    form = UploadFileForm(request.POST, request.FILES)
    if form.is_valid():
      their_code = request.FILES['file'].read()
      lint = collections.defaultdict(list)
      for plugin in open("cpplint/plugins.conf"):
        try:
          plugin, _ = plugin.split("#", 1)
        except ValueError:
          pass
        plugin = plugin.strip()

        if plugin:
          stdin, stdout, stderr = os.popen3("bash -c '%s'" % plugin)
          stdin.write(their_code)
          stdin.close()
          for line in stdout:
            fn, line_no, comment = line.split(":", 2)
            lint[max(0, int(line_no) - 1)].append(comment)

      response = ""
      for (line_no, line) in enumerate(their_code.split("\n")):
        if line_no in lint:
          response += "<font color=red>%s</font><br/>" % space_escape(line) + "\n"
          for comment in lint[line_no]:
            response += "<font color=green>// ^^^ SUGGESTION: %s</font><br/>" % space_escape(comment.replace("\n", "")) + "\n"
        else:
          response += space_escape(line) + "<br/>" + "\n"

      return HttpResponse("<h1>Comments will appear in green and the lines they apply to in red.</h1><h2> There are a total of %i suggestions for this file.</h2>" % sum(map(len, lint.values())) + response)
    else:
      return HttpResponseRedirect('/cpplint/invalid')
