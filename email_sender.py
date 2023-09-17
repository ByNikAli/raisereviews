import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

#open json
with open('list.json') as file: # change your json name file if its not list.json
    data = json.load(file)

#send email with extract data in json
for item in data:
    if 'email_1' not in item:
        continue
    email_rec = item['email_1']
    name = item['name']
    rating = item['rating']
    reviews = item['reviews']

    # Check if any of the required fields are empty or contain only whitespace
    if not name or not email_rec or not rating or not reviews:
        print(f"Skipping email for {email_rec} because one or more fields are empty or contain only whitespace")
        continue
    
    #check if address email is invalid send msg and go for next mail
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email_rec):
        print(f"Skipping email for {email_rec} because the email address is invalid")
        continue

    #check if rating and reviews are not numbers skip mail address
    try:
        rating = float(rating)
        reviews = int(reviews)
    except ValueError:
        print(f"Skipping email for {email_rec} because the rating or reviews field is not a valid integer value")
        continue
    
    #if name is not string
    if not isinstance(name, str):
        print(f"Skipping email for {email_rec} because the name field is not a valid string value")
        continue

    try:
        message = MIMEMultipart()
        message['From']='your email'
        message['To'] = email_rec
        message['subject'] = 'Enhance Your Business\'s Online Reputation'

        # Calculate z and num_reviews as before
        if int(reviews) < 100:
            z = ((50 * 5) + (int(reviews) * float(rating))) / (50 + int(reviews))
            num_reviews = 50
        elif int(reviews) < 300:
            z = ((100 * 5) + (int(reviews) * float(rating))) / (100 + int(reviews))
            num_reviews = 100
        elif int(reviews) < 600:
            z = ((200 * 5) + (int(reviews) * float(rating))) / (200 + int(reviews))
            num_reviews = 200
        elif int(reviews) < 1000:
            z = ((400 * 5) + (int(reviews) * float(rating))) / (400 + int(reviews))
            num_reviews = 400
        elif int(reviews) < 2000:
            z = ((800 * 5) + (int(reviews) * float(rating))) / (800 + int(reviews))
            num_reviews = 800
        else:
            z = ((1000 * 5) + (int(reviews) * float(rating))) / (1000 + int(reviews))
            num_reviews = 1000

        price_per_review = 2
        total_price = price_per_review * num_reviews
        Your_Calendly_Link = 'https://calendar.google.com/calendar/u/0/selfsched?sstoken=UUN1X2lWeVB0M3VzfGRlZmF1bHR8ZWMwMDZjNGI0M2U1NmY0YmY3NDc3YTliNzQ1ZmI2NDc'

        # Construct the message body using the name, rating, reviews, z, and num_reviews values
        body = f"Dear Sir/Ma’am,\n\n" \
               f"I hope this Email finds you well. We noticed that {name}'s Google rating is currently {rating}/5. " \
               f"With our specialized review service, we can improve your current rating to {z:.1f}/5. " \
               f"You'll be glad to know that achieving this goal review score is absolutely reachable with just {num_reviews} reviews " \
               f"and we guarantee that each review would be submitted by a real user.\n\n" \
               f"The total cost for this service is {total_price}CA$, an unbeatable price of only 2CA$ per review.\n\n" \
               f"You’ll get 10 reviews for free just after contacting us using one of the methods below:\n\n" \
               f"1. Reply to this email.\n" \
               f"2. Schedule a meeting using the following link:{Your_Calendly_Link} \n\n" \
               f"We look forward to the opportunity of working together to augment your online presence.\n\n" \
               f"Best regards,\n" \
               f"Raise Reviews Sales Team"
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()

        # Log in and send the email
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.starttls()
        server.login('your email',"your pass")
        server.sendmail("your email",email_rec,text)
        print(f'email sent to:  {email_rec}')
        server.quit()
    except Exception as e:
        print(f"Failed to send email to {email_rec}. An error occurred: {str(e)}")
