from flask import Blueprint, render_template, request, flash, jsonify, redirect, session, url_for
from firebase_admin import firestore
import datetime
db = firestore.client()

def check_role(role):
    role_list = ['Admin', 'Manager', 'Editor']
    che = False
    for i in role_list:
        if(role == i):
            che = True
    return che

def check_admin():
    che = False
    role = session['role']
    role_list = 'Admin'
    if role == role_list:
        che = True
    return che

def check_manager():
    che = False
    role = session['role']
    role_list = 'Manager'
    if role == role_list:
        che = True
    return che

def check_editor():
    che = False
    role = session['role']
    role_list = 'Editor'
    if role == role_list:
        che = True
    return che

def user_role():
    email= session['username']
    role = session['role']
    return email, role
def add_action(do,oj):

    ten =session['username']
    action = db.collection('action').add({'do': do, 'name': ten, 'object': oj,'date':  datetime.datetime.now(),'viewer':[]})
    return True