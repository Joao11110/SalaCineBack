from flask import Flask, jsonify
from flask_cors import CORS
from flask.json.provider import DefaultJSONProvider

from Model.Connect import initialize_db
from View.FilmeView import filme_bp
from View.SalaView import sala_bp
from View.SessaoView import sessao_bp

class CustomJSONProvider(DefaultJSONProvider):
    def __init__(self, app):
        super().__init__(app)
        self.ensure_ascii = False

app = Flask(__name__)
app.json = CustomJSONProvider(app)
CORS(app)

app.register_blueprint(filme_bp, url_prefix='/api')
app.register_blueprint(sala_bp, url_prefix='/api')
app.register_blueprint(sessao_bp, url_prefix='/api')

@app.route('/')
def home():
    return jsonify({
        "message": "A API do SalaCine esta funcionando!",
        "endpoints": {
            "filmes": "/api/filmes",
            "salas": "/api/salas",
            "sessoes": "/api/sessoes",
            "generos": "/api/generos",
            "poster": "/api/filmes/<int:id_filme>/poster"
        },
        "uso": "Use os endpoints acima para interagir com a API."
    })

initialize_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)