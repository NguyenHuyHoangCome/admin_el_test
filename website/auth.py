from multiprocessing import AuthenticationError
from flask import Blueprint, render_template, request, flash, jsonify, redirect, session, url_for
from requests_toolbelt import user_agent
from website import create_app
from collections import OrderedDict
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials, initialize_app
from firebase_admin import firestore
from firebase_admin import storage
import datetime
import urllib.parse
import os
from werkzeug.utils import secure_filename
import urllib.request
import tempfile
import random
import string
import pyrebase
import json
from .middle import check_role,check_admin,check_editor,check_manager,user_role,add_action


auth1 = Blueprint('auth', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# from flask_login import login_user, login_required, logout_user, current_user


db = firestore.client()
pb = pyrebase.initialize_app(json.load(open('website/keypb.json')))

@auth1.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('views.home'))
    if request.method =='POST':
       
        email = request.form['email']
        password = request.form['password']
        if email is None or password is None:
            flash('Nhập đầy đủ dữ liệu','warning')
            return render_template("login.html")
        try:
            user = pb.auth().sign_in_with_email_and_password(email, password)
            print(user)
            uid=''
            for x in user:
                if x == 'localId':
                    uid=(user[x])
            print(uid)
            User = db.collection(u'User').document(uid).get()
            if User.exists:
                iquizz = User.to_dict()
                role = iquizz['Role']
                if check_role(role) == True:
                    session['username'] = email
                    session['role'] = role
                    return redirect(url_for('views.home'))
                else:
                    flash('Bạn không có quyền try cập','warning')
                    return render_template("login.html")
                    
            else:
                flash('Lỗi, không tồn tại','warning')
                return render_template("login.html")

        except:
            flash('Lỗi, Hãy thử lại','warning')
            return render_template("login.html")
    return render_template("login.html")

@auth1.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        if request.method == "POST":
            email = request.form['val-email']
            password = request.form['val-password']
            age = request.form['val-age']
            name = request.form['val-name']
            role = request.form['val-skill']
            phone = request.form['val-phoneus']
            # print(email)
            file = request.files['file']
            if file.filename == '':
                if email is None or password is None:
                    return {'message': 'Error missing email or password'},400
                try:
                    user = auth.create_user(
                        email=email,
                        password=password,
                    )
                    ref = db.collection(u'User').document(user.uid)
                    ref.set({
                        u'Age': age,
						u'Avatar': '',
						u'Name':  name,
						u'Role':  role,
						u'Email':  email,
						u'Uid':  user.uid,
						u'Phone':  phone,
                    })
                    add_action("Thêm user có id",user.uid)
                    flash('Thêm tài khoản '+ email +' thành công','success')
                    email,role = user_role()
                    return redirect(url_for('auth.admin'))
                except:
                    page = auth.list_users()
                    while page:
                        for user in page.users:
                            if email == user.email:
                                ref = db.collection(u'User').document(user.uid)
                                ref.update({
                                    u'Age': age,
                                    u'Avatar': '',
                                    u'Name':  name,
                                    u'Role':  role,
                                    u'Email':  email,
                                    u'Uid':  user.uid,
                                    u'Phone':  phone,
                                })
                        page = page.get_next_page()
                    add_action("Tài khoản đã tồn tại, cập nhập user có id",user.uid)
                    flash('Tài khoản đã tồn tại, cập nhập '+ email +' thành công','success')
                    email,role = user_role()
                    return redirect(url_for('auth.admin'))

            if file and allowed_file(file.filename):
                temp = tempfile.NamedTemporaryFile(delete=False)
                file.save(temp.name)

                bucket = storage.bucket()
                try:
                    user = auth.create_user(
                        email=email,
                        password=password,
                    )
                    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))   
                    blob = bucket.blob("images/" + user.uid + '_' + str(ran) + '.jpg')
                    with open(temp.name, "rb") as f:
                        blob.upload_from_file(f)
                    f.close()
                    blob.make_public()
                    link = blob.public_url
                    print(link)
                    temp.close()
                    os.remove(temp.name)
                    ref = db.collection(u'User').document(user.uid)
                    ref.set({
                        u'Age': age,
						u'Avatar': link,
						u'Name':  name,
						u'Role':  role,
						u'Email':  email,
						u'Uid':  user.uid,
						u'Phone':  phone,
                    })
                    add_action("Thêm user có id",user.uid)
                    flash('Thêm tài khoản '+ email +' thành công','success')
                    email,role = user_role()
                    return redirect(url_for('auth.admin'))
                except:
                    page = auth.list_users()
                    while page:
                        for user in page.users:
                            if email == user.email:
                                ref = db.collection(u'User').document(user.uid)
                                try:
                                    avatar = db.collection(u'User').document(user.uid).get().to_dict().get('Avatar')
                                    link_old = avatar.split('/')
                                    blob = bucket.blob("images/" + link_old[-1])
                                    blob.delete()
                                except:
                                    print("error delete")
                                ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))   
                                blob = bucket.blob("images/" + user.uid + '_' + str(ran) + '.jpg')
                                with open(temp.name, "rb") as f:
                                    blob.upload_from_file(f)
                                f.close()
                                blob.make_public()
                                link = blob.public_url
                                print(link)
                                temp.close()
                                os.remove(temp.name)
                                ref.update({
                                    u'Age': age,
                                    u'Avatar': link,
                                    u'Name':  name,
                                    u'Role':  role,
                                    u'Email':  email,
                                    u'Uid':  user.uid,
                                    u'Phone':  phone,
                                })
                        page = page.get_next_page()
                    add_action("Tài khoản đã tồn tại, cập nhập user có id",user.uid)
                    flash('Tài khoản đã tồn tại, cập nhập '+ email +' thành công','success')
                    email,role = user_role()
                    return redirect(url_for('auth.admin'))
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif','warning')
                email,role = user_role()
                return redirect(request.url)      
        email,role = user_role()
        return render_template("register.html",email=email,role=role)
    else:
        return redirect(url_for('auth.login'))


@auth1.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

@auth1.route('/user', methods=['GET', 'POST'])
def user():
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        email= session['username']
        role = session['role']
        return render_template("user.html",email=email,role=role)
        
    else:
        return redirect(url_for('auth.login'))

@auth1.route('/admin', methods=['GET', 'POST'])
def admin():
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        email= session['username']
        role = session['role']
        return render_template("admin.html",email=email,role=role)
        
    else:
        return redirect(url_for('auth.login'))

@auth1.route('/api/admin', methods=['GET', 'POST'])
def api_admin():
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        admin = db.collection(u'User').where(u'Role', u'==', u'Admin').stream()
        detail = []
        for doc in admin:
            de = doc.to_dict()
            detail.append(de)
        manager = db.collection(u'User').where(u'Role', u'==', u'Manager').stream()

        for doc in manager:
            de = doc.to_dict()
            detail.append(de)
        editor = db.collection(u'User').where(u'Role', u'==', u'Editor').stream()

        for doc in editor:
            de = doc.to_dict()
            detail.append(de)
        return jsonify(detail)


@auth1.route('/api/user', methods=['GET', 'POST'])
def api_user():
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        users = db.collection(u'User').stream()
        detail = []
    
        for doc in users:
            de = doc.to_dict()
            detail.append(de)
        return jsonify(detail)

@auth1.route('/api/user/<id>', methods=['GET', 'POST'])
def api_user_id(id):
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        detail = []
        doc_ref = db.collection(u'User').document(id)
        doc = doc_ref.get()
        if doc.exists:
            detail.append(doc.to_dict())
            return jsonify(detail)
        else:
            return 'Error'


@auth1.route('/delete/user/<id>', methods=['GET', 'POST'])
def delete_user(id):
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        auth.delete_user(id)
        add_action("xóa user có id",id)
        flash('Xóa tài khoản có ID:'+id+' thành công','success')
        return redirect(url_for('auth.user'))
    else:
        return redirect(url_for('auth.login'))

@auth1.route('/delete/user/chucvu/<id>', methods=['GET', 'POST'])
def delete_user_chucvu(id):
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        ref = db.collection(u'User').document(id)
        ref.update({
                u'Role': "",
            })
        add_action("xóa chức vụ user có id",id)
        flash('Xóa chức vụ tài khoản có ID:'+id+' thành công','success')
        return redirect(url_for('auth.admin'))
    else:
        return redirect(url_for('auth.login'))

@auth1.route('/update/user/<id>', methods=['GET', 'POST'])
def update_user(id):
    if 'username' in session:
        if check_editor == True:
            return redirect(url_for('views.home'))
        if request.method == "POST":
            email = request.form['Email']
            uid = request.form['Uid']
            age = request.form['Age']
            name = request.form['Name']
            role = request.form['Role']
            print(email)
            file = request.files['file']
            if file.filename == '':
                ref = db.collection(u'User').document(uid)
                ref.update({
						u'Age': age,
						u'Name':  name,
						u'Role':  role,
					})
                add_action("Cập nhập user có id",uid)
                flash('Cập nhập tài khoản '+ email +' thành công','success')
                return redirect(url_for('auth.user'))

            if file and allowed_file(file.filename):
                temp = tempfile.NamedTemporaryFile(delete=False)
                file.save(temp.name)

                bucket = storage.bucket()
               
                try:
                    avatar = db.collection(u'User').document(uid).get().to_dict().get('Avatar')
                    link_old = avatar.split('/')
                    blob = bucket.blob("images/" + link_old[-1])
                    blob.delete()
                except:
                    print("error delete")
                ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))   
                blob = bucket.blob("images/" + uid + '_' + str(ran) + '.jpg')
                with open(temp.name, "rb") as f:
                    blob.upload_from_file(f)
                f.close()
                blob.make_public()
                link = blob.public_url
                print(link)
                temp.close()
                os.remove(temp.name)
                ref = db.collection(u'User').document(uid)
                ref.update({
						u'Age': age,
						u'Avatar': link,
						u'Name':  name,
						u'Role':  role,
					})
                add_action("Cập nhập user có id",uid)
                flash('Cập nhập tài khoản '+ email +' thành công','success')
                return redirect(url_for('auth.user'))
            else:
                flash('Allowed image types are -> png, jpg, jpeg, gif','warning')
                return redirect(request.url)      
        email= session['username']
        role = session['role']               
        return render_template("update_user.html",id=id,email=email,role=role)
    else:
        return redirect(url_for('auth.login'))