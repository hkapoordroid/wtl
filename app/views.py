from app import app	
from flask import redirect, request, render_template, flash
import requests
import json 
import boto3
from loginform import LoginForm 


clientID = '26d2405a54464c8d93cc2cc786401246'
clientSecret = '3f6f68e1ab2841a9831f10bf6a13bcfd'
redirectUrl = 'http://127.0.0.1:5000/index'



@app.route('/sga', methods=['GET', 'POST'])
def setupgiveaway():
	if request.method == 'POST':
		#gather the data from the form
		igLinkUrl = request.form['igimageurl']
		gaTitle = request.form['gatitle']
		gaType = request.form['gatype']
		description = request.form['description']
		userTZ = request.form['usertz']

		return render_template('giveawayconfirm.html', 
								ig_embed_url = igLinkUrl,
								ga_title = gaTitle,
								ga_description = description,
								ga_timezone = userTZ
								)
		return igLinkUrl
	else:
		return render_template('giveawayform.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    	flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
    	redirect('/authenticate')
    return render_template('login.html', 
                           title='Sign In',
                           loginform=form,
                           providers=app.config['OPENID_PROVIDERS'])


@app.route('/authenticate')
def authenticate():
	igAuthUrl = 'https://api.instagram.com/oauth/authorize/?client_id='+clientID+'&redirect_uri='+redirectUrl+'&response_type=code&scope=basic+public_content+follower_list+comments+relationships+likes'

	#initialize the global variables and settings
	return redirect(igAuthUrl)

@app.route('/index')
def index():
	code = request.args.get('code')
	r = requests.post('https://api.instagram.com/oauth/access_token', data={ 'client_id' : clientID, 
																			'client_secret' : clientSecret, 
																			'grant_type' : 'authorization_code', 
																			'redirect_uri' : redirectUrl,
																			'code' : code })


	resObj = json.loads(r.text)
	
	accessToken = resObj['access_token']
	userID = resObj['user']['id']
	userName = resObj['user']['username']
	userProfilePic = resObj['user']['profile_picture']
	userFullName = resObj['user']['full_name']
	userBio = resObj['user']['bio']
	userWebsite = resObj['user']['website']

	return accessToken
