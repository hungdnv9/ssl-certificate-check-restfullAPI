from SSLCertificateCheck.utils.ssl_get import Certificate
from datetime import datetime
import logging
from SSLCertificateCheck import db
from SSLCertificateCheck.models import Domain
logger = logging.getLogger(__name__)


def worker_list_and_update_domain(domain):
    '''
    Return a dictionary, also update the domain database
    '''
    result = {
        'id': domain.id,
        'domain_name': domain.domain_name,
        'notbefore': domain.notbefore,
        'notafter': domain.notafter,
        'remaining': domain.remaining,
        'last_checked': domain.last_checked              
    }
    logger.debug(domain)
    dom = Certificate(domain.domain_name)
    domain.notbefore = dom.notBefore()
    domain.notafter = dom.notAfter()
    domain.remaining = dom.remaining()
    domain.last_checked = datetime.utcnow()    
    logger.debug(domain)

    return result