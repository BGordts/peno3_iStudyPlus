@app.route('/home')
def home():
    user = User.query.get(session["userID"])
    return render_template('pages/dashboard_profile-info.html', user=user)

@app.route('/welcome')
@login_required
def welcome():
    return render_template('pages/dashboard.html')