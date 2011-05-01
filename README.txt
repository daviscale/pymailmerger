################################################################################
                             pymailmerger.py
################################################################################

pymailmerger.py is a simple mail merger. The script reads in an email template,
replaces the template values with values from a database, and then sends out
emails. 

This script is not an "out-of-the-box" solution. It should be thought of as a
template for your own mail merge solution. I have it set up to send
fictitious emails to fake individuals in a SQLite database. In this README,
I'll briefly describe the files in this project and how to alter my script
for your own purposes.

email_template_example.txt
################################################################################
Contains the email template. Any words that you want replaced by pymailmerger.py
should be surrounded by "%%".

config.yaml
################################################################################
This YAML file contains configuration information for your email address (i.e.
username, password, server). It also contains a mapping of keywords in the
template to fields in the database.

example-data.db
################################################################################
This is my SQLite database of fake people. pymailmerger.py uses the SQLAlchemy
library so the script can be easily edited to support other databases such as
Postresql or MySQL.

Requirements to run pymailmerger.py
################################################################################
SQLAlchemy  - http://www.sqlalchemy.org/
PyYaml - http://pyyaml.org

Adapting pymailmerge.py for your own purposes
################################################################################
The main items that need to change in pymailmerger.py are your database class
and the object(s) that are mapped by your DB class. In pymailmerger.py, I have
a PersonDB class and a Person class:

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

Edit your DB class so that it contains all the table(s) and columns that you
want to use from your database. You can change that name of the Person class to
a name that's more meaningful to your mail merge project.

In the main section of the script, you can change the name of the config
and email template file names:

        # The config and email template filenames go here
        config_filename = "config.yaml"
        email_template_filename = "email_template_example.txt"

That's it.
