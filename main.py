from pickle import TRUE
from website import create_app


app = create_app()

if __name__ == "__main__":
    app.run(debug=TRUE)


