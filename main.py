from flask import *
import sqlite3
app = Flask(__name__)  # creating the Flask class objec
app.secret_key = "abc"
@app.route('/')  # decorator drfines the
def home():
    return  render_template('index.html')

# define route
@app.route('/test')
def test():
    return "Second function working successfully route"

# now I am focusing on url building
# check evey url and route path
@app.route('/admin')
def admin():
    return "Welcome Admin"

@app.route('/student')
def student():
    return "Welcome dear Student"



@app.route('/librarian')
def librarian():
    return "Welcome dear librarian"

# define route 3
@app.route('/user/<name>')
def test2(name):
    if  name =="admin":
        return  redirect(url_for('admin'))
    if  name =="student":
         return  redirect(url_for('student'))
    if  name =="librarian":
        return redirect(url_for('librarian'))


@app.route('/login',methods=["POST"])
def login():
    uname = request.form['uname']
    passwrd = request.form['pass']
    if uname == "Amol" and passwrd == "TheHero":
        return "Welcome %s" % uname


    # now I am revising flask template



    # flask method
# 1 Get, Post, Put , delete , head

# jinja template for tips and
# {% ... %} for statements
# {{ ... }} for expressions to print to the template output
# {# ... #} for the comments that are not included in the template output
# # ... ## for line statements


# working with jinja tempate
@app.route('/table/<int:num>')
def table(num):
    return  render_template("print-table.html",n=num)


# now we will play with cookie

@app.route('/cookie')
def cookie():
    res=make_response("<h1> Cookie is Set</h1>")
    res.set_cookie('t1','My Name is Amol Kharat')
    return res


# Working with session

@app.route("/session_var")
def set_session():
    res = make_response("<h4>session variable is set, <a href='/get'>Get Variable</a></h4>")
    session['response'] = 'session#1'
    return res


@app.route('/get')
def getVariable():
    if 'response' in session:
        s = session['response'];
        return render_template('getsession.html',name = s)



@app.route('/file_upload')
def upload_form():
    return render_template('file_upload_form.html')

@app.route('/upload_success',methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        f.save(f.filename)
        return render_template("success.html", name=f.filename)


# flash message  flash(message, category)
# syntax
# get_flashed_message(with_categories, category_filter)


@app.route('/developer/<name>')
def get_developer_name(name):
    flash("I know You are developer"+name)
    return  redirect('developer.html')

@app.route('/employee_op')
def  employee_operation():
    return  render_template('crud.html')


@app.route("/add")
def add():
    return render_template("add.html")





@app.route("/savedetails",methods = ["POST","GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            print(name,email,address)
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (name, email, address) values (?,?,?)",(name,email,address))
                con.commit()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            msg = "We can not add the employee to the list"
        finally:
            return render_template("success.html",msg = msg)
            con.close()


@app.route("/deleterecord",methods = ["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?",id)
            msg = "record successfully deleted"
        except:
            msg = "can't be deleted"
        finally:
            return render_template("delete_record.html",msg = msg)


@app.route('/view')
def view():
    print("I  am your view I am working")
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    print(rows)
    return render_template("view.html",rows = rows)
if __name__ == '__main__':
    app.run(debug=True)


