from flask import Flask
from Model.Connect import initialize_db
from View.FilmeView import filme_bp
from View.SalaView import sala_bp
from View.SessaoView import sessao_bp

app = Flask(__name__)

app.register_blueprint(filme_bp, url_prefix='/api')
app.register_blueprint(sala_bp, url_prefix='/api')
app.register_blueprint(sessao_bp, url_prefix='/api')

initialize_db()
if __name__ == '__main__':
    app.run(debug=True)