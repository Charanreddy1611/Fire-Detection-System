import smtplib
import os
import imghdr
from email.message import EmailMessage
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import requests

def get_gps_location():
    response = requests.get('https://ipinfo.io/json')
    data = response.json()
    coordinates = data['loc'].split(',')
    latitude = coordinates[0]
    longitude = coordinates[1]
    return latitude, longitude

def create_stats_pie_chart(count):
    if count > 10:
        colors = ['red', 'green']
        labels = ['high alert! more persons to save', ' persons  to be saved']
        sizes = [count, 10]
    else:
        colors = ['green', 'red']
        labels = ['persons to be saved', 'high alert! more persons to save']
        sizes = [count, 10]

    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title('Statistics')
    plt.axis('equal')

def send_email_with_attachment(receiver_email, attachment_path):
    sender_email = "sairohitha1@gmail.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    username = "sairohitha1@gmail.com"
    password = "iphj vldh xqoa fvwf"

    latitude, longitude = get_gps_location()
    maps_url = f'https://www.google.com/maps/search/?api=1&query={latitude},{longitude}'

    message = EmailMessage()
    message['Subject'] = f'Statistics and gps - GPS Location: {latitude}, {longitude}'
    message['From'] = sender_email
    message['To'] = receiver_email
    message.set_content('Please find the attached pie chart.\n\nGPS Location: '
                        f'Latitude: {latitude}, Longitude: {longitude}'
                        f'Click the link to view the location on Maps: {maps_url}')

    with open(attachment_path, 'rb') as file:
        file_data = file.read()
        file_type = imghdr.what(file.name)
        file_name = os.path.basename(file.name)

    message.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(message)
        print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Error sending email:", e)

def main():
    count = int(input("Enter the count of persons: "))
    save_path = os.path.join(os.path.expanduser("~"), "Desktop", "stats_pie_chart.png")
    create_stats_pie_chart(count)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print("Pie chart saved successfully at:", save_path)

    receiver_email = 'recipient_email@gmail.com'
    send_email_with_attachment(receiver_email, save_path)

if _name_ == '_main_':
    main()