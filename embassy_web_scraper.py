from email.message import EmailMessage
import smtplib, ssl
from bs4 import BeautifulSoup
import requests
import time

def send_email(emb_email, emb_name, emb_country):

    global email
    pwd = '' #place email third party access password here
    message = EmailMessage()
    message["From"] = email
    message["To"] = emb_email
    message["Subject"] = "Special Request"
    message.set_content(f"""Dear {emb_name},\n 
**** Insert email message here ****""")
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, 
                            context=ssl.create_default_context ()) as server:
        server.login(email, pwd)
        server.send_message(message)
    

def retrieve_emails():
    
    link = requests.get('https://travel.state.gov/content/travel/en/consularnotification/ConsularNotificationandAccess.html').text
    soup = BeautifulSoup(link, 'lxml')
    country_sections = soup.find('div', class_='tsg-rwd-side-menu-iparsys iparsys parsys').find_all('a', href=True)
    my_dict = {}
    
    with open('embassiesinWash.txt', 'w', encoding='utf-8') as file:
    
        for country in country_sections:
            country_name = country.text
            country_link = requests.get('https://travel.state.gov' + str(country.get('href'))).text
            second_soup = BeautifulSoup(country_link, 'lxml')

            country_skips = ['Greenland', 'Seychelles', 'Turks and Caicos Islands', 'Burundi', 'Sudan', 'Suriname', 'Iceland', 'Slovakia', 'Switzerland', 'Sri Lanka']
            
            if country_name in country_skips:
                continue

            if 'Venezuela' in country_name:
                embassy_name = 'Embassy of Venzuela'
                embassy_email = 'serviciosconsulares@us.embajadavenezuela.org'
                file.write('COUNTRY\n')
                file.write(country_name + '\n')
                file.write(embassy_name + '\n')
                file.write(embassy_email + '\n')
                break
            

            if country_name not in (second_soup.find('div', class_='tsg-rwd-csi-contry-name').text):
                continue

            email_blocks = second_soup.find('div', class_='tsg-rwd-consular-notifications-fram-for-info').find_all('a')

            for em_block in email_blocks:
            
                if 'Embassy' in em_block.text:
                    embassy_email = str(em_block.get('href'))
                    embassy_email = embassy_email[7:]
                    embassy_name = 'Embassy of ' + str(country.text)
                    break
                    
                else:
                    embassy_email = str(em_block.get('href'))
                    embassy_email = embassy_email[7:]
                    embassy_name = em_block.text
                    embassy_name = embassy_name[10:]
            
            if country_name == 'Antigua and Barbuda':
                embassy_name = 'Embassy of Antigua and Babuda'
            if country_name == 'Canada':
                embassy_name = 'Embassy of Canada'
            if country_name == 'Russian Federation':
                country_name = 'Russia'
                embassy_name = 'Embassy of Russia'
            if country_name == 'Taiwan':
                embassy_name = 'Embassy of Taiwan'
                
            my_dict[country_name] = [embassy_name, embassy_email]
            
            #print(country_name)
            #print(embassy_name)
            #print(embassy_email)
            
            #embassy will not always be the first one
            #if embassy not found, email all the consulates
            
            file.write('COUNTRY\n')
            file.write(country_name + '\n')
            file.write(embassy_name + '\n')
            file.write(embassy_email + '\n')
        
        file.close()

def database_parsing():

    emb_contacted = ['Sri Lanka']
    
    with open('embassiesinWash.txt', 'r') as file:
    
        text = file.read()
        countries = text.split('COUNTRY\n')
        del countries[0]
        database = []
        
        for trip in countries:
        
            list = trip.split('\n')
            del list[-1]
            country_name = list[0]
            
            if country_name in emb_contacted:
                continue
                
            embassy_name = list[1]
            embassy_email = list[2]
            #send_email(embassy_email, embassy_name, country_name)   uncomment when ready to send emails
            

def main():
    
    df = database_parsing()

if __name__ == '__main__':
    main()
