#coding=utf-8
from openerp.osv import osv, fields
import uuid

class licence_software(osv.Model):
    _name = 'licence.software'
    _columns = {
        'licence_key':fields.char('Chave licença', size=100),
        'state':fields.selection(
            [('not_used', u'Não usada'), ('in_use', 'Em uso'),
            ('cancelled', u'Cancelada')], 'Status', required=True),
        'partner_id': fields.many2one('res.partner', 'Cliente', required=False,
            help='O cliente a qual a licença está vinculada.'),
        'issued_date': fields.datetime('Data inicio uso'),
        'expiry_date':fields.datetime('Data final uso'),
        'max_users': fields.integer('Número máximo de usuários'),
    }
    _defaults = {
         'licence_key' : lambda *x: str(uuid.uuid4()),
         'state':'not_used',
         'max_users':3,
        }
    
licence_software()