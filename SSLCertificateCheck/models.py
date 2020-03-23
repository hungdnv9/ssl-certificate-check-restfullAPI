from SSLCertificateCheck import db
from datetime import datetime

class Domain(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain_name = db.Column(db.String(20), nullable=False)
    notbefore = db.Column(db.String(20), nullable=True)
    notafter = db.Column(db.String(20), nullable=True)
    remaining = db.Column(db.Integer, nullable=True)
    last_checked = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Domain('{self.domain_name}', '{self.notbeforce}', '{self.notaffter}', '{self.remaining}')"