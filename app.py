from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import pickle
import numpy as np

app = Flask(__name__)

###### MYSQL Configuration 
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'iris_database'

mysql = MySQL(app)

with open("linear_reg_model.pkl","rb") as model_file:
    model = pickle.load(model_file)




@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods = ["GET","POST"])
def predict():
    data = request.form
    print(data)

    
    
    sepal_length_data = float(request.form["sepal_length"])
    sepal_width_data= float(request.form["sepal_width"])
    petal_length_data = float(request.form["petal_length"])
    species_data = float(request.form["species"])
    
    array = [(sepal_length_data,sepal_width_data,petal_length_data,species_data)]
    petal_width = model.predict(array)
    print("Petal_width    == ",petal_width)


    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS iris_tb1(sepal_length VARCHAR(10),sepal_width VARCHAR(10),petal_length VARCHAR(10),species VARCHAR(10),petal_width VARCHAR(50))'
    cursor.execute(query)

    cursor.execute('INSERT INTO iris_tb1(sepal_length,sepal_width,petal_length,species,petal_width) VALUES(%s,%s,%s,%s,%s)',(sepal_length_data,sepal_width_data,petal_length_data,species_data,petal_width))

    mysql.connection.commit()
    cursor.close()


    return render_template("display.html",petal_width=petal_width)


if __name__ == "__main__":
    app.run(host="127.0.0.1",port="5000",debug=True)