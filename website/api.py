import datetime
from pydoc import Doc
import random
import urllib.parse

from unicodedata import category
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import *
from collections import OrderedDict
from flask.json import JSONEncoder
from flask_cors import CORS
import json

from .middle import check_role,check_admin,check_editor,check_manager,user_role,add_action
from flask import Blueprint, render_template, request, flash, jsonify

db = firestore.client()
api = Blueprint('api', __name__)

@api.route('/api/dkt_ver2_for_table', methods=['GET', 'POST'])
def dkt_ver2_for_table():
	users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
	detail = []
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	for i in detail:
		id = i['Id']
		list_dvkt = []
		ct_dvkt = db.collection(u'Category_Don_vi_kien_thuc').where(u'Id_category_dkt', u'==', id).stream()
		tong_mtct = 0
	

		for doc_dvkt in ct_dvkt:
			de_dvkt = doc_dvkt.to_dict()
			de_dvkt['Id'] = doc_dvkt.id
			list_dvkt.append(de_dvkt)
		if list_dvkt != []:
			for i2 in list_dvkt:
				list_mtct = []
				id1 = i2['Id']
				list_mo_ta_chi_tiet = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id1).stream()
				for doc_mtct in list_mo_ta_chi_tiet:
					de_mtct = doc_mtct.to_dict()
					list_mtct.append(de_mtct)
				i2['data_mtct'] = list_mtct

				if(len(list_mtct) != 0):
					tong_mtct += len(list_mtct)
				else:
					tong_mtct += 1
			
			if (len(list_dvkt) != 0):
				i['Row_dvkt'] = len(list_dvkt)
				i['Row_mtct'] = tong_mtct
			else:
				i['Row_dvkt'] = 1
				i['Row_mtct'] = tong_mtct
		else:
			
			i['Row_dvkt'] = 1
			i['Row_mtct'] = 1
		i['data_dvkt'] = list_dvkt
		# print(len(list_dvkt))
 
	return jsonify(detail)

@api.route('/api/dvkt/<id>', methods=['GET', 'POST'])
def api_id_dvkt(id):
	Quiz_detail = db.collection(u'Category_Don_vi_kien_thuc').where(u'Id_category_dkt', u'==', id).stream()
	detail = []
	deto = {}
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)

@api.route('/api/dvkt2/<id>', methods=['GET', 'POST'])
def api_id_dvkt2(id):
		Quiz = db.collection(u'Category_Don_vi_kien_thuc').where(u'Id_category_dkt', u'==', id).stream()
		detail= []
		for doc in Quiz:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
			print(detail)
		
		return jsonify(detail)

@api.route('/api/dvkt2/<id>/<id2>', methods=['GET', 'POST'])
def api_id_dvkt_level(id,id2):
		Quiz_level = db.collection(u'Question').where(u'level', u'==', id2).where(u'Id_category_dkt', u'==', id).stream()
		detail_level = []
		for doclv in Quiz_level:
			delv = doclv.to_dict()
			delv['Id'] = doc.id
			detail_level.append(de)
			print(detail_level)
		
		return jsonify(detail_level)


@api.route('/api/level/<id>', methods=['GET', 'POST'])
def api_id_level(id):
	Quiz_detail = db.collection(u'Question').where(u'level', u'==', id).stream()
	detail = []
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	
	return jsonify(detail)

@api.route('/api/mtct/<id>', methods=['GET', 'POST'])
def api_id_mtct(id):
	Quiz_detail = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id).stream()
	detail = []
	deto = {}
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)

@api.route('/api/mtct2/<id>', methods=['GET', 'POST'])
def api_id_mtct1(id):
	Quiz_detail = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id).stream()
	detail = []
	deto = {}
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	
	return jsonify(detail)

@api.route('/api/action', methods=['GET', 'POST'])
def api_action():
	Quiz_detail = db.collection(u'action').order_by(
    u'date', direction=firestore.Query.DESCENDING).limit(5).stream()
	detail = []
	deto = {}
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	
		#print(de)
	return jsonify(detail)



@api.route('/del_mtct/<id>', methods=['GET', 'POST'])
def api_del_mtct(id):
	Quiz_detail2 = db.collection(u'Question').where(u'Id_cate_mtct', u'==', id).stream()
	da = []
	for doc in Quiz_detail2:
		de = doc.id
		da.append(de)
	print(da)
	if da == []:
		Quiz_detail2 = db.collection(u'Category_mo_ta_chi_tiet').document(id).delete()
		print("rỗng đấy")
	else:
		print("ko rỗng đâu, ko xóa đc")


	return render_template("motachitiet.html")

@api.route('/del_dvkt/<id>', methods=['GET', 'POST'])
def api_del_dvkt(id):
	Quiz_detail2 = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id).stream()
	da = []
	for doc in Quiz_detail2:
		de = doc.id
		da.append(de)
	print(da)
	if da == []:
		Quiz_detail2 = db.collection(u'Category_Don_vi_kien_thuc').document(id).delete()
		print("rỗng đấy")
	else:
		print("ko rỗng đâu, ko xóa đc")


	return render_template("donvikienthuc.html")

@api.route('/del_mtct/<id1>/<id2>', methods=['GET', 'POST'])
def api_del_dkt(id1,id2):
	if id1 =='Null':
		Quiz_detail2 = db.collection(u'Category_Don_vi_kien_thuc').where(u'Id_category_dkt', u'==', id2).stream()
		da = []
		for doc in Quiz_detail2:
			de = doc.id
			da.append(de)
		print(da)
		if da == []:
			Quiz_detail2 = db.collection(u'Category_Dang_Kien_Thuc').document(id2).delete()
			print("Xóa thành công")
			add_action("xóa dạng kiến thức theo id",id2)
			return"Xóa thành công"
		else:
			print("ko rỗng đâu, ko xóa đc")
			return "ko rỗng đâu, Không xóa được"

		
	elif id1 == 'Null2':
		Quiz_detail2 = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id2).stream()
		da = []
		for doc in Quiz_detail2:
				de = doc.id
				da.append(de)
		print(da)
		if da == []:
			Quiz_detail2 = db.collection(u'Category_Don_vi_kien_thuc').document(id2).delete()
			print("Xóa thành công")
			add_action("xóa đơn vị kiến thức theo id",id2)

			return("Xóa thành công")
		else:
			print("ko rỗng đâu, ko xóa đc")
			return "ko rỗng đâu, Không xóa được"


	elif id1 == 'Null3':
		Quiz_detail2 = db.collection(u'Question').where(u'Id_cate_mtct', u'==', id2).stream()
		da = []
		for doc in Quiz_detail2:
			de = doc.id
			da.append(de)
		print(da)
		if da == []:
			Quiz_detail2 = db.collection(u'Category_mo_ta_chi_tiet').document(id2).delete()
			print("Xóa thành công")
			add_action("xóa mô tả chi tiết theo id",id2)
			return("Xóa thành công")
		else:
			print("ko rỗng đâu, ko xóa đc")
			return "ko rỗng đâu, Không xóa được"

@api.route('/sua_danhmuc/<id1>/<id2>', methods=['GET', 'POST'])
def api_sua_dm(id1,id2):
	# if id1 =='01':
	# 	Quiz_detail2 = db.collection(u'Category_Dang_Kien_Thuc').where(u'Id_category_dkt', u'==', id2).stream()
	# 	detail = []
	# 	print(id1)
	# 	print(id2)
	# 	deto = {}
	# 	for doc in Quiz_detail2:
	# 		de = doc.to_dict()
	# 		de['Id'] = doc.id
	# 		detail.append(de)
	# 		print(de)
	# 	print(detail)
	# 	return jsonify(detail)
		# if da == []:
		# 	Quiz_detail2 = db.collection(u'Category_Dang_Kien_Thuc').document(id2).delete()
		# 	print("Xóa thành công")
		# 	return"Xóa thành công"
		# else:
		# 	print("ko rỗng đâu, ko xóa đc")
		# 	return "ko rỗng đâu, Không xóa được"
	
	a = urllib.parse.unquote(id2)
	print(a)
	if id1 == '02':
		Quiz_detail2 = db.collection(u'Category_Don_vi_kien_thuc').document(id2).get()
		print(id2)
		if Quiz_detail2.exists:
			
			print(f'Document data: {Quiz_detail2.to_dict()}')
			iquizz = Quiz_detail2.to_dict()
			dkt = iquizz['Name']
			slug = iquizz['Slug']
			

		else:
			print(u'No such document!')
			return "No such document"

		return redirect(url_for('auth.login'))
		


	# elif id1 == '03':
	# 	Quiz_detail2 = db.collection(u'Question').where(u'Id_cate_mtct', u'==', id2).stream()
	# 	da = []
	# 	for doc in Quiz_detail2:
	# 		de = doc.id
	# 		da.append(de)
	# 	print(da)
	# 	if da == []:
	# 		Quiz_detail2 = db.collection(u'Category_mo_ta_chi_tiet').document(id2).delete()
	# 		print("Xóa thành công")
	# 		return("Xóa thành công")
	# 	else:
	# 		print("ko rỗng đâu, ko xóa đc")
	# 		return "ko rỗng đâu, Không xóa được"

@api.route('/api/ques/<id>', methods=['GET', 'POST'])
def api_ques_id(id):

	Quiz_detail = db.collection(u'Option').where(u'id_Question', u'==', id).stream()
	detail = []
	deto = {}
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)


@api.route('/api/ques1/<id>', methods=['GET', 'POST'])
def api_ques_id12(id):

	Quiz_detail = db.collection(u'Option').where(u'id_Question', u'==', id).stream()
	detail = []
	deto = {}
	for doc in Quiz_detail:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	
	return jsonify(detail)


@api.route('/delete_ques/<id>', methods=['GET', 'POST'])
def api_delete_ques_id(id):
	
	Quiz_detail2 = db.collection(u'Option').where(u'id_Question', u'==', id).stream()
	
	for doc in Quiz_detail2:
		de = doc.id

		Quiz_detail2 = db.collection(u'Option').document(de).delete()

	Quiz_detail1 = db.collection(u'Question').document(id).delete()
	add_action("xóa câu hỏi theo id : ",id)


	return redirect(url_for('views.ques'))

@api.route('/search/<id>', methods=['GET', 'POST'])
def api_search(id):
	

	x = id.split(',')
	detail = []
	deto = {}
	for i in x:
		Quiz_detail = db.collection(u'Question').document(i).get()
	
		if Quiz_detail.exists:
	
			de = Quiz_detail.to_dict()
			de['Id'] = Quiz_detail.id
			detail.append(de)
	deto['data'] = detail

	return jsonify(deto)



@api.route('/api/ques1/<id>/<id1>/<id2>', methods=['GET', 'POST'])
def api_ques_id1(id,id1,id2):
	if(id=="Null"):
		users_ref = db.collection(u'Question').stream()
		detail = []
		deto = {}
		for doc in users_ref:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)
		# my_dict = { el.id: el.to_dict() for el in users_ref }
		
		return jsonify(dictionary)
	elif(id1=="Null" and id2=="Null"):
		Quiz_detail = db.collection(u'Question').where(u'Id_cate_dkt', u'==', id).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)
	elif(id2=="Null"):
		Quiz_detail = db.collection(u'Question').where(u'Id_cate_dvkt', u'==', id1).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)
	else:
		Quiz_detail = db.collection(u'Question').where(u'Id_cate_mtct', u'==', id2).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)


@api.route('/api/quess/<id>/<id1>/<id2>', methods=['GET', 'POST'])
def api_ques_tu(id,id1,id2):
	if(id=="Null"):
		users_ref = db.collection(u'Question').stream()
		detail = []
		deto = {}
		for doc in users_ref:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
		# my_dict = { el.id: el.to_dict() for el in users_ref }
		
		return jsonify(dictionary)
	elif(id1=="Null" and id2=="Null"):
		Quiz_detail = db.collection(u'Question').where(u'Id_cate_dkt', u'==', id).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		
		return jsonify(detail)
	elif(id2=="Null"):
		Quiz_detail = db.collection(u'Question').where(u'Id_cate_dvkt', u'==', id1).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
	else:
		Quiz_detail = db.collection(u'Question').where(u'Id_cate_mtct', u'==', id2).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
	

@api.route('/api/quess/<id>/<id1>', methods=['GET', 'POST'])
def api_ques_dm(id,id1):
	if(id=="Null"):
		users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
		detail = []
		deto = {}
		for doc in users_ref:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
		# my_dict = { el.id: el.to_dict() for el in users_ref }
		
	elif(id1=="Null"):
		print("id1 null")
		Quiz_detail = db.collection(u'Category_Don_vi_kien_thuc').where(u'Id_category_dkt', u'==', id).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		
		return jsonify(detail)
	
	else:
		Quiz_detail = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id1).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
	


@api.route('/api/quessdm/<id>/<id1>', methods=['GET', 'POST'])
def api_ques_dm2(id,id1):
	if(id=="Null1"):
		users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
		detail = []
		deto = {}
		for doc in users_ref:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
		# my_dict = { el.id: el.to_dict() for el in users_ref }
		
	elif(id1=="Null2"):
		print("id1 null")
		Quiz_detail = db.collection(u'Category_Don_vi_kien_thuc').where(u'Id_category_dkt', u'==', id).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		
		return jsonify(detail)
	
	else:
		Quiz_detail = db.collection(u'Category_mo_ta_chi_tiet').where(u'Id_category_dvkt', u'==', id1).stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
	
		return jsonify(detail)
	



@api.route('/api/dkt', methods=['GET', 'POST'])
def api_quiz():
	users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)
	
@api.route('/api/dkt_ver2', methods=['GET', 'POST'])
def api_quiz_ver2():
	users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	return jsonify(detail)

@api.route('/api/dkt/<id>', methods=['GET', 'POST'])
def api_danhmuc(id):
	if(id=="01"):
		users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
		detail = []
		deto = {}
		for doc in users_ref:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)
		
		return jsonify(dictionary)
	elif(id=="02"):
		Quiz_detail = db.collection(u'Category_Don_vi_kien_thuc').stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)
	elif(id=="03"):
		Quiz_detail = db.collection(u'Category_mo_ta_chi_tiet').stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		deto['data'] = detail
		return jsonify(deto)

@api.route('/api/dktsua/<id>', methods=['GET', 'POST'])
def api_danhmuc1(id):
	if(id=="01"):
		users_ref = db.collection(u'Category_Dang_Kien_Thuc').stream()
		detail = []
		deto = {}
		for doc in users_ref:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		return jsonify(detail)
		
		return jsonify(dictionary)
	elif(id=="02"):
		Quiz_detail = db.collection(u'Category_Don_vi_kien_thuc').stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		return jsonify(detail)
	elif(id=="03"):
		Quiz_detail = db.collection(u'Category_mo_ta_chi_tiet').stream()
		detail = []
		deto = {}
		for doc in Quiz_detail:
			de = doc.to_dict()
			de['Id'] = doc.id
			detail.append(de)
		return jsonify(detail)

@api.route('/api/ques', methods=['GET', 'POST'])
def api_dkt():
	users_ref = db.collection(u'Question').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)
	# my_dict = { el.id: el.to_dict() for el in users_ref }
	

@api.route('/api/quess', methods=['GET', 'POST'])
def api_dkt12():
	users_ref = db.collection(u'Question').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	
	return jsonify(detail)
	# my_dict = { el.id: el.to_dict() for el in users_ref }
	



@api.route('/api/dvkt', methods=['GET', 'POST'])
def api_donvi_kt():
	users_ref = db.collection(u'Category_Don_vi_kien_thuc').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)


@api.route('/api/dvkt_ver2', methods=['GET', 'POST'])
def api_donvi_kt_ver2():
	users_ref = db.collection(u'Category_Don_vi_kien_thuc').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	return jsonify(detail)

@api.route('/api/mtct', methods=['GET', 'POST'])
def api_danhmucmtct():
	users_ref = db.collection(u'Category_mo_ta_chi_tiet').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	deto['data'] = detail
	return jsonify(deto)

@api.route('/api/mtct_ver2', methods=['GET', 'POST'])
def api_mtct_ver2():
	users_ref = db.collection(u'Category_mo_ta_chi_tiet').stream()
	detail = []
	deto = {}
	for doc in users_ref:
		de = doc.to_dict()
		de['Id'] = doc.id
		detail.append(de)
	return jsonify(detail)

# @app.route('/api/ques', methods=['GET', 'POST'])
# def api_menu():
# 	users_ref = db.collection(u'Quiz').stream()
# 	data = OrderedDict([(doc.id, doc.to_dict()) for doc in users_ref])
# 	return jsonify(data)



@api.route('/api/test/<id>/<id2>/<id3>', methods=['GET', 'POST'])
def api_test(id,id2,id3):
	print(id)
	print(id2)
	print(id3)
	return "dsadad"