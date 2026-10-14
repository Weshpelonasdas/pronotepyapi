import pronotepy
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/pronote', methods=['POST'])
def get_pronote():
    data = request.json
    try:
        # Connexion gérée proprement par pronotepy (plus d'erreur G=8 !)
        client = pronotepy.Client(data['url'], username=data['username'], password=data['password'])
        
        # Récupération des notes et devoirs
        notes = [{"matiere": n.subject.name, "note": n.grade, "sur": n.out_of} for n in client.current_period.grades]
        devoirs = [{"date": d.date.strftime("%Y-%m-%d"), "matiere": d.subject.name, "travail": d.text} for d in client.homework]
        
        return jsonify({
            "success": True,
            "nom": client.info.name,
            "moyenne": client.current_period.general_average,
            "notes": notes,
            "devoirs": devoirs
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
