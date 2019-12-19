import tableauserverclient as TSC
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
import datetime

#open sites dictionary
with open('sites test.txt','r') as f:
    data = f.read()
    f.close()
    
for site in eval(data)["sites"]:
    #init_data
    site_name = site["site_name"]
    user = site["user"]
    passw = site["pass"]

    #Tableau_server_Connect
    tableau_auth = TSC.TableauAuth(user, passw, site_name)
    server = TSC.Server('http://192.168.5.35:8000',use_server_version=True)

    #download pdf and mail
    with server.auth.sign_in(tableau_auth):
        for view in TSC.Pager(server.views):
            if view.name == "Dashboard - KII / Sub-CQI":
                print(view.id,view.name)
                server.views.populate_pdf(view)
                with open(r"C:\Users\manas\Downloads\TableauAuto\KII Weekly Report.pdf",'wb') as f:
                    f.write(view.pdf)

                #pdf attachment
                fo = open(r"C:\Users\manas\Downloads\TableauAuto\KII Weekly Report.pdf",'rb')
                attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
                fo.close()
                attach.add_header('Content-Disposition','attachment',filename="KII Weekly Report.pdf")

                #html response
                html = "Sir/Madam,<br><br>Weekly KII Dashboard for <b>"+site_name+"Department</b> <br><br>Best Regards,<br>IT Bhaktivedanta Hospital<br><br>Acharya Test"
                HTML_Contents = MIMEText(html, 'html')

                #build message
                msg = MIMEMultipart('alternative')
                msg.attach(attach)
                msg.attach(HTML_Contents)
                msg['Subject'] = site_name+" Weekly KII Report "+datetime.datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")

                #send mail
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls()  
                s.login("ithis@bhaktivedantahospital.com", "ithis@108")
                msg['From'] = "ithis@bhaktivedantahospital.com"
                x = ["manasbass.99@gmail.com"]
                if site["email"] != "" or site["email"] != None:
                    x.append(site["email"])
                msg['To'] = ','.join(x)
                s.sendmail(msg['From'],msg['To'],msg.as_string()) 
                s.quit()
                break
