from flask import request, url_for, abort, redirect
from flask_api import status
from SSLCertificateCheck import app, db
from SSLCertificateCheck.utils.ssl_get import Certificate
from SSLCertificateCheck.utils.workers import worker_list_and_update_domain

from SSLCertificateCheck.models import Domain
from datetime import datetime
import logging
import concurrent.futures

logger = logging.getLogger(__name__)



@app.route("/api/v1/domains/", methods=['GET', 'POST', 'DELETE'])
def domains_list():
    if request.method == 'POST':
        try:
            if str(request.data.get('domain_name','')):
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
                    return  {
                        "domain_name": domain_name,
                        "notbefore": notbefore,
                        "notafter": notafter,
                        "remaining": remaining,
                        "last_checked": datetime.utcnow(),
                        "status": "success"
                        }
                except Exception as err:
                    logger.debug(f'Commit database error, reason {err}')
            else:
                return {
                    "status": "error",
                    "exception": f"key error {[ key for key in request.data.keys()]}"
                }
        except Exception as err:
            return {
                "status": "error",
                "exception": str(err)
            }

    elif request.method == 'DELETE':
        Domain.query.delete()
        db.session.commit()        

    # request.method == 'GET'
    domains = Domain.query.all()
    result_base = [
        {
            "Descritions": "Garther the SSL Certificate infomation!",
            "Total domains": len(domains),
            "Result": [],
        }
    ]
    if len(domains) == 0:
        return result_base
    else:
        # List and Update Database
        ''' without threading
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
            dom = Certificate(domain.domain_name)
            domain.notbefore = dom.notBefore()
            domain.notafter = dom.notAfter()
            domain.remaining = 23232323
            domain.last_checked = datetime.utcnow()
            logger.debug(domain)
            db.session.commit()
        '''

        domain_result = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(worker_list_and_update_domain, domain): domain for domain in domains}
            for future in concurrent.futures.as_completed(future_to_url):
                dom = future_to_url[future]
                try:
                    data = future.result()
                    domain_result.append(data)               
                except Exception as exc:
                    logger.debug(f'{dom} generated an exception: {exc}')    
        db.session.commit()         
        result_base[0]['Result'] = domain_result

    return  result_base

@app.route('/api/v1/domains/<int:id>/', methods=['PUT', 'GET', 'DELETE'])
def domains_detail(id):
    domain = Domain.query.get(id)
    if domain:
        if request.method == 'PUT':
            try:
                if str(request.data.get('domain_name','')):
                    domain.domain_name = str(request.data.get('domain_name',''))
                    d = Certificate(str(request.data.get('domain_name','')))  
                    domain.notbefore = d.notBefore()
                    domain.notafter = d.notAfter()
                    domain.remaining = d.remaining()
                    domain.last_checked = datetime.now()         
                    db.session.commit()
                else:
                    return {
                        "status": "error",
                        "exception": f"key error {[ key for key in request.data.keys()]}"
                    }
            except Exception as err:
                return {
                    "status": "error",
                    "exception": str(err)
                }

        elif request.method == 'DELETE':
            db.session.delete(domain)
            db.session.commit()
            return '', status.HTTP_204_NO_CONTENT

        # request.method == 'GET'

        result = {
            'id': domain.id,
            'domain_name': domain.domain_name,
            'notbefore': domain.notbefore,
            'notafter': domain.notafter,
            'remaining': domain.remaining,
            'last_checked': domain.last_checked              
        }
        dom = Certificate(domain.domain_name)            
        domain.notbefore = dom.notBefore()
        domain.notafter = dom.notAfter()
        domain.remaining = dom.remaining()
        domain.last_checked = datetime.utcnow()
        db.session.commit()            
        return result
    else:
        return {
            "error": "404"
        }

@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('domains_list'))