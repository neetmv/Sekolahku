from flask import Flask, request, jsonify, render_template
from scipy.spatial import KDTree
from math import radians, cos, sin, sqrt, atan2
import pandas as pd
import os

app = Flask(__name__)

# Fungsi jarak Haversine dalam km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius bumi dalam km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

@app.route("/")
def index():
    sekolah = []
    if os.path.exists("school_data.csv"):
        df = pd.read_csv("school_data.csv")
        sekolah = df.to_dict(orient="records")
    return render_template("landing.html", sekolah=sekolah)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/cari_sekolah")
def cari_sekolah():
    lat = float(request.args.get("lat"))
    lon = float(request.args.get("lon"))
    radius = float(request.args.get("radius"))

    df = pd.read_csv("school_data.csv")
    coords = df[["lat", "lon"]].to_numpy()
    tree = KDTree(coords)

    distances, indices = tree.query([lat, lon], k=len(df))
    hasil = []

    for i, dist in zip(indices, distances):
        row = df.iloc[i]
        jarak = haversine(lat, lon, row["lat"], row["lon"])
        if jarak <= radius:
            hasil.append({
                "nama": row["nama"],
                "alamat": row["alamat"],
                "lat": row["lat"],
                "lon": row["lon"],
                "gambar": row["gambar"],
                "akreditasi": row["akreditasi"],
                "deskripsi": row["deskripsi"],
                "jarak_km": round(jarak, 2)
            })

    return jsonify(hasil)

@app.route("/bookmark")
def bookmark():
    return render_template("bookmark.html")

if __name__ == "__main__":
    app.run(debug=True)
