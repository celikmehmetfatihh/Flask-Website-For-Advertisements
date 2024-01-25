from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L1F4Q8z\xec]/'

@app.route("/")
@app.route("/home")
def index():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT cname FROM CATEGORY")
    category_list = c.fetchall()
    conn.close()

    return render_template("home.html", category_list = category_list)

@app.route("/register")
def registration():
    return render_template("registration.html")

@app.post("/applyregister")
def applyRegister():
    username = request.form.get("username")
    pwd = request.form.get("pwd")
    fullname = request.form.get("fullname")
    email = request.form.get("email")
    telno = request.form.get("telno")

    error = validate(username, pwd, fullname, email, telno)

    if error:
        return render_template("registration.html", error = error)
    else:
        return render_template("registerConfirmation.html")

def validate(username, pwd, fullname, email, telno):
    if upperCaseChecker(pwd) == 0:
        return "Password must include at least one upper case letter."
    if lowerCaseChecker(pwd) == 0:
        return "Password must include at least one lower case letter."
    if digitChecker(pwd) == 0:
        return "Password must include at least one digit."
    if specialSymbolChecker(pwd) == 0:
        return "Password must include at least [+, !, *, -] one of these symbols."
    if len(pwd) < 10:
        return "Password is too short! Password's length must be at least 10 characters."

    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()
    c.execute("SELECT username FROM User WHERE username = ?", (username,))

    if(c.fetchone() != None):
        conn.close()
        return "This username is taken!"
    else:
        c.execute("INSERT INTO User VALUES (?,?,?,?,?)", (username, pwd, fullname, email, telno))
        conn.commit()
        conn.close()

    return None

def specialSymbolChecker(pwd):
    specialSymbolCounter = 0
    for char in pwd:
        if (char == "+") or (char == "!") or (char == "*") or (char == "-"):
            specialSymbolCounter += 1
        if specialSymbolCounter == 1:
            return specialSymbolCounter
    return 0


def upperCaseChecker(pwd):
    upperCaseCounter = 0
    for char in pwd:
        if char.isupper():
            upperCaseCounter += 1
        if upperCaseCounter == 1:
            return upperCaseCounter
    return 0

def lowerCaseChecker(pwd):
    lowerCaseCounter = 0
    for char in pwd:
        if char.islower():
            lowerCaseCounter += 1
        if lowerCaseCounter == 1:
            return lowerCaseCounter
    return 0

def digitChecker(pwd):
    digitCounter = 0
    for char in pwd:
        if char.isdigit():
            digitCounter += 1
        if digitCounter == 1:
            return digitCounter
    return 0

@app.route("/applylogin", methods=["GET", "POST"])
def applylogin():
    if request.method == "POST":
        username = request.form.get("username")
        pwd = request.form.get("pwd")

        conn = sqlite3.connect("mydb.db")
        c = conn.cursor()

        c.execute("SELECT * FROM USER WHERE username = ? AND password = ?", (username, pwd))
        if (c.fetchone() == None):
            return render_template("home.html", error = "Invalid username or password!")
            return render_template("home.html", error = "Invalid username or password!")

        session["username"] = username
        return  render_template("home.html", showMenu=True)
    else:
        return  render_template("home.html", showMenu=True)


@app.route("/logout")
def logoutoperation():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.get("/myadvertisements")
def myadvertisements():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT cname FROM CATEGORY")
    category_list = c.fetchall()

    c.execute("SELECT a.aid, a.title,a.description,c.cname,a.isactive FROM ADVERTISEMENT a, CATEGORY c WHERE a.cid = c.cid AND a.username = ?", (session["username"],))
    advertisement_list = c.fetchall()

    conn.close()

    return render_template("myadvertisements.html", category_list = category_list, advertisement_list = advertisement_list)

@app.post("/addAdvertisement")
def addAdvertisement():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    title = request.form.get("title")
    desc = request.form.get("desc")
    selected_category = request.form.get("category")

    c.execute("SELECT cid FROM CATEGORY WHERE cname = ? ", (selected_category,))
    cid = c.fetchone()

    c.execute("INSERT INTO ADVERTISEMENT (title, description, isactive, username, cid) VALUES (?, ?, ?, ?, ?)",(title, desc, 1, session["username"], cid[0]))
    conn.commit()
    conn.close()

    return redirect(url_for("myadvertisements"))

@app.get("/deactivate")
def deactivate():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    aid = request.args.get("aid")
    print(aid)

    c.execute("UPDATE ADVERTISEMENT SET isactive = 0 WHERE aid = ?", (aid,))
    conn.commit()
    conn.close()

    return redirect(url_for("myadvertisements"))

@app.get("/activate")
def activate():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    aid = request.args.get("aid")

    c.execute("UPDATE ADVERTISEMENT SET isactive = 1 WHERE aid = ?", (aid,))
    conn.commit()
    conn.close()

    return redirect(url_for("myadvertisements"))

@app.route("/myprofile")
def myprofile():
    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT * FROM USER WHERE username = ?", (session["username"],))
    user_details = c.fetchone()

    conn.close()

    return render_template("myprofile.html", user_details = user_details)

@app.post("/editprofile")
def editprofile():
    username = request.form.get("username")
    pwd = request.form.get("password")
    name = request.form.get("fullname")
    email = request.form.get("email")
    telno = request.form.get("telno")

    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    c.execute("SELECT password, fullname, email, telno FROM USER WHERE username = ?", (session["username"],))
    updated_list = c.fetchone()

    user_details = (username, pwd, name, email, telno)

    if session["username"] != username: # Username is updated
        c.execute("SELECT * FROM USER WHERE username = ?", (username,))
        if c.fetchone() == None: # Username can be updated
            c.execute("UPDATE USER SET username=? WHERE username = ?", (username, session["username"]))
            c.execute("UPDATE ADVERTISEMENT SET username=? WHERE username = ?", (username, session["username"]))
            conn.commit()
            conn.close()
            session["username"] = username
            return render_template("myprofile.html", user_details=user_details, error = "Username is updated!")
        else: # Username provided is not unique
            conn.close()
            return render_template("myprofile.html", user_details=user_details, error = "This username is already taken!")
    if updated_list[0] != pwd: # Password has been updated
        c.execute("UPDATE USER SET password=? WHERE username = ?", (pwd, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Password is updated!")
    if updated_list[1] != name: # Name has been updated
        c.execute("UPDATE USER SET fullname=? WHERE username = ?", (name, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Fullname is updated!")
    if updated_list[2] != email:  # Email has been updated
        c.execute("UPDATE USER SET email=? WHERE username = ?", (email, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Email is updated!")
    if updated_list[3] != telno:  # Telno has been updated
        c.execute("UPDATE USER SET telno=? WHERE username = ?", (telno, session["username"]))
        conn.commit()
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="Telno is updated!")
    else:
        conn.close()
        return render_template("myprofile.html", user_details=user_details, error="No update has been occured!")

@app.post("/searchadvertisement")
def searchadvertisement():
    keywords = request.form.get("keywords")
    cname = request.form.get("category")

    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()

    if cname != "all":
        c.execute("""
                  SELECT a.title, a.description, u.fullname, a.aid 
                  FROM CATEGORY c, ADVERTISEMENT a, USER u 
                  WHERE c.cid = a.cid  AND a.username = u.username AND 
                  a.isactive = 1 AND c.cname = ? AND 
                  (a.title LIKE ? OR a.description LIKE ? OR u.fullname LIKE ?)
                  """, (cname, f"%{keywords}%", f"%{keywords}%", f"%{keywords}%"))
        searchList = c.fetchall()
        conn.close()
        return render_template("searchadvertisement.html", searchList=searchList, cname=cname)

    else:
        c.execute("""
               SELECT a.title, a.description, u.fullname, a.aid 
               FROM CATEGORY c, ADVERTISEMENT a, USER u 
               WHERE c.cid = a.cid AND a.username = u.username AND a.isactive = 1 
               AND (a.title LIKE ? OR a.description LIKE ? OR u.fullname LIKE ?)
           """, (f"%{keywords}%", f"%{keywords}%", f"%{keywords}%"))
        searchList = c.fetchall()
        conn.close()
        return render_template("searchadvertisement.html", searchList=searchList, cname=cname)

@app.route("/seeadvertisement", methods=["GET"])
def seeadvertisement():
    aid = request.args.get("aid")

    conn = sqlite3.connect("mydb.db")
    c = conn.cursor()
    c.execute("""
        SELECT a.title, a.description, c.cname, u.fullname, u.email, u.telno
        FROM ADVERTISEMENT a, CATEGORY c, USER u
        WHERE a.cid = c.cid AND a.username = u.username AND
        a.aid = ?        
        """, (aid,))
    advertisement = c.fetchone()

    conn.close()

    return render_template("seeadvertisement.html", advertisement=advertisement)


if __name__ == "__main__":
    app.run(debug=True)