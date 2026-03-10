from flask import Flask, jsonify, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

LEAGUE_IDS = {
    "Serie A": 2019,
    "Champions League": 2001,
    "Premier League": 2021,
    "La Liga": 2014,
    "Bundesliga": 2002,
    "Ligue 1": 2015,
    "Europa League": 2146,
    "Eredivisie": 2003,
}

@app.route('/matches')
def get_matches():
    api_key  = request.args.get('apiKey')
    comp     = request.args.get('comp')
    data_da  = request.args.get('dataDa')
    data_a   = request.args.get('dataA')

    if not all([api_key, comp, data_da, data_a]):
        return jsonify({'error': 'Parametri mancanti'}), 400

    if comp == 'TUTTO':
        da_cercare = list(LEAGUE_IDS.items())
    else:
        lid = LEAGUE_IDS.get(comp)
        if not lid:
            return jsonify({'error': 'Competizione non trovata'}), 400
        da_cercare = [(comp, lid)]

    risultati = {}
    for nome, lid in da_cercare:
        url = f"https://api.football-data.org/v4/competitions/{lid}/matches"
        headers = {"X-Auth-Token": api_key}
        params  = {"dateFrom": data_da, "dateTo": data_a, "status": "SCHEDULED,LIVE,FINISHED"}
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            matches = res.json().get("matches", [])
            if matches:
                risultati[nome] = matches

    return jsonify(risultati)

if __name__ == '__main__':
    app.run()

