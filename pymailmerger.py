#!/usr/bin/python

from email.mime.text import MIMEText
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
import smtplib
import yaml

class Person(object):
	pass

class PersonDB:
	def __init__(self):
		# Use example-data.db
		person_db = create_engine("sqlite:///example-data.db")
	
		metadata = MetaData()
		persons_table = Table("persons", metadata,
			Column("id", Integer, primary_key=True),
			Column("first_name", String),
			Column("last_name", String),
			Column("address", String),
			Column("city", String),
			Column("state", String),
			Column("zip", String),
			Column("email", String),
			Column("email_text", String),
			Column("email_sent", Integer))
		
		mapper(Person, persons_table)
	
		Session = sessionmaker(bind=person_db)
		self.session = Session()
		
class EmailProcessor:
	def __init__(self, person, template_filename, config):
		self.person = person				
		self.email_msg = template_filename
		self.email_config = config["email config"]
		self.search_config = config["search terms"]
		
	def get_value_by_db_name(self, db_field):
		table, column = db_field.split(".")
		return getattr(getattr(self, table), column)
	
	def replace_template(self):
		for template_value, db_field in self.search_config.iteritems():
			new_value = self.get_value_by_db_name(db_field)
			self.email_msg = self.email_msg.replace("%%%%%s%%%%" % template_value, new_value)
		
	def send_email(self):
		# Create a text/plain message
		msg = MIMEText(self.email_msg)
		
		me = "%s <%s>" % (self.email_config["from-name"], self.email_config["from-email"])
		you = self.person.email
		
		msg['Subject'] = self.email_config["subject"]
		msg['From'] = me 
		msg['To'] = you
		
		if self.email_config["use tls"] == True:
			s = smtplib_.SMTP_SSL()
		else:	
			s = smtplib.SMTP()
		if self.email_config["use debug"] == True:
			s.set_debuglevel(True)
		
		s.connect(self.email_config["server"])
		s.login(self.email_config["from-email"], self.email_config["password"])
		s.sendmail(me, [you], msg.as_string())
		s.quit()

if __name__ == "__main__":
	# The config and email template filenames go here
	config_filename = "config.yaml"
	email_template_filename = "email_template_example.txt"
	
	email_template = open(email_template_filename, "r").read()
	config = yaml.load(open(config_filename, 'r').read())
	
	person_db = PersonDB()
	for person in person_db.session.query(Person).filter(Person.email_sent == 0).order_by(Person.id):
		email_processor = EmailProcessor(person, email_template, config)
		email_processor.replace_template()
		email_processor.send_email()
		person.email_sent = 1
		person_db.session.commit()
		print email_processor.email_msg
		print "==================================="
		print "\n"
		print "\n"
