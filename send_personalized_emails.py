import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

df = pd.read_excel("/content/grades.xlsx")
df['subject'] = "Your grade report - " + df['student_name']
df['body'] = "Dear " + df['student_name']+",\n\nYour grade is: "+df['grade']+"\n\nBest regards,\nSophia"

send_email = "purple.an@gmail.com"
send_password="vifp ejml evym yizt"

server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(send_email, send_password)

for index, row in df.iterrows():
    msg = MIMEMultipart()
    msg['From'] = send_email
    msg['To'] = row['email']
    msg['Subject'] = row['subject']
    msg.attach(MIMEText(row['body'], 'plain'))

    try:
        server.send_message(msg)
        print(f"Email sent to {row['student_name']}")
    except Exception as e:
        print(f"Failed to send to {row['student_name']}:{e}")

server.quit()
print("All email sent!")
