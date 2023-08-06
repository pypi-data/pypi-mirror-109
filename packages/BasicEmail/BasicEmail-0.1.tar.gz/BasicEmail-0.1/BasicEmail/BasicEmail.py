"""BasicEmail

This script allows the user to send emails using the smtplib library.
Some of the functuanity of the smtplib has been encapsulated in the EmailMessage class.

This file can also be imported as a module.  You can create a EmailMessage object using its static method `setup_email`
    e.g. email = EmailMessage.setup_email(email_from="sender@email.com", email_to="reciever@email.com", subject="email subject", msg="email message")

There are currently two different child classes
    `GmailMessage`
    `YahooMessage`
That have the same methods as its parent class `EmailMessage`.  The class attributes `smtp_server` and `smtp_port` are tailored to the class.

The EmailMessage.send method can raise an exception if
    `email_account_password` is incorrect.
    `smtp_server` and `smtp_port` is not recognised.
    The secruity settings on the senders email account is too strict.
"""
from __future__ import annotations
import smtplib


class EmailMessage:
    """
    A class used to send emails using the smtplib builtin python library

    Attributes
    ----------
    smtp_server : str
        Class Attribute - The name of the email server that will be used to send the email e.g. `gmail`
    smtp_port : int
        Class Attribute - The port number required to send the email
    email_from : str
        Instance Attribute - The email address the email is being sent from
    email_to : str
        Instance Attribute - The email address the email is being sent to
    subject : str
        Instance Attribute - The subject of the email that is being sent
    message : str
        Instance Attribute - The message used in the email body that is being sent

    Methods
    -------
    update_email_details(email_from: str = "", email_to: str = "", subject: str = "", msg: str = "") -> EmailMessage:
        Updates the object attrubutes.  Keyword arguments required if not using all arguments.  Arguments not used will be ignored in the method
    send(self, email_account_password: str) -> None:
        Attempts to access the senders email account using the method argument and send the email using the object attributes.
    _obj_has_smtp_values(self) -> bool:
        Private method to validate that the object has smtp_server and port values
    update_smtp_details(self, **kwargs) -> EmailMessage:
        Using a dictornary to update the smtp_server and port values.  If the correct keys are not passed it ignores the values
    keep_setup_change_server(self, email_server="default")
        Returns a new EmailMessage object using the orignal object attributes.
        The new object could be the base class or child class based on the argument in the method
    setup_email(email_from, email_to, subject, msg, email_server="default") -> EmailMessage:
        Static factory method that returns a new EmailMessage object.
        The new object could be the base class or child class based on the email_server argument in the method
    """
    smtp_server: str = None
    smtp_port: int = None

    def __init__(self, email_from: str, email_to: str, subject: str, msg: str) -> None:
        """
        Parameters
        ----------
        email_from : str
            The senders email address
        email_to : str
            The recievers email address
        subject : str
            The subject of the email
        msg : str
            The message of the email
        """
        self.email_from: str = email_from
        self.email_to: str = email_to
        self.subject: str = subject
        self.message: str = msg

    def __repr__(self):
        return f"{self.__class__.__name__}(smtp_server={self.smtp_server}, " \
               f"smtp_port={self.smtp_port}, email_from={self.email_from}, " \
               f"email_to={self.email_to}, subject={self.subject}, " \
               f"message={self.message})"

    def update_email_details(self,
                             email_from: str = "",
                             email_to: str = "",
                             subject: str = "",
                             msg: str = "") -> EmailMessage:
        """
        Updates the instance attrubutes of the object.

        If an argument is not passed the default value of empty string is passed.  The empty string gets ignored.
        Pass the arguments with the name of the parameters for readability.

        Parameters
        ----------
        email_from : str
            The senders email address
        email_to : str
            The recievers email address
        subject : str
            The subject of the email
        msg : str
            The message of the email
        Returns
        -------
        EmailMessage object for method chaining
        """
        if email_from:
            self.email_from = email_from
        if email_to:
            self.email_to = email_to
        if subject:
            self.subject = subject
        if msg:
            self.message = msg
        return self

    def send(self, email_account_password: str) -> None:
        """
        Sends an email using all of the object attributes.  Email_account_password is required to use the senders email account.

        The method can fail and raise an exception from the smtplib library if
            `email_account_password` is incorrect.
            `smtp_server` and `smtp_port` is not recognised.
            The secruity settings on the senders email account is too strict.

        Parameters
        ----------
        email_account_password : str
            The senders email account password
        Raises
        ------
        ValueError
            If the object attributes `smtp_server` or `smtp_port` are None
        """
        if not self._obj_has_smtp_values:
            raise ValueError(f"self.smtp_server require a valid smtp str value "
                             f"and self.smtp_port require a valid smtp int value.  "
                             f"Currently assigned as "
                             f"self.smtp_server={self.smtp_server} self.smtp_port={self.smtp_port}")
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as connection:
            connection.starttls()
            connection.login(user=self.email_from, password=email_account_password)
            connection.sendmail(from_addr=self.email_from,
                                to_addrs=self.email_to,
                                msg=f"Subject:{self.subject}\n\n{self.message}"
                                )

    def _obj_has_smtp_values(self) -> bool:
        """
        Validation check on `smtp_server` and `smtp_port values`

        return
        ------
        Returns True if `smtp_server` and `smtp_port values` are both truthy.  Returns False if they are not truthy.
        """
        if self.smtp_server and self.smtp_port:
            return True
        return False

    def update_smtp_details(self, **kwargs) -> EmailMessage:
        """
        Updates the class attributes for `smtp_server` and `smtp_port`

        Parameters
        ----------
        kwargs
            Pass a dictornary with one or both keys `smtp_server` and `smtp_port`

        Returns
        -------
        EmailMessage object for method chaining
        """
        smtp_server_data = kwargs.get("smtp_server", "")
        smtp_port_data = kwargs.get("smtp_port", 0)
        if smtp_server_data:
            self.smtp_server = smtp_server_data
        if smtp_port_data:
            self.smtp_port = smtp_port_data
        return self

    def keep_setup_change_server(self, email_server: str = "default") -> EmailMessage:
        """
        Creates a new Base or child EmailMessage object using the same object attributes.
        The class attributes `smtp_server` and `smpt_port` will change based on the object returned
        from the method parameters e.g. "gmail" -> `smtp_server` = `smtp.gmail.com`

        Parameters
        ----------
        email_server : str
            A new base class of EmailMessage will be created if
                The method can not find the parameter in the module dictornary.
                The parameter uses the default value

        Returns
        -------
        EmailMessage
        """
        return self.setup_email(self.email_from,
                                self.email_to,
                                self.subject,
                                self.message,
                                email_server
                                )

    @staticmethod
    def setup_email(email_from: str, email_to: str, subject: str, msg: str, email_server: str ="default") -> EmailMessage:
        """
        Static facotry method that creates a new base or child EmailMessage.

        Parameters
        ----------
        email_from : str
            The senders email address
        email_to : str
            The recievers email address
        subject : str
            The subject of the email
        msg : str
            The message of the email
        email_server : str
            The senders email account server e.g. gmail
        Returns
        -------
        EmailMessage
        """
        email_class = email_class_dict.get(email_server, EmailMessage)
        return email_class(email_from, email_to, subject, msg)


class GmailMessage(EmailMessage):
    """
    Child class from EmailMessage.  The class attribute values are different to work with Gmail server

    Type in help(EmailMessage) to see all class attributes and methods
    """
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    def __init__(self, email_from: str, email_to: str, subject: str, msg: str) -> None:
        super().__init__(email_from, email_to, subject, msg)


class YahooMessage(EmailMessage):
    """
    Child class from EmailMessage.  The class attribute values are different to work with Yahoo server

    Type in help(EmailMessage) to see all class attributes and methods
    """
    smtp_server = 'smtp.mail.yahoo.com'
    smtp_port = 587

    def __init__(self, email_from: str, email_to: str, subject: str, msg: str):
        super().__init__(email_from, email_to, subject, msg)


email_class_dict = {"default": EmailMessage, "gmail": GmailMessage, "yahoo": YahooMessage}


