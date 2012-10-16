import smtplib, os, sys
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
from email import Encoders

def send_mail(send_from, send_to, subject, text, files=[], server="localhost"):
  assert type(send_to)==list
  assert type(files)==list

  msg = MIMEMultipart()
  msg['From'] = send_from
  msg['To'] = COMMASPACE.join(send_to)
  msg['Date'] = formatdate(localtime=True)
  msg['Subject'] = subject

  msg.attach( MIMEText(text) )

  for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload( open(f,"rb").read() )
    Encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part)

  smtp = smtplib.SMTP(server)
  smtp.sendmail(send_from, send_to, msg.as_string())
  smtp.close()

def main():
  if len(sys.argv) != 2:
    print "Usage: %s style_grades" % sys.argv[0]
    return

  os.chdir(sys.argv[1])
  for student in os.listdir("."):
    try:
      print "Emailing student", student
      attachments = [os.path.abspath("%s/%s") % (student, fn)
                     for fn in os.listdir(student)]
      send_mail("183help@umich.edu", ["%s@umich.edu" % student],
                "[EECS 183 - Wolfsburg] - Project Style Grade", "", attachments)
    except Exception, error:
      print "Problem processing student", student
      if raw_input("Raise?").lower() == "y":
        raise

if __name__ == "__main__":
  main()
