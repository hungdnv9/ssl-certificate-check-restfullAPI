from flask import request, url_for, abort, redirect
from flask_api import status
from SSLCertificateCheck import app, db
from SSLCertificateCheck.utils.ssl_get import Certificate
from SSLCertificateCheck.models import Domain
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@app.route("/api/v1/domains/", methods=['GET', 'POST'])
def domains_list():
    if request.method == 'POST':
        domain_name = str(request.data.get('domain_name',''))       
        d = Certificate(domain_name)
        notbefore = d.notBefore()
        notafter = d.notAfter()
        remaining = d.remaining()

        domain = Domain(domain_name=domain_name, notbefore=notbefore, notafter=notafter, 
                        remaining=remaining)
        db.session.add(domain)
        try:
            db.session.commit()
            logger.debug(f'Commit database done, domain {domain_name}')
        except Exception as err:
            logger.debug(f'Commit database error, reason {err}')

        

    # request.method == 'GET'
    result = [] 
    domains = Domain.query.all()
    if len(domains) == 0:
        return {"Error": "Not have data"}

    for domain in domains:
        result.append(
            {
                'id': domain.id,
                'domain_name': domain.domain_name,
                'notbefore': domain.notbefore,
                'notafter': domain.notafter,
                'remaining': domain.remaining,
                'last_checked': domain.last_checked              
            }
        )
        # Update Database
        d = Certificate(domain.domain_name)        
        domain.notbefore = d.notBefore()
        domain.notafter = d.notAfter()
        domain.remaining = d.remaining()
        domain.last_checked = datetime.utcnow()
        try:
            db.session.commit()
            logger.debug(f'Update domain infomation done, site: {domain.domain_name}')                
        except Exception as err:            
            logger.debug(f'Update database error, reason {err}')

    return  result

@app.route('/api/v1/domains/<int:id>/', methods=['PUT', 'GET', 'DELETE'])
def domains_detail(id):
    domain = Domain.query.get(id)
    if domain:
        if request.method == 'PUT':
            domain.domain_name = str(request.data.get('domain_name',''))            
            db.session.commit()

        elif request.method == 'DELETE':
            db.session.delete(domain)
            db.session.commit()
            return '', status.HTTP_204_NO_CONTENT

        return {
                'id': domain.id,
                'domain_name': domain.domain_name,
                'notbefore': domain.notbefore,
                'notafter': domain.notafter,
                'remaining': domain.remaining,
                'last_checked': domain.last_checked              
            }
    else:
        abort(404)

@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('domains_list'))