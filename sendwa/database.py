from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy(engine_options={
    "pool_recycle": 3600
})
migrate = Migrate(db=db)

class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys, required by SQLAlchemy
    nama = db.Column(db.String(1000), nullable=False)
    panggilan = db.Column(db.String(1000), nullable=True)
    kelas = db.Column(db.String(100), nullable=False)
    nomor = db.Column(db.String(100), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        """https://stackoverflow.com/a/11884806"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'<Student {self.nama}>'
