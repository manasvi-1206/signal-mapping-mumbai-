from flask import Flask, render_template, request, jsonify
import pandas as pd
import os
from werkzeug.utils import secure_filename
import math

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "data" # set dic where uploaded files will be stored
app.config["ALLOWED_EXTENSIONS"] = {"csv"} # saftly filter for csv files

#check if the extension exists if yes is it csv 
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def clean_df(df): # lowercase removes space and etc and maps common synonyms 
    df.columns = [c.strip().lower() for c in df.columns]
    if "long" in df.columns and "lng" not in df.columns:
        df = df.rename(columns={"long": "lng"})
    if "avgsignal" in df.columns and "signal" not in df.columns:
        df = df.rename(columns={"avgsignal": "signal"})
    return df

def load_csv():
    path = "data/cleaned_uploaded.csv"
    if not os.path.exists(path):
        return None
    df = pd.read_csv(path)
    df = clean_df(df)
    return df

def prepare_df(df):
    for col in ["lat", "lng", "signal"]:
        if col not in df.columns:
            df[col] = None
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df["lng"] = pd.to_numeric(df["lng"], errors="coerce")
    df["signal"] = pd.to_numeric(df["signal"], errors="coerce")
    df = df.dropna(subset=["lat", "lng", "signal"]).copy()
    if "radio" not in df.columns:
        df["radio"] = ""
    if "sim" not in df.columns:
        df["sim"] = ""
    return df

def quality_from_signal(x):
    if x >= -79:
        return "Excellent"
    if x >= -89:
        return "Good"
    if x >= -99:
        return "Fair"
    return "Poor"

def dead_zone_cells(df, grid_size=0.01, threshold=-110):
    df = df.copy()
    df["cell_lat"] = (df["lat"] / grid_size).round(0) * grid_size
    df["cell_lng"] = (df["lng"] / grid_size).round(0) * grid_size

    grouped = df.groupby(["cell_lat", "cell_lng"], as_index=False).agg(
        avg_signal=("signal", "mean"),
        points=("signal", "size"),
        radio=("radio", lambda x: x.mode().iloc[0] if not x.mode().empty else ""),
        sim=("sim", lambda x: x.mode().iloc[0] if not x.mode().empty else "")
    )

    grouped["quality"] = grouped["avg_signal"].apply(quality_from_signal)
    dead = grouped[grouped["avg_signal"] < threshold].copy()
    dead["lat"] = dead["cell_lat"]
    dead["lng"] = dead["cell_lng"]
    dead["signal"] = dead["avg_signal"].round(2)
    return dead[["lat", "lng", "signal", "quality", "radio", "sim", "points"]]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if "file" not in request.files:
            return render_template("index.html", error="No file part")
        file = request.files["file"]
        if file.filename == "":
            return render_template("index.html", error="No file selected")
        if file and allowed_file(file.filename):
            os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(save_path)

            df = pd.read_csv(save_path)
            df = clean_df(df)
            df.to_csv("data/cleaned_uploaded.csv", index=False)
        
            return render_template("index.html", success="File uploaded successfully")
        return render_template("index.html", error="Only CSV allowed")
    return render_template("index.html")

@app.route("/api/data")
def api_data():
    df = load_csv()
    if df is None:
        return jsonify([])

    operator = request.args.get("operator", "All")
    mode = request.args.get("mode", "all")

    df = prepare_df(df)

    if operator != "All":
        df = df[df["sim"].astype(str).str.strip().str.lower() == operator.lower()]

    if mode == "dead":
        result = dead_zone_cells(df)
        return jsonify(result.to_dict(orient="records"))

    df["quality"] = df["signal"].apply(quality_from_signal)
    result = df[["lat", "lng", "signal", "quality", "radio", "sim"]].copy()
    return jsonify(result.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)