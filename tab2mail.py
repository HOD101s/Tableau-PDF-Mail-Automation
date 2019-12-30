import tableauserverclient as TSC
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import datetime

#open sites dictionary
#place sites.txt in same directory or provide path  to it
with open('sites.txt','r') as f:
    data = f.read()
    f.close()
    
for site in eval(data)["sites"]:
    #init_data
    site_name = site["site_name"]
    user = site["user"]
    passw = site["pass"]

    #Tableau_server_Connect
    tableau_auth = TSC.TableauAuth(user, passw, site_name)
    server = TSC.Server('http://SERVER_IP',use_server_version=True)

    #Tableau sign in
    with server.auth.sign_in(tableau_auth):
        for view in TSC.Pager(server.views):
            if view.name == "VIEW_NAME":
                print(view.id,view.content_url)

                #download pdf
                server.views.populate_pdf(view)
                #PATH to be changed to any local directory
                with open(r"C:\FILE_NAME.pdf",'wb') as f:			 
                    f.write(view.pdf)

                #pdf attachment
                #PATH to be changed to any local directory
                fo = open(r"C:\FILE_NAME.pdf",'rb')
                attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
                fo.close()
                attach.add_header('Content-Disposition','attachment',filename="KII Weekly Report.pdf")

                #html response
                html = "" #ENTER HTML RESPONSE
                HTML_Contents = MIMEText(html, 'html')

                #build message
                msg = MIMEMultipart('alternative')
                msg.attach(attach)
                msg.attach(HTML_Contents)
                msg['Subject'] = #EMAIL SUBJECT

                #send mail
                s = smtplib.SMTP('smtp.gmail.com', 587) 
                s.starttls()  
                s.login(ENTER_EMAIL,ENTER_PASS)
                msg['From'] = FROM_MAIL_ID   
                msg['To'] = site["email"]
                s.sendmail(msg['From'],msg['To'],msg.as_string()) 
                s.quit()
                break
