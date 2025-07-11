from peewee import (
    AutoField,
    CharField,
    IntegerField,
    ForeignKeyField,
    BlobField,
    CompositeKey,
    ManyToManyField
)

from Model.BaseModel import BaseModel

class Genero(BaseModel):
    id_genero = AutoField(primary_key=True,)
    nome = CharField(max_length=50, unique=True)

class Filme(BaseModel):
    id_filme = AutoField(primary_key=True)
    titulo = CharField(max_length=150)
    duracao = IntegerField()
    classificacao = IntegerField()
    diretor = CharField(max_length=150)
    poster_blob = BlobField(null=True)
    poster_mime_type = CharField(max_length=50, null=True)

    def generos(self):
        return (Genero
                .select()
                .join(FilmeGenero, on=(Genero.id_genero == FilmeGenero.genero_id))
                .where(FilmeGenero.filme_id == self.id_filme))

    @classmethod
    def create(cls, titulo, duracao, classificacao, diretor, generos=None, poster_blob=None, poster_mime_type=None):
        # Primeiro cria o filme
        filme = super().create(
            titulo=titulo,
            duracao=duracao,
            classificacao=classificacao,
            diretor=diretor,
            poster_blob=poster_blob,
            poster_mime_type=poster_mime_type
        )
        
        # Depois adiciona os gêneros se foram fornecidos
        if generos:
            if isinstance(generos, str):
                generos = [generos]
            
            for genero_nome in generos:
                genero, _ = Genero.get_or_create(nome=genero_nome)
                FilmeGenero.create(filme=filme, genero=genero)
        
        return filme

    @classmethod
    def readByTitulo(cls, titulo):
        return cls.select().where(cls.titulo.contains(titulo))

    @classmethod
    def update(cls, id_filme, **kwargs):
        query = cls.update(**kwargs).where(cls.id_filme == id_filme)
        return query.execute()

    @classmethod
    def delete(cls, id_filme):
        # Primeiro deleta as relações com gêneros
        FilmeGenero.delete().where(FilmeGenero.filme == id_filme).execute()
        # Depois deleta o filme
        return cls.delete().where(cls.id_filme == id_filme).execute()

    def getPosterUrl(self):
        if self.poster_blob:
            return f"/api/filmes/{self.id_filme}/poster"
        return None

    def getIdFilme(self):
        return self.id_filme

class FilmeGenero(BaseModel):
    filme = ForeignKeyField(Filme, field=Filme.id_filme, backref='generos_link')
    genero = ForeignKeyField(Genero, field=Genero.id_genero, backref='filmes_link')

    class Meta:
        primary_key = CompositeKey('filme', 'genero')