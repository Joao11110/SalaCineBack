from flask import Flask
from Model.BD import initialize_db
from View.FilmeView import filme_bp
from View.SalaView import sala_bp
from View.SessaoView import sessao_bp

app = Flask(__name__)

app.register_blueprint(filme_bp, url_prefix='/api')
app.register_blueprint(sala_bp, url_prefix='/api')
app.register_blueprint(sessao_bp, url_prefix='/api')

@app.before_request
def before_request():
    if not hasattr(app, 'db_initialized'):
        initialize_db()
        app.db_initialized = True

if __name__ == '__main__':
    app.run(debug=True)