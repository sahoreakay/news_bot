import requests
from bs4 import BeautifulSoup
import redis
class scraper:
    def __init__(self,keywords):
        self.markup=requests.get('https://inshorts.com/en/read').text #it will get the markup from the whole page
        self.keywords=(keywords)
    def parser(self):
        soup=BeautifulSoup(self.markup,'html.parser')
        links=soup.findAll("a",{"class":"clickable" })
        self.saved_links=[]
        for link in links:
            #print(links)
            for keyword in self.keywords:
                if keyword.lower() in (link.text).lower():
                    self.saved_links.append(link.get('href'))
    def store(self):
        r = redis.Redis(host='localhost', port=6379, db=0)
        for link in self.saved_links:
            print(link)
            r.set(link,f"https://inshorts.com{str(link)}")
    def email(self):
         r = redis.Redis(host='localhost', port=6379, db=0)
         links=[r.get(k) for k in r.keys()]
         import smtplib
         from email.mime.multipart import MIMEMultipart
         from email.mime.text import MIMEText

         fromEmail = 'sender@gmail.com'
         toEmail = 'receiver@gmail.com'

         msg = MIMEMultipart('alternative')
         msg['Subject'] = "Link"
         msg["From"] = fromEmail
         msg["To"] = toEmail

         msg = MIMEMultipart('alternative')
         msg['Subject'] = "Link"
         msg["From"] = fromEmail
         msg["To"] = toEmail

         html = """
            <h4> %s links you might find interesting today:</h4>
            
            %s
           """ % (len(links), links)
        

         mime = MIMEText(html, 'html')

         msg.attach(mime)

         try:
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(fromEmail,'password')
            mail.sendmail(fromEmail, toEmail, msg.as_string())
            mail.quit()
            print('Email sent!')
            
         except Exception as e:
             print('Something went wrong... %s' % e)
            

         # flush redis
         r.flushdb()
       
        
         

s=scraper(['covid-19','america'])
s.parser()
s.store()
s.email()



















#link.get('href')