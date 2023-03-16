from smtplib import *
import csv
import emails
email="YOUR SES VERIFIED EMAIL"
password = "YOUR PASSWORD"


from_mail = "YOUR SES VERIFIED EMAIL"
to_mail = "TO MAIL"

class NotificationManager:

    def calculate_power(self,file_name):
      with open('/home/ec2-user/solar/{}'.format(file_name), 'r') as a:
        re = csv.reader(a)
        all = [i[1] for i in re]
        tot = 0
        for i in range(1, 49):
          tot += float(all[i])
        return tot

    def send_sms_ofline(self,file_name):
        res_pow = self.calculate_power(file_name)

        text = "The power output of your solar plant is calculated by our software. And the calculated power is:{}, from the above reference kindly plan your power consuption accordingly.".format("{:.2f}".format(res_pow))

        send_mail = to_mail
        connection = SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(user=email, password=password)
        print(text)
        # connection.sendmail(from_addr=email,to_addrs="aashishas0310@gmail.com",msg=f"Subject:price alert!!\n\n{flight_d.departure_city}, {flight_d.departure_code} TO {flight_d.arrival_city}, {flight_d.arrival_code}\n PRICE:{flight_d.price}")
        connection.sendmail(from_addr=email, to_addrs=send_mail, msg="Subject:Solar alart!!\n\n{}\n I will there to assit your power consuption \n\n\n Thank you,".format(text))
        connection.close()
    def send_sms_online(self,file_name):
        res_pow = self.calculate_power(file_name)
        text = "The power output of your solar plant is calculated by our software. And the calculated power is:{}, from the above reference kindly plan your power consuption accordingly.".format(res_pow)



        # Prepare the email
        message = emails.html(
            html=f"<h1>Predicted Solar Output for the Current Day</h1>{text}<strong></strong>",
            subject= "Solar alart!!",
            mail_from= from_mail,
        )

        # Send the email
        r = message.send(
            to= to_mail,
            smtp={
                "host": "email-smtp.us-west-2.amazonaws.com",
                "port": 587,
                "timeout": 5,
                "user": "AKIAZAGDZA6ZYZS7MIUR",
                "password": "BG5KPlZ3gB0PMTAWgySQ/1A9RpaPuvJMp8M6Um2TAv+U",
                "tls": True,
            },
        )
        # Prints if successfully sent.
    #send_sms(msg="fhduhf")