from flask import Flask, render_template
import folium
import requests
import time

app = Flask(__name__)

@app.route('/')
def index():
    TOMTOM_API_KEY = "YROIDXIDz8bIxMtnoKHhn5AenBATS7NU"

    # Define multiple routes
    routes = [
        {"name": "Coimbatore to Salem", "start": "11.0168,76.9558", "end": "11.6643,78.1460"},
        {"name": "Navi Mumbai to Pune","start": "19.0368,73.0158","end":   "18.5196,73.8554"},
        {"name": "Hubli to Chitradurga","start": "15.36, 75.12","end":   "14.23, 76.40"},
        {"name": "surat to vadodara","start": "21.1702,72.8311","end": "22.3072	73.1812"},
        {"name": "Mumbai to Nashik","start": "19.0760,72.8777","end": "19.9975,73.7898"}
    ]

    m = folium.Map(location=[11.3, 77.2], zoom_start=8)

    for route in routes:
        route_url = (
            f"https://api.tomtom.com/routing/1/calculateRoute/{route['start']}:{route['end']}/json"
            f"?key={TOMTOM_API_KEY}&routeType=fastest&traffic=false"
        )
        response = requests.get(route_url)
        data = response.json()
        route_coords = data['routes'][0]['legs'][0]['points']
        truck_route = [(pt['latitude'], pt['longitude']) for pt in route_coords]
        folium.PolyLine(truck_route, color='red', weight=4, tooltip=route['name']).add_to(m)
        time.sleep(0.2)

    # Substations
    substations = [
        {"name": "Arasur AIS", "lat": 11.1269, "lon": 77.1929, "voltage": "400/220 kV"},
        {"name": "K. Paramathi", "lat": 11.0398, "lon": 77.7583, "voltage": "110/33 kV"},
        {"name": "Salem AIS", "lat": 11.6643, "lon": 78.1460, "voltage": "400/220 kV"},
        {"name": "Pugalur HVDC", "lat": 10.9500, "lon": 77.9500, "voltage": "HVDC"},
        {"name": "Dharmapuri AIS", "lat": 11.7600, "lon": 78.1600, "voltage": "400/220 kV"},
        {"name": "Periyakodivery", "lat": 11.5000, "lon": 77.8000, "voltage": "110/33 kV"},
        {"name": "Nagapattinam(PGCIL)", "lat": 10.961668, "lon": 77.3126364, "voltage": "400/220 kV"},

        # NAVI MUMBAI TO PUNE
        {"name": "Kalamboli MSEB Substation", "lat": 19.0007, "lon": 73.1232, "voltage": "400/220 kV"},
        {"name": "Khopoli MIDC Grid Area", "lat": 18.7639, "lon": 73.3406, "voltage": "110/33 kV"},
        {"name": "Talegaon Industrial Substation", "lat": 18.7380, "lon": 73.6820, "voltage": "400/220 kV"},
        {"name": "Chakan MIDC Power Grid", "lat": 18.7550, "lon": 73.8470, "voltage": "400/220 kV"},
        {"name": "Pimpri Chinchwad MSEDCL Substation", "lat": 18.6257, "lon": 73.8149, "voltage": "400/220 kV"},
         #Hubli to Chitradurga
        {"name": " Substation", "lat": 15.1631,  "lon": 75.1447, "voltage": "400/220 kV"},
         {"name": " Substation", "lat": 14.3919,  "lon": 76.0674, "voltage": "400/220 kV"},
         {"name": " Substation", "lat": 14.6103,  "lon": 75.6243, "voltage": "400/220 kV"},
         {"name": " Substation", "lat": 14.8009,  "lon": 75.3903, "voltage": "400/220 kV"},
         {"name": " Substation", "lat": 14.2654,  "lon": 76.3355, "voltage": "400/220 kV"},
        #surat to vadodara
        {"name": "Palsana GETCO Substation", "lat": 21.2085, "lon": 72.9282, "voltage": "220kV"},
        {"name": "Vav GETCO Substation (Bharuch)", "lat": 21.6952, "lon": 73.0562, "voltage": "220kV"},
        #Mumbai to Nashik
         {"name": "Ghoti Budruk", "lat": 19.7050, "lon": 73.6240, "voltage": "132 kV"},
         {"name": "Igatpuri", "lat": 19.6960, "lon": 73.5610, "voltage": "220 kV"},
         {"name": "Shahapur Outskirts", "lat": 19.4650, "lon": 73.3350, "voltage": "132 kV"}
        
    ]
    for s in substations:
        folium.Marker([s["lat"], s["lon"]],
                      popup=f"{s['name']} ({s['voltage']})",
                      icon=folium.Icon(color='blue', icon='bolt', prefix='fa')).add_to(m)

    # Renewables
    renewables = [
        {"name": "Kayathar Wind Farm Zone", "lat": 10.957, "lon": 77.341, "type": "Wind"},
        {"name": "Sankarankoil Solar Park", "lat": 10.957, "lon": 77.892, "type": "Solar"},
        {"name": "ARS Solar Power Plant", "lat": 11.2645, "lon": 77.0547, "type": "Solar"},
        {"name": "M/S.JLV WIND POWER", "lat": 10.8088, "lon": 77.2028, "type": "Wind"},
        {"name": "Zf Wind Power Coimbatore Private Limited", "lat": 11.1317, "lon": 77.1785, "type": "Wind"},
        {"name": "SWELECT HHV Solar Photovoltaics Pvt. Ltd.", "lat": 11.1430, "lon":  77.0050, "type": "Solar"},
        {"name": "VC Green Energy", "lat": 10.875476, "lon": 77.1620733, "type": "Solar"},
        #Hubli to Chitradurga 
        {"name": " Mayakonda ", "lat":14.321773,  "lon": 76.111559, "type": "Solar"},
         {"name": "Unnamed Solar station", "lat": 14.341453, "lon": 76.398584, "type": "Solar"},
        #surat to vadodara
        {"name": "NTPC Kawas Solar & Gas Plant", "lat": 21.0905, "lon": 72.7118, "type": "Solar + Gas"},
        {"name": "Vahelam Solar Park", "lat": 21.7941, "lon": 73.2175, "type": "Solar"},
        #Mumbai to Nashik
        {"name": "Mumbai (Solar project IX)", "lat": 19.1650, "lon":72.9212, "type":"Solar"},
        {"name": "Igatpuri Taluka Solar Project", "lat": 19.7878, "lon":73.6599, "type":"Solar"},
        {"name": "Nashik Taluka Solar Project", "lat": 19.9937, "lon":73.7221, "type":"Solar"}
    ]
    for r in renewables:
        icon_color = 'orange' if r["type"] == "Solar" else 'purple'
        folium.Marker([r["lat"], r["lon"]],
                      popup=f"{r['name']} ({r['type']})",
                      icon=folium.Icon(color=icon_color, icon='sun' if r["type"] == "Solar" else 'leaf', prefix='fa')).add_to(m)

    # Charging Stations
    charging_sites = [
        {"name": "Arasur - Near Industrial Belt", "lat": 11.1269, "lon": 77.1929, "reason": "400kV substation + industrial zone", "distance_km": 0.0},
        {"name": "Tiruppur Region", "lat": 11.1075, "lon": 77.3411, "reason": "Textile hub, heavy truck traffic", "distance_km": 0.0},
        {"name": "Erode Bypass - Periyakodivery", "lat": 11.5000, "lon": 77.8000, "reason": "Central point, grid availability", "distance_km": 0.0},
        {"name": "Salem Entry (Salem AIS)", "lat": 11.6643, "lon": 78.1460, "reason": "City entry, logistics hub", "distance_km": 0.0},
        {"name": "Pugalur (Multi-grid Area)", "lat": 10.95, "lon": 77.95, "reason": "400kV AIS/GIS/HVDC grid cluster", "distance_km": 13.2},
        {"name": "Salem Steel Plant", "lat": 11.6490, "lon": 78.1830, "reason": "Heavy industrial activity", "distance_km": 4.07},
        {"name": "SWELECT HHV Solar station", "lat": 11.1520, "lon": 77.0140, "reason": "Reputed solar manufacturing", "distance_km": 6.84},
        {"name": "VC Green Energy", "lat": 11.0337, "lon": 76.9070, "reason": "Solar-powered site ", "distance_km": 6.38},
        #Hubli to Chitradurga 
        {"name": "Anagodu", "lat": 14.391918, "lon": 76.067372 , "reason": "Solar-powered site ", "distance_km": 1.7},
        {"name": "Varur", "lat": 15.2159,  "lon": 75.1479 , "reason": "VRL logistics is nearer  ", "distance_km": 1.2},
        {"name": "Kamadod", "lat": 14.5700,  "lon": 75.6902 , "reason": "Industrial area", "distance_km": 1.5},
        {"name": "Haveri ", "lat": 14.8392,  "lon": 75.3547 , "reason": "Beside High way", "distance_km": 0.2},
        {"name": "Chitradurga ", "lat": 14.2654, "lon": 76.3355 , "reason": "Beside highway ", "distance_km": 0.7},
        #surat to vadodara
        {"name": "Palsana Charging Station", "lat": 21.1848, "lon": 72.9196, "voltage": "350kW + 180kW"},
        {"name": "Bharuch Charging Station", "lat": 21.6945, "lon": 72.9985, "voltage": "350kW + 180kW"},
        #Mumbai to Nashik
        {"name": "Gonde Industrial Area","lat":19.9130, "lon": 73.7010, "reason": "Industrial Zone", "distance_km": 0.9},
        {"name": "Kasara Entry Point","lat":19.6480, "lon": 73.5480, "reason": "supportive resting point", "distance_km": 0.9},
        {"name": "Khadavli Bridge","lat":19.4250, "lon": 73.3000, "reason": "Beside high way", "distance_km": 1.0}

    ]
    for c in charging_sites:
        distance_info = f"Distance from route: {c.get('distance_km')} km" if "distance_km" in c else ""
        popup_text = f"{c['name']}<br>{c['reason']}<br>{distance_info}"
        folium.Marker(
            [c["lat"], c["lon"]],
            popup=popup_text,
            icon=folium.Icon(color='green', icon='charging-station', prefix='fa')
        ).add_to(m)

    # Industries
    industries = [
        {"name": "IndoSpace Coimbatore", "lat": 10.905, "lon": 77.090},
        {"name": "Tiruppur Textile Cluster", "lat": 11.1075, "lon": 77.3411},
        {"name": "Perumanallur Industrial Park", "lat": 11.152, "lon": 77.397},
        {"name": "SIDCO Veerapandi, Salem", "lat": 11.635, "lon": 78.070},
        {"name": "Salem Steel Plant", "lat": 11.640, "lon": 78.174},
        {"name": "Mettur Industrial Area", "lat": 11.786, "lon": 77.800},
        {"name": "Sangagiri Transport Hub", "lat": 11.478, "lon": 77.872}
    ]
    for ind in industries:
        folium.Marker([ind["lat"], ind["lon"]],
                      popup=ind["name"],
                      icon=folium.Icon(color='red', icon='industry', prefix='fa')).add_to(m)

    etruck_info = {
        "title": "About Electric Trucks",
        "summary": (
            "Electric trucks (e-trucks) are commercial vehicles powered by electric motors and batteries instead of diesel engines. "
            "They offer zero tailpipe emissions, lower noise, and reduced operating costs. "
            "Modern e-trucks can cover 100–500 km per charge, support fast charging, and are ideal for urban and regional logistics. "
            "Adoption is growing rapidly due to environmental benefits and improved technology, though challenges remain with charging infrastructure and initial costs."
        ),
        "features": [
            "Zero tailpipe emissions, reducing air pollution and greenhouse gases.",
            "Lower operating and maintenance costs due to fewer moving parts.",
            "Smooth, quiet operation—ideal for urban and regional deliveries.",
            "Range: 70–560 km per charge, depending on model and battery size.",
            "Fast charging: 90–120 minutes for a full charge with high-power DC chargers."
        ]
    }

    return render_template(
        'index.html',
        map=m._repr_html_(),
        charging=charging_sites,
        substations=substations,
        renewables=renewables,
        industries=industries,
        etruck_info=etruck_info,
    )

if __name__ == '__main__':
    app.run(debug=True)
