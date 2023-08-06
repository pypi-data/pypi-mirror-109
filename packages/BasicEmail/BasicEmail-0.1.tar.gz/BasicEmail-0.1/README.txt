BasicEmail

Wrapping the Main methods to send an email, in a class, from the python package smtplib to send a simple email.

The module allows the user to send emails using the smtplib library. Some of the functuanity of the smtplib has been encapsulated in the EmailMessage class.

You can create a EmailMessage object using its static method setup_email e.g. email = EmailMessage.setup_email(email_from="sender@email.com", email_to="reciever@email.com", subject="email subject", msg="email message")

There are currently two different child classes GmailMessage YahooMessage That have the same methods as its parent class EmailMessage. The class attributes smtp_server and smtp_port are tailored to the class.

The EmailMessage.send method can raise an exception if email_account_password is incorrect. smtp_server and smtp_port is not recognised. The secruity settings on the senders email account is too strict

I have written this module to learn the following:

Add documentation to a python file, test the module using pytest and add my first project to pypi.

Thank you for taking the time to look at my work.

John Piper