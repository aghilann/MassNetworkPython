import yagmail
from concurrent.futures import ThreadPoolExecutor
import re
import csv
import logging

from getEmails import EmailGetter

# Setup logging
logging.basicConfig(filename='email_sender.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def clean_email(email):
    """Strips spaces and commas from an email string."""
    return email.strip().replace(",", "")

def is_valid_email(email):
    """Returns True if the email is valid, False otherwise."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# TODO: Fill in your email and app password
app_password = ""
user = ""

class EmailSender:
    def __init__(self, **args):
        self.file_name = args.get("file_name")
        self.company = args.get("company")
        self.message_body = args.get("message_body", "")
        self.debug = args.get("debug", False)
        self.tags = args.get("tags", [])
        self.get_emails = args.get("get_emails", lambda x, y: f"{x}{y}")
        self.count = 0

    def send_email_to_recipient(self, email, first_name, company, title):
        with yagmail.SMTP(user, app_password) as yag:
            try:
                if self.debug:
                    # TODO: Fill in your debug email
                    email = ""
                
                if not is_valid_email(email):
                    return f"Invalid email: {email}"
                
                # TODO: Change the subject line
                subject = f"[Ex Robinhood/Intuit]: SWE Internship at {company}"
                smtp_message = self.message_body.format(their_name=first_name, their_company=company)
                
                # TODO: Attach your resume
                contents = [smtp_message, 'my_resume.pdf']
                yag.send(email, subject, contents)
                return f'Sent email successfully to {first_name} at {company}, {email}, {title}'
            except Exception as e:
                return "Error sending email to ", email

    def __call__(self):
        executor = ThreadPoolExecutor(max_workers=4)
        futures = []
        path = f"recruiters/{self.file_name}"
        with open(path, mode='r') as file:
            csv_reader = csv.DictReader(file)

            limit = 2 if self.debug else None

            for row in csv_reader:
                try:
                    first_name = row.get("firstName", "")
                    last_name = row.get("lastName", "")
                    company = self.company
                    email = self.get_emails(first_name, last_name)
                    title = row.get("job", "").lower()
                    
                    if self.tags and not any(tag in title for tag in self.tags): 
                        continue

                    future = executor.submit(self.send_email_to_recipient, clean_email(email), first_name, company, title)
                    futures.append(future)

                    if self.debug and len(futures) >= limit:
                        break
                except Exception as e:
                    logger.error(f"Error processing row: {e}")

        for future in futures:
            logger.info(future.result())
            self.count += 1
        
        logger.info(f"Sent {self.count} emails to {self.company} recruiters.")


# TODO: Change the message body
message_body = """
Hi {their_name},

I'm FIRST LAST, I saw on LinkedIn you were a recruiter at {their_company}. I'm a rising junior at the University of Foo Bar studying XX and YY, class of 2025. I have experience interning at Robinhood and Intuit, and I'm writing this email to express my strong interest in the SWE Internship posting {their_company} recently made for Summer 2024. 

I have applied for the position through the careers page and I think I would be a good fit for the role given the alignment of my skills with the job requirements. Moreover, I have an offer deadline from Robinhood, and I would like to speed up the process if possible as I am very interested in interning at {their_company}.

Please reach out to me at any time as I'm ready to interview right now. I also attached my resume for your reference, and I'm looking forward to hearing back from you. 

Have a wonderful day! 

Sincerely,

FIRST LAST
"""
old_tags = ["univ", "campus", "eng", "tech", "software", "developer", "intern", "internship", "new grad", "graduate", "grad", "early"]
args = {
    "file_name": "googlerecruiters.csv",  
    "company": "Google",
    "message_body": message_body,
    "get_emails": EmailGetter.get_google_email,
    "debug": True,
    "tags": old_tags
}

email_sender = EmailSender(**args)
email_sender()