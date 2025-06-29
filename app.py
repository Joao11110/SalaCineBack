from flask import Flask, jsonify
from Model.Connect import initialize_db
from View.FilmeView import filme_bp
from View.SalaView import sala_bp
from View.SessaoView import sessao_bp

app = Flask(__name__)

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
            "sessoes": "/api/sessoes"
        },
        "uso": "Use os endpoints acima para interagir com a API."
    })

initialize_db()

if __name__ == '__main__':
    app.run(debug=True)