from applications import app
from applications.models import User, Checkup




if __name__=="__main__":
    with app.app_context():
        users=User.query.all()
        checkups=Checkup.query.all()
        print(users)
        print(checkups)
    app.run(debug=True)