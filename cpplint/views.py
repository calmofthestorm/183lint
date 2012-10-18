from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.template.defaultfilters import escape

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
      stdin, stdout, stderr = os.popen3("python %s/cpplint/cpplint.py --filter=-legal,-readability/streams,-whitespace/newline,-readability/constructors,-runtime/arrays,-build/namespaces,-runtime/string,-readability/casting,-runtime/references,-readability/streams,-whitespace/labels,-readability/todo,-runtime/threadsafe_fn,-readability/header_guard,-whitespace/braces_google,-build/include_directory -" % os.getcwd())
      stdin.write(their_code)
      stdin.close()

      lint = {}
      for line in stdout:
        if line.startswith("Done processing") or line.startswith("Total errors found"):
          continue
        line_no, comment = line[2:].split(":", 1)
        lint[max(0, int(line_no) - 1)] = comment

      response = ""
      for (line_no, line) in enumerate(their_code.split("\n")):
        if line_no in lint:
          response += "<font color=red>%s</font><br/>" % space_escape(line) + "\n"
          response += "<font color=green>// ^^^ SUGGESTION: %s</font><br/>" % space_escape(lint[line_no].replace("\n", "")) + "\n"
        else:
          response += space_escape(line) + "<br/>" + "\n"

      return HttpResponse("<h1>Comments will appear in green and the lines they apply to in red.</h1><h2> There are a total of %i suggestions for this file.</h2>" % len(lint) + response)
    else:
      return HttpResponseRedirect('/cpplint/invalid')
