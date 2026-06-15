import smtplib

from email.message import EmailMessage


class EmailSender:

    def __init__(self):

        self.sender_email = "pridharsh2693@gmail.com"

        self.app_password = "ahvr lmla ongl iwsu"

    def send_email(
        self,
        recipient_email,
        subject,
        body,
        attachment_path
    ):

        msg = EmailMessage()

        msg["Subject"] = subject
        msg["From"] = self.sender_email
        msg["To"] = recipient_email

        msg.set_content(body)

        with open(
            attachment_path,
            "rb"
        ) as f:

            file_data = f.read()

            msg.add_attachment(
                file_data,
                maintype="application",
                subtype="pdf",
                filename="comparison_report.docx"
            )

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                self.sender_email,
                self.app_password
            )

            smtp.send_message(msg)

        return True