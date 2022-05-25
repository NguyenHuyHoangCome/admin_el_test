from unicodedata import name
from flask import Blueprint, redirect, render_template, request, flash, jsonify, session, url_for
from website import create_app
from collections import OrderedDict
views = Blueprint('views', __name__)
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
from .middle import check_role,check_admin,check_editor,check_manager,user_role,add_action

db = firestore.client()

@views.route('/', methods=['GET', 'POST'])
def home():
	if 'username' in session:
		email,role = user_role()
		#print(email)
		return render_template("index.html",email=email,role=role)
	else:
		return redirect(url_for('auth.login'))
	

@views.route('/test', methods=['GET', 'POST'])
def test():
	if 'username' in session:
		email,role = user_role()
		return render_template("test.html",email=email,role=role)
	else:
		return redirect(url_for('auth.login'))


@views.route('/themques', methods=['GET', 'POST'])
def themques():
	if 'username' in session:
		email,role = user_role()
		return render_template("themcauhoi.html",email=email,role=role)
	else:
		return redirect(url_for('auth.login'))


@views.route('/suaquiz/<name>', methods=['GET', 'POST'])
def suaques(name):
	if 'username' in session:
		email,role = user_role()
		Quiz_detail = db.collection(u'Question').document(name).get()


		if Quiz_detail.exists:
			#print(f'Document data: {Quiz_detail.to_dict()}')
			iquizz = Quiz_detail.to_dict()
			Id_cate_dkt = iquizz['Id_cate_dkt']
			Id_cate_dvkt = iquizz['Id_cate_dvkt']
			Id_cate_mtct = iquizz['Id_cate_mtct']
			level = iquizz['level']
			name_Question = iquizz['name_Question']
			slug = iquizz['slug']

		else:
			print(u'No such document!')
			return "No such document"
		return render_template("sua_cauhoi.html",Id_cate_dkt=Id_cate_dkt, Id_cate_dvkt=Id_cate_dvkt, Id_cate_mtct=Id_cate_mtct, level=level, name_Question=name_Question,slug=slug, name=name,email=email,role=role)
	else:
		return redirect(url_for('auth.login'))
#Thêm câu hỏi

@views.route('/add_ques/<id>', methods=['GET', 'POST'])
def addques(id):
	if 'username' in session:
		email,role = user_role()
		# Quiz_detail = db.collection(u'Question').document(name).get()
		
		#id.split("&")
		a = id.split("&")
		print(a)
		print(a[0])
		print(a[1])
		print(a[2])
		Id_cate_dkt=a[0]
		Id_cate_dvkt=a[1]
		Id_cate_mtct=a[2]
		# Id_cate_dvkt=id.split("&")[2]
		# Id_cate_mtct=id.split("&")[3]
		# if name1 == "Null" and name2=="Null" and name3=="Null":
		# 	return render_template("themcauhoi.html",email=email,role=role)
		# if Quiz_detail.exists:
		# 	#print(f'Document data: {Quiz_detail.to_dict()}')
		# 	iquizz = Quiz_detail.to_dict()
		# 	Id_cate_dkt = iquizz['Id_cate_dkt']
		# 	Id_cate_dvkt = iquizz['Id_cate_dvkt']
		# 	Id_cate_mtct = iquizz['Id_cate_mtct']
		# 	level = iquizz['level']
		# 	name_Question = iquizz['name_Question']
		# 	slug = iquizz['slug']

		# else:
		# 	print(u'No such document!')
		# 	return "No such document"
		#return redirect(url_for('views.test',Id_cate_dkt=Id_cate_dkt,Id_cate_dkt1=Id_cate_dkt1,Id_cate_dkt2=Id_cate_dkt2))
		#return render_template("themcauhoi.html",email=email,role=role)
		#return render_template("test.html",Id_cate_dkt=Id_cate_dkt, Id_cate_dvkt=Id_cate_dvkt, Id_cate_mtct=Id_cate_mtct,email=email,role=role)
		return render_template("add_quess_dm.html",Id_cate_dkt=Id_cate_dkt, Id_cate_dvkt=Id_cate_dvkt, Id_cate_mtct=Id_cate_mtct, email=email,role=role)
		#return render_template("themcauhoi.html",email=email,role=role,Id_cate_dkt=Id_cate_dkt,Id_cate_dkt1=Id_cate_dkt1,Id_cate_dkt2=Id_cate_dkt2)
	else:
		return redirect(url_for('auth.login'))

@views.route('apisua/<id>/<id1>', methods=['GET', 'POST'])
def suadm(id,id1):
	if 'username' in session:
		email,role = user_role()
		if (id == "Null1") :
			dm_detail = db.collection(u'Category_Dang_Kien_Thuc').document(id1).get()
			if dm_detail.exists:
				print(f'Document data: {dm_detail.to_dict()}')
				iquizz = dm_detail.to_dict()
				
				name = iquizz['Name']
				slug = iquizz['Slug']
				#return render_template("sua_danhmuc.html",email=email,role=role)	
			else:
				print(u'No such document!')
				return "No such document"

			return render_template("sua_danhmuc.html", slug=slug, name=name,id1=id1,id=id,email=email,role=role)
		elif(id=="Null2"):
			print(id)
			return render_template("sua_danhmuc.html",email=email,role=role,slug=slug, name=name,id1=id1,id=id)	
	else:
		return redirect(url_for('auth.login'))

@views.route('/danhmuc', methods=['GET', 'POST'])
def danhmuc():
	if 'username' in session:
		email,role = user_role()
		return render_template("danhmuc.html",email=email,role=role)
	else:
		return redirect(url_for('auth.login'))

@views.route('/them_danhmuc', methods=['GET', 'POST'])
def themdm():
	if 'username' in session:
		email,role = user_role()
		if request.method =='POST':
			if request.form['submit']=='add_dkt':
				dkt = request.form['dkt']
				slug = request.form['slug']
				Q = db.collection('Category_Dang_Kien_Thuc').add({ 'Slug': slug, 'Name': dkt})
				#ten =session['username']
				#action = db.collection('action').add({'do': 'thêm dạng kiến thức', 'name': ten, 'object': dkt,'date':  datetime.datetime.now(),'viewer':[]})
				add_action("thêm dạng kiến thức:",dkt)
				return render_template('danhmuc.html',email=email,role=role)
			
			if request.form['submit']=='add_dvkt':
				dvkt = request.form['dvkt']
				slug = request.form['slug']
				id_dkt = request.form['Id_cate_dkt']
				Q = db.collection('Category_Don_vi_kien_thuc').add({'Id_category_dkt':id_dkt, 'Slug': slug, 'Name': dvkt})
				add_action("thêm đơn vị kiến thức:",dvkt)
				return render_template('danhmuc.html',email=email,role=role)

			if request.form['submit']=='add_mtct':
				id_dvkt = request.form['dvkt']
				mtct = request.form['mtct']
				slug = request.form['slug']
				Q = db.collection('Category_mo_ta_chi_tiet').add({'Id_category_dvkt': id_dvkt,'Slug': slug, 'Name': mtct})
				add_action("thêm mô tả chi tiết :",mtct)
				return render_template('danhmuc.html',email=email,role=role)
		return render_template('them_dm.html',email=email,role=role)
	else:
		return redirect(url_for('auth.login'))


@views.route('/add_action/<name>/<id>', methods=['GET', 'POST'])
def add_action_for_view(name,id):
	if 'username' in session:
		
	#	print("hoang cam")
		city_ref = db.collection(u'action').document(id)

		 #Atomically add a new region to the 'regions' array field.
		city_ref.update({u'viewer': firestore.ArrayUnion([name])})
	

		return redirect(url_for('views.ques'))

	else:
		return redirect(url_for('auth.login'))




@views.route('/sua_cauhoi', methods=['GET', 'POST'])
def sua_cauhoi():
	if 'username' in session:
		email,role = user_role()
		if request.method =='POST':
			if request.form['submit']=='add':
				question = request.form['question']
				cate_dkt = request.form['Id_cate_dkt']
				cate_dvkt = request.form['Id_cate_dvkt']
				cate_mtct = request.form['Id_cate_mtct']
				Slug = request.form['slug']
				answer1 = request.form['answer1']
				answer2 = request.form['answer2']
				answer3 = request.form['answer3']
				answer4 = request.form['answer4']
				Level = request.form['level']
				id_ques = request.form['id']
				
				Quiz_detail2 = db.collection(u'Option').where(u'id_Question', u'==', id_ques).stream()
	
				for doc in Quiz_detail2:
					de = doc.id
				#	print(de)
				flexRadioDefault = request.form['flexRadioDefault']
				true_ans = request.form[flexRadioDefault]
				
				city_ref = db.collection(u'Question').document(id_ques)
				city_ref.update({u'name_Question': question,u'level': Level,u'Id_cate_dkt': cate_dkt,u'Id_cate_dvkt': cate_dvkt,u'Id_cate_mtct': cate_mtct,u'slug': Slug})
				city_ref2 = db.collection(u'Option').document(de)
				city_ref2.update({
						u'Option_ans': [answer1, answer2, answer3, answer4],
						u'True_ans': true_ans,
						u'date':  datetime.datetime.now(tz=datetime.timezone.utc)
					})
				add_action("sửa câu hỏi :",id_ques)
				
				return redirect(url_for('views.ques'))


		return redirect(url_for('views.ques'))
	else:
		return redirect(url_for('auth.login'))


@views.route('sua/<id>/<id1>', methods=['GET', 'POST'])
def sua_dkt(id,id1):
	if 'username' in session:
		email,role = user_role()
		if id == "Null" :
			dm_detail = db.collection(u'Category_Dang_Kien_Thuc').document(id1).get()
			if dm_detail.exists:
				print(f'Document data: {dm_detail.to_dict()}')
				iquizz = dm_detail.to_dict()
				print("id dang kt")
				name = iquizz['Name']
				slug = iquizz['Slug']

			else:
				print(u'No such document!')
				return "No such document"
			return render_template("sua_danhmuc.html", slug=slug, name=name,id1=id1,id=id,email=email,role=role)

		elif id =="Null2":
			dm_detail = db.collection(u'Category_Don_vi_kien_thuc').document(id1).get()
			if dm_detail.exists:
				print(f'Document data: {dm_detail.to_dict()}')
				iquizz = dm_detail.to_dict()
				Id_cate_dkt = iquizz['Id_category_dkt']
				name = iquizz['Name']
				slug = iquizz['Slug']

			else:
				print(u'No such document!')
				return "No such document"
			return render_template("sua_danhmuc.html",Id_cate_dkt=Id_cate_dkt, slug=slug, name=name,id=id,id1=id1,email=email,role=role)

		elif id =="Null3":
			dm_detail = db.collection(u'Category_mo_ta_chi_tiet').document(id1).get()
			if dm_detail.exists:
				print(f'Document data: {dm_detail.to_dict()}')
				iquizz = dm_detail.to_dict()
				Id_cate_dkt = iquizz['Id_category_dvkt']
				name = iquizz['Name']
				slug = iquizz['Slug']

			else:
				print(u'No such document!')
				return "No such document"
			return render_template("sua_danhmuc.html",Id_cate_dkt=Id_cate_dkt, slug=slug, name=name,id=id,id1=id1,email=email,role=role)
		

		
	else:
		return redirect(url_for('auth.login'))

@views.route('/sua_danhmuc', methods=['GET', 'POST'])
def sua_danhmuc():
	if 'username' in session:
		email,role = user_role()
		if request.method =='POST':
			if request.form['submit']=='sua_dkt':
				Id1 = request.form['Id2']
				if Id1 =='Null':
					Id_cate_dkt = request.form['Id1']
					print(Id_cate_dkt)
					dkt = request.form['dkt']
					slug = request.form['slug']
					city_ref = db.collection(u'Category_Dang_Kien_Thuc').document(Id_cate_dkt)
					city_ref.update({u'Name': dkt,u'Slug':slug})
					add_action("sửa dạng kiến thức :",dkt)
					return render_template('danhmuc.html',email=email,role=role)
				
				elif Id1 =='Null2':
					Id_cate_dkt = request.form['Id1']
					print(Id_cate_dkt)
					dkt = request.form['dkt']
					slug = request.form['slug']
					city_ref = db.collection(u'Category_Don_vi_kien_thuc').document(Id_cate_dkt)
					city_ref.update({u'Name': dkt,u'Slug':slug})
					add_action("sửa đơn vị kiến thức :",dkt)
					return render_template('danhmuc.html',email=email,role=role)
				
				
				elif Id1 =='Null3':
					Id_cate_dkt = request.form['Id1']
					print(Id_cate_dkt)
					dkt = request.form['dkt']
					slug = request.form['slug']
					city_ref = db.collection(u'Category_mo_ta_chi_tiet').document(Id_cate_dkt)
					city_ref.update({u'Name': dkt,u'Slug':slug})
					add_action("sửa mô tả chi tiết :",dkt)
					return render_template('danhmuc.html',email=email,role=role)
	else:
		return redirect(url_for('auth.login'))

@views.route('/form', methods=['GET', 'POST'])
def basic():
	if 'username' in session:
		email,role = user_role()
		if request.method =='POST':
			if request.form['submit']=='add':
				try:
					question = request.form['question']
					cate_dkt = request.form['Id_cate_dkt']
					cate_dvkt = request.form['Id_cate_dvkt']
					cate_mtct = request.form['Id_cate_mtct']
					Slug = request.form['slug']
					answer1 = request.form['answer1']
					answer2 = request.form['answer2']
					answer3 = request.form['answer3']
					answer4 = request.form['answer4']
					Level = request.form['level']
					
			
					
				
					flexRadioDefault = request.form['flexRadioDefault']
					true_ans = request.form[flexRadioDefault]
				
				except:
					flash('Điền đầy đủ vào bạn ơiiii','sussess')
					return redirect(url_for('views.basic'))
				
				d = db.collection('Question').add({'name_Question':question, 'Id_cate_dkt':cate_dkt ,'Id_cate_dvkt':cate_dvkt,'Id_cate_mtct':cate_mtct,'level':Level,'slug':Slug})
				docId = d[1].id
				new_city_ref = db.collection("Option").document()
				new_city_ref.set(
					{
						u'id_Question': docId,
						u'Option_ans': [answer1, answer2, answer3, answer4],
						u'True_ans': true_ans,
						u'date':  datetime.datetime.now(tz=datetime.timezone.utc),
					}
				)
				add_action("sửa câu hỏi :",docId)
				return redirect(url_for('views.ques'))
		return render_template('themcauhoi.html',email=email,role=role)
	else:
		return redirect(url_for('auth.login'))


@views.route('/cauhoi', methods=['GET', 'POST'])
def ques():
	if 'username' in session:
		email,role = user_role()
		return render_template("cauhoi.html",email=email,role=role)
	else:
		return redirect(url_for('auth.login'))


# if request.method =='POST':
		# 	if request.form['submit']=='sua_dkt':
		# 		Id_cate_dkt = request.form['Id_cate_dkt']
		# 		print(Id_cate_dkt)
		# 		dkt = request.form['dkt']
		# 		slug = request.form['slug']
		# 		city_ref = db.collection(u'Category_Dang_Kien_Thuc').document(Id_cate_dkt)
		# 		city_ref.update({u'Name': dkt})
		# 		return render_template('sua_danhmuc.html')

		# 	elif request.form['submit']=='sua_dvkt':
		# 		Id_cate_dvkt = request.form['Id_cate_dvkt']
		# 		dkt = request.form['dvkt']
		# 		slug = request.form['slug']
		# 		city_ref = db.collection(u'Category_Don_vi_kien_thuc').document(Id_cate_dvkt)
		# 		city_ref.update({u'Name': dkt})
		# 		return render_template('sua_danhmuc.html')

		# 	elif request.form['submit']=='sua_mtct':
		# 		Id_cate_dvkt = request.form['Id_cate_mtct']
		# 		dkt = request.form['dvkt']
		# 		slug = request.form['slug']
		# 		city_ref = db.collection(u'Category_mo_ta_chi_tiet').document(Id_cate_dvkt)
		# 		city_ref.update({u'Name': dkt})
		# 		return render_template('sua_danhmuc.html')