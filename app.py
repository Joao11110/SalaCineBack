from flask.json.provider import DefaultJSONProvider
from flask import Flask, jsonify
from flask_cors import CORS

from Model.Connect import initializeDB
from View.SessaoView import sessao_bp
from View.FilmeView import filme_bp
from View.SalaView import sala_bp

class CustomJSONProvider(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)
        self.ensure_ascii = False

app = Flask(__name__)
app.json = CustomJSONProvider(app)
CORS(app)

app.register_blueprint(filme_bp,  url_prefix='/api')
app.register_blueprint(sala_bp,   url_prefix='/api')
app.register_blueprint(sessao_bp, url_prefix='/api')
initializeDB()

@app.route('/')
def home():
    return jsonify({
        "message": "A API do SalaCine esta funcionando!",
        "endpoints": {
            "filmes ": "/api/filmes",
            "sessoes": "/api/sessoes",
            "salas  ": "/api/salas",
            "generos": "/api/generos",
            "poster ": "/api/filmes/<int:id_filme>/poster"
        },
        "usage": "Use os endpoints acima para interagir com a API."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)