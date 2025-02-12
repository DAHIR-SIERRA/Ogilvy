from flask import Blueprint, render_template, request, flash, redirect, url_for



hsoprt_bp = Blueprint('homeSoport', __name__)

 
@hsoprt_bp.route('/homeSoport', methods=['GET', 'POST'])
def home():
       return render_template('homeSoport.html')
