from flask import Flask, render_template
import pandas as pd
import matplotlib


app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[['STAID','STANAME                                 ']]

@app.route("/")
def home():
    return render_template("home.html", data= stations.to_html())


@app.route("/tutorial/")
def tutorial():
    return render_template("tutorial.html")


@app.route("/about/")
def about():
    return render_template("about.html")


@app.route("/api/v1/<station>/<date>")
def call_api(station, date):
    filename= "data_small\TG_STAID" + str(station).zfill(6) +".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE']==date]['   TG'].squeeze()/10
    
    
    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<station>/")
def station_only(station):
    filename= "data_small\TG_STAID" + str(station).zfill(6) +".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=['    DATE'])
    dish = df.to_dict(orient="records")
    # plot = df.loc[df['   TG'] != -9999]['   TG'].hist()
    return dish

@app.route("/api/v1/annual/<station>/<year>/")
def annual(year,station):
    filename= "data_small\TG_STAID" + str(station).zfill(6) +".txt"
    df = pd.read_csv(filename, skiprows=20)
    df['    DATE']=df['    DATE'].astype(str)
    yearly_result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return yearly_result
    
if __name__ == '__main__':
    app.run(debug=True)
