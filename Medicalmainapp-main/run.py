from applications import app
from applications.models import User




if __name__=="__main__":
    with app.app_context():
        users=User.query.all()
        print(users)
    app.run(debug=True)