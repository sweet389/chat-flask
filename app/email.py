import os
import requests
import logging
def send_baltrota_message(log):
  	return requests.post(
  		"https://api.mailgun.net/v3/sandboxf5c296b3cc614dc78660f8d10c15434e.mailgun.org/messages",
  		auth=("api", os.getenv('API_KEY', 'API_KEY')),
  		data={"from": "Mailgun <postmaster@sandboxf5c296b3cc614dc78660f8d10c15434e.mailgun.org>",
			"to": "Pedro Octavio Kunz Morello <pedroadf2010@gmail.com>",
            "subject": "Baltrota!",
  			"text": f"Baltrota Log: {log}"})
         
def send_simple(text, subject):
    return requests.post(
  		"https://api.mailgun.net/v3/sandboxf5c296b3cc614dc78660f8d10c15434e.mailgun.org/messages",
  		auth=("api", os.getenv('API_KEY', 'API_KEY')),
  		data={"from": "Mailgun <postmaster@sandboxf5c296b3cc614dc78660f8d10c15434e.mailgun.org>",
			"to": "Pedro Octavio Kunz Morello <pedroadf2010@gmail.com>",
            "subject": f"{subject}",
  			"text": f"{text}"})
    
class KeywordEmailHandler(logging.Handler):
    def __init__(self, keyword: str):
        super().__init__()
        self.keyword = keyword.upper()
    def emit(self, record):
        log_entry = self.format(record)
        if self.keyword in log_entry.upper():
            if self.keyword == "Baltrota":
                logging.info("EMAIL SENT")
                send_baltrota_message(log_entry)
            else:
                logging.info("EMAIL SENT")
                send_simple(subject=self.keyword, text=log_entry)

         
         