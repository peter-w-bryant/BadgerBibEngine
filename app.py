
from flask import Flask,render_template, flash, redirect, url_for, request, session, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, PasswordField, validators, SelectField
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os
import config

# session is a dictionary that stores data across requests.
# logging is a simple logger that logs to a file.


# Flask Object
app = Flask(__name__)
app.secret_key = config.secret_key
app.debug = True

#Config MySQL: HEROKU
app.config['MYSQL_HOST'] = config.host
app.config['MYSQL_USER'] = config.user
app.config['MYSQL_PASSWORD'] = config.password
app.config['MYSQL_DB'] = config.database
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'


#Create MYSQL Instance
mysql = MySQL(app)

# Login PAGE
@app.route('/', methods=['GET','POST'])
def login():
    form = LoginForm(request.form)
    session['logged_in'] = False
    if request.method == 'POST': # If the form is submitted.
        username = form.username.data # Get the username from the form.
        password = form.password.data # Get the password from the form.
    
        # Create cursor
        cur = mysql.connection.cursor()

        # Search for the user in the database.
        result = cur.execute("SELECT * FROM users WHERE username = %s and password = %s", (username, password))

        # If the user is found in the database.
        if result > 0:
            session['logged_in'] = True # Set the session to True.
            session['user'] = username # Set the user in the session.
            return redirect(url_for('home'))
        else:
            flash('<Error: Invalid username or password, please try again or continue as guest!')
            return render_template('login.html', form=form)

    return render_template('login.html')

# Logout PAGE
@app.route('/logout', methods=['GET','POST'])
def logout():
    session.clear() # Clear the session.
    return redirect(url_for('login'))

# Registration PAGE
@app.route('/register', methods=['GET','POST'])
def Register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        new_username = form.new_username.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data

        # Create cursor
        cur = mysql.connection.cursor()
        print("FLAG")
        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", (new_username,))
        print("FLAG2")
        if result > 0:
            flash('<Username already taken, please try again!')
            return render_template('register.html', form=form)
        elif new_password != confirm_password:
            print("FLAG3")
            flash('<Error: Passwords do not match, please try again!')
            return render_template('register.html', form=form)
        else:
            cur.execute("INSERT INTO users(username, password) VALUES(%s, %s)", (new_username, new_password))
            mysql.connection.commit()
            flash('<Registration successful, please login!')
            return redirect(url_for('login'))
    
    return render_template('register.html')

# HOME PAGE
@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')

# My Account PAGE
@app.route('/my-account', methods=['GET','POST'])
def account():
    return render_template('my-account.html')

# Documentation PAGE
@app.route('/documentation')
def doc():
    return render_template('documentation.html')

# Form for Login
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [validators.Length(min=4, max=50)])

# Form for Login
class RegisterForm(Form):
    new_username = StringField('Username', [validators.Length(min=4, max=50)])
    new_password = PasswordField('Password', [validators.Length(min=4, max=50)])
    confirm_password = PasswordField('Password', [validators.Length(min=4, max=50)])

# Form for Search
class SearchForm(Form):
    select_options = ['<Select Option>','Article','Author','Journal']
    select_field = SelectField('What would you like to search by?', choices=select_options)
    name_exact = StringField('By Article Title',[validators.Length(min=0,max=50)])
    uid = StringField('By UID',[validators.Length(min=0,max=50)])
    journal = StringField('Find a Journal Name',[validators.Length(min=0,max=50)])
    authors_exact = StringField('By Author Name',[validators.Length(min=0,max=50)])
    author_id = StringField('By Author ID',[validators.Length(min=0,max=50)])
    code_venue = StringField('By Code Venue',[validators.Length(min=0,max=50)])

    # Form for Search
class EditForm(Form):
    select_op_options = ['<Select Option>','Insert','Delete']
    select_options = ['<Select Option>','Article','Author','Journal']
    select_op = SelectField('Would you like to insert or delete?', choices=select_op_options)
    select_field = SelectField('What would you like to edit?', choices=select_options)

    # Article
    UID = StringField('Article UID',[validators.Length(min=0,max=50)])
    title = StringField('Article Title',[validators.Length(min=0,max=50)])
    DOI = StringField('Article DOI',[validators.Length(min=0,max=50)])
    code_venue = StringField('Article Code Venue',[validators.Length(min=0,max=50)])
    issue = StringField('Article Issue',[validators.Length(min=0,max=50)])
    volume = StringField('Article Volume',[validators.Length(min=0,max=50)])
    num_addresses = StringField('Number of Addresses',[validators.Length(min=0,max=50)])
    num_references = StringField('Number of References',[validators.Length(min=0,max=50)])
    num_authors= StringField('Number of Authors',[validators.Length(min=0,max=50)])
    pub_year = StringField('Publication Year',[validators.Length(min=0,max=50)])
    num_pages = StringField('Number of Pages',[validators.Length(min=0,max=50)])
    # Authors of the article being inserted, max of 3 authors: format-> "AuthorID, FirstName, LastName, Suffix"
    author_1 = StringField('Author 1',[validators.Length(min=0,max=100)])
    author_2 = StringField('Author 2',[validators.Length(min=0,max=100)])
    author_3 = StringField('Author 3',[validators.Length(min=0,max=100)])

    # Author
    author_id = StringField('Author ID',[validators.Length(min=0,max=50)])
    first_name = StringField('Author First Name',[validators.Length(min=0,max=50)])
    last_name = StringField('Author Last Name',[validators.Length(min=0,max=50)])
    suffix = StringField('Author Suffix',[validators.Length(min=0,max=50)])
    full_name = StringField('Author Full Name',[validators.Length(min=0,max=50)])

    # Journal
    journal_name = StringField('Journal Name',[validators.Length(min=0,max=50)])
    code_venue = StringField('Code Venue',[validators.Length(min=0,max=50)])
    discipline = StringField('Discipline',[validators.Length(min=0,max=50)])
    specialty = StringField('Specialty',[validators.Length(min=0,max=50)])    


class MoreForm(Form):
    select_options = ['<Select Option>','1','2', '3']
    select_field = SelectField('What operation would you like to perform?', choices=select_options)
    num_publications = StringField('Minimum Number of Publications',[validators.Length(min=0,max=50)]) 
    title_string = StringField('By Title',[validators.Length(min=0,max=50)])
    journal_name = StringField('By Journal Name',[validators.Length(min=0,max=50)])


# SEARCH PAGE
@app.route('/search', methods=['GET','POST'])
def search():
    form = SearchForm(request.form)
    if request.method == 'POST' and form.validate():
        # Init variable from user input in WTF form
        select_field = form.select_field.data
        uid = form.uid.data
        name_exact = form.name_exact.data
        journal = form.journal.data
        authors_exact = form.authors_exact.data
        author_id = form.author_id.data
        code_venue = form.code_venue.data

         # Create a MySQL connection and cursor
        cur = mysql.connection.cursor()    

        # Search Flag is 1 if user selects Article, 2 if Author, or 3 if Journal
        search_flag =-1
        # Flag is 1-6 corresponding to the search options
        flag = -1

        # Set search flag based on Search By option
        if select_field == "Article":
            search_flag = 1
        elif select_field == "Author":
            search_flag = 2
        elif select_field == "Journal":
            search_flag = 3
        else:
            search_flag = -1

        # If the search flag is unset, continue to render the search page
        if search_flag == -1:
            return render_template('search.html',form=form)

        # If the search flag is set, but the fields are empty, continue to render the search page
        if (search_flag == 1 and uid == "" and name_exact == ""):
            return render_template('search.html',form=form)

        # Begin Searching
        if search_flag == 1 and uid != None and name_exact != None:
            # BY ARTICLE UID
            if uid != '':
                cur.execute("SELECT Distinct a.UID, a.Title, GROUP_CONCAT(c.Full_Name SEPARATOR ' ') as Authors, a.DOI, a.Nb_Page, a.issue, a.Volume, a.PubYear FROM Article a, Authored_by b, Author c WHERE a.UID = %s and a.UID = b.UID and b.author_id = c.author_id;", (uid,))
                fetchdata = cur.fetchall()
                flag = 1
                cur.close()
                return render_template('search.html', form = form, data = fetchdata, flag = flag, search_flag = search_flag)
            # BY ARTICLE NAME
            if name_exact != '':
                cur.execute("SELECT a.UID as UID, a.Title as Title, a.DOI as DOI, a.issue as Issue, a.Volume as Volume, a.PubYear as YearPublished, GROUP_CONCAT(au.Full_Name SEPARATOR ' ') as Authors, a.Nb_Page as NumberofPages, a.issue as Issue FROM Article a JOIN authored_by ab ON a.UID = ab.UID JOIN author au ON au.author_Id = ab.author_Id WHERE a.title LIKE '%" + name_exact + "%' GROUP BY a.title")
                fetchdata = cur.fetchall()
                flag=5
                cur.close()
                return render_template('search.html', form = form, data = fetchdata, flag = flag, search_flag = search_flag)
        if search_flag == 2 and author_id != None and authors_exact != None:
            if author_id != '':
                cur.execute("SELECT b.author_id, b.Full_Name, COUNT(a.UID) as count, CAST(SUM(a.Nb_Reference) as SIGNED) as sum FROM article a, author b, authored_by c WHERE b.author_id = "+ author_id +" AND b.author_id = c.author_id AND c.UID = a.UID;")
                fetchdata = cur.fetchall()
                cur.execute("SELECT a.Title FROM article a, author b, authored_by c WHERE b.author_id =" + author_id + " AND b.author_id = c.author_id AND c.UID = a.UID")
                fetchdata2 = cur.fetchall()
                flag = 2
                cur.close()
                return render_template('search.html', form = form, data = fetchdata, data2 = fetchdata2, flag = flag, search_flag = search_flag)
            if authors_exact != '':
                cur.execute("SELECT b.author_id, b.Full_Name, COUNT(a.UID) as count, CAST(SUM(a.Nb_Reference) as SIGNED) as sum FROM article a, author b, authored_by c WHERE b.Full_Name LIKE'%" + authors_exact +"%' AND b.author_id = c.author_id AND c.UID = a.UID Group by b.Full_Name;")
                fetchdata = cur.fetchall()
                cur.execute("SELECT a.Title, b.Full_Name, b.author_id FROM article a, author b, authored_by c WHERE b.Full_Name LIKE '%" + authors_exact + "%' AND b.author_id = c.author_id AND c.UID = a.UID")
                fetchdata2 = cur.fetchall()
                flag =4
                cur.close()
                return render_template('search.html', form = form, data = fetchdata, data2 = fetchdata2, flag = flag, ssearch_flag = search_flag)
        if search_flag == 3 and journal != None and code_venue != None:
            if journal != '':
                cur.execute("SELECT DISTINCT j.Code_Venue, j.abbrev, j.journal_name, j.discipline, j.specialty FROM journal j WHERE j.journal_name LIKE '%" + journal +"%';")
                fetchdata = cur.fetchall()
                flag = 3
                cur.close()
                return render_template('search.html', form = form, data = fetchdata, flag = flag, search_flag = search_flag)
            if code_venue != '':
                cur.execute("SELECT DISTINCT j.Code_Venue, j.abbrev, j.journal_name, j.discipline, j.specialty FROM journal j WHERE j.Code_Venue = '" + code_venue + "'")
                fetchdata = cur.fetchall()
                flag = 6
                cur.close()
                return render_template('search.html', form = form, data = fetchdata, flag = flag, search_flag = search_flag)
            
    return render_template('search.html',form=form)


@app.route('/edit', methods=['GET','POST'])
def edit():
    if session['logged_in']:
        form = EditForm(request.form)
        if request.method == 'POST' and form.validate():
            select_field = form.select_field.data
            select_op = form.select_op.data
            
            con = mysql.connection
            cur = con.cursor()

            flag = -1

            # Article
            UID = form.UID.data                 # Primary Key
            title = form.title.data
            DOI = form.DOI.data
            code_venue = form.code_venue.data
            issue = form.issue.data
            volume = form.volume.data
            num_addresses = form.num_addresses.data
            num_references = form.num_references.data
            num_pages = form.num_pages.data
            num_authors = form.num_authors.data
            pub_year = form.pub_year.data
            author_1 = form.author_1.data
            author_2 = form.author_2.data
            author_3 = form.author_3.data

            # Author
            author_id = form.author_id.data     # Primary Key
            first_name = form.first_name.data
            last_name = form.last_name.data
            suffix = form.suffix.data

            # Journal
            code_venue = form.code_venue.data   # Primary Key
            journal_name = form.journal_name.data
            discipline = form.discipline.data
            specialty = form.specialty.data

            # Start INSERT
            if select_op == "Insert":

                if select_field == "Article" and UID != None and title != None and DOI != None and issue != None and volume != None and num_addresses != None and num_references != None and num_pages != None and num_authors != None and pub_year != None and author_1 != None and UID != 0 and title != 0 and DOI != 0 and issue != 0 and volume != 0 and num_addresses != 0 and num_references != 0 and num_pages != 0 and num_authors != 0 and pub_year != 0 and author_1 != 0:
                    flag = 1
                    author_flag = [0,0,0]                           # Create empty author flag array of size 3
                    author_1_array = author_1.split(",")            # Delimit author_1 by space and store in array name author_1_array
                    author_2_array = author_2.split(",")            # Delimit author_2 by space and store in array name author_2_array
                    author_3_array = author_3.split(",")            # Delimit author_3 by space and store in array name author_3_array

                    # datetime object containing current date and time
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S on %m/%d/%Y ")

                    # Author 1 must not be empty, so we can gurantee that the author exists
                    author_flag[0] = 1

                    # INSERT INTO Article
                    cur.execute("INSERT INTO Article (UID, title, DOI, Code_Venue, issue, volume, Nb_Address, Nb_Reference, Nb_Page, PubYear, Nb_Author) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (UID, title, DOI, code_venue, issue, volume, num_addresses, num_references, num_pages, pub_year, num_authors))
                    # Insert into AUTHORED_BY 
                    cur.execute("INSERT INTO authored_by (UID, author_Id) VALUES (%s, %s)", (UID, author_1_array[0]))
                    # Insert into AUTHOR
                    cur.execute("INSERT INTO author (author_Id, First_Name, Last_Name, Suffix) VALUES (%s, %s, %s, %s)", (author_1_array[0], author_1_array[1], author_1_array[2], author_1_array[3]))
                    
                    # Author 2 can be empty
                    if(author_2 != ""):
                        author_flag[1] = 1
                        # Insert into AUTHORED_BY
                        cur.execute("INSERT INTO authored_by (UID, author_Id) VALUES (%s, %s)", (UID, author_2_array[0]))
                        # Insert into AUTHOR
                        cur.execute("INSERT INTO author (author_Id, First_Name, Last_Name, Suffix) VALUES (%s, %s, %s, %s)", (author_2_array[0], author_2_array[1], author_2_array[2], author_2_array[3]))
                    
                    # Author 3 can be empty
                    if(author_3 != ""):
                        author_flag[2] = 1
                        # Insert into authored_by
                        cur.execute("INSERT INTO authored_by (UID, author_Id) VALUES (%s, %s)", (UID, author_3_array[0]))
                        # Insert into author
                        cur.execute("INSERT INTO author (author_Id, First_Name, Last_Name, Suffix) VALUES (%s, %s, %s, %s)", (author_3_array[0], author_3_array[1], author_3_array[2], author_3_array[3]))
                    
                    con.commit()
                    fetchdata = 1
                    
                    if author_flag[0] == 1 and author_flag[1] == 1 and author_flag[2] == 1:
                        return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string, author1 = author_1_array, author2 = author_2_array, author3 = author_3_array)

                    elif author_flag[0] == 1 and author_flag[1] == 1:
                        return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string, author1 = author_1_array, author2 = author_2_array)

                    else:
                        return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string, author1 = author_1_array)

                elif select_field == "Author" and author_id != None and first_name != None and last_name != None and suffix != None and author_id != "" and first_name != "" and last_name != "" and suffix != "":
                    flag = 2
                    print("Test")
                    # datetime object containing current date and time
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S on %m/%d/%Y ")
                    cur.execute("INSERT INTO Author (author_id, first_name, last_name, suffix) VALUES (%s, %s, %s, %s)", (author_id, first_name, last_name, suffix))
                    con.commit()
                    fetchdata = 1
                    return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string)

                elif select_field == "Journal" and code_venue != None and journal_name != None and discipline != None and specialty != None and code_venue != "" and journal_name != "" and discipline != "" and specialty != "":
                    flag = 3
                    # datetime object containing current date and time
                    now = datetime.now()
                    dt_string = now.strftime("%H:%M:%S on %m/%d/%Y ")
                    cur.execute("INSERT INTO journal (code_Venue, journal_name, discipline, specialty) VALUES (%s, %s, %s, %s)", (code_venue, journal_name, discipline, specialty))
                    con.commit()
                    fetchdata = 1
                    return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string)

            # Start DELETE
            elif select_op == "Delete":
                if select_field == "Article" and UID != None and UID != "":
                    flag = 1
                    now = datetime.now()   # datetime object containing current date and time
                    dt_string = now.strftime("%H:%M:%S on %m/%d/%Y ")
                    cur.execute("Select * FROM Article WHERE UID = %s", (UID,))
                    fetchdata = cur.fetchall()
                    cur.execute("DELETE FROM Article WHERE UID = %s", (UID,))
                    cur.execute("DELETE FROM authored_by WHERE UID = %s", (UID,))
                    con.commit()
                    return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string)

                elif select_field == "Author" and author_id != None and author_id != "":
                    flag = 2 
                    now = datetime.now()    # datetime object containing current date and time
                    dt_string = now.strftime("%H:%M:%S on %m/%d/%Y ")
                    cur.execute("Select * FROM Author WHERE author_id = %s", (author_id,))
                    fetchdata = cur.fetchall()
                    cur.execute("DELETE FROM Author WHERE author_id = %s", (author_id,))
                    cur.execute("DELETE FROM authored_by WHERE author_id = %s", (author_id,))
                    con.commit()
                    return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string)

                elif select_field == "Journal":
                    flag = 3
                    now = datetime.now()    # datetime object containing current date and time
                    dt_string = now.strftime("%H:%M:%S on %m/%d/%Y ")
                    cur.execute("Select * FROM Journal WHERE code_venue = %s", (code_venue,))
                    fetchdata = cur.fetchall()
                    cur.execute("DELETE FROM journal WHERE code_Venue = %s", (code_venue,))
                    con.commit()
                    return render_template('edit.html', form = form, data = fetchdata, flag = flag, time = dt_string)
        return render_template('edit.html', form = form)
    else:
        flash('<Error: You need to log in to edit the database!')
        return render_template('home.html')

# WEAK
# More PAGE
@app.route('/more', methods=['GET','POST'])
def more():
    form = MoreForm(request.form)
    if request.method == 'POST' and form.validate():
        select_field = form.select_field.data
        num_publications = form.num_publications.data
        title_string = form.title_string.data
        journal_name = form.journal_name.data

        # Create cursor
        cur = mysql.connection.cursor()

        # If the search flag is unset, continue to render the search page
        if select_field == "":
            return render_template('more.html',form=form)

        # If the search field is most productive authors
        elif select_field == "1":
            if num_publications == "" or num_publications == None:
                return render_template('more.html',form=form)
            # Create cursor
            if num_publications != None or num_publications != "":
                cur = mysql.connection.cursor()
                cur.execute("SELECT DISTINCT b.Full_Name, a.Author_ID FROM (SELECT b.author_id, COUNT(DISTINCT a.UID) times FROM article a INNER JOIN authored_by b ON a.UID = b.UID GROUP BY b.author_id HAVING COUNT(DISTINCT a.UID) >"+num_publications+") a LEFT JOIN author b ON a.author_id = b.author_id;")
                fetchdata = cur.fetchall()
                return render_template('more.html',form=form, data = fetchdata, option = select_field, user_data = num_publications)
        elif select_field == "2":
            if title_string == "" or title_string == None:
                return render_template('more.html',form=form)
            if title_string != None or title_string != "":
                cur = mysql.connection.cursor()
                cur.execute("SELECT DISTINCT b.Code_Venue, b.journal_name, b.specialty, b.discipline FROM article a, journal b WHERE a.Title LIKE '%" + title_string + "%' AND a.Code_Venue = b.Code_Venue ORDER BY b.journal_name;")
                fetchdata = cur.fetchall()
                return render_template('more.html',form=form, data = fetchdata, option = select_field, user_data = title_string)
        elif select_field == "3":
            if journal_name == "" or journal_name == None:
                return render_template('more.html',form=form)
            if journal_name != None or journal_name != "":
                cur = mysql.connection.cursor()
                cur.execute("CREATE TEMPORARY TABLE t1 (SELECT DISTINCT c.author_id, COUNT(DISTINCT a.UID) c FROM article a, journal b, authored_by c WHERE b.journal_name = %s AND b.Code_Venue = a.Code_Venue AND a.UID = c.UID GROUP BY c.author_id);", (journal_name,)); 
                cur.execute("CREATE TEMPORARY TABLE t2 (SELECT MAX(t1.c) m FROM t1);")
                cur.execute("SELECT a.First_Name, a.Last_Name FROM t1, t2, author a WHERE t1.c = t2.m AND t1.author_id = a.author_id;")
                fetchdata = cur.fetchall()
                return render_template('more.html',form=form, data = fetchdata, option = select_field, user_data = journal_name)

    return render_template('more.html', form = form) 


if __name__ =='__main__':
    app.secret_key='secret123'
    app.run()
