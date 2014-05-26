#coding=utf-8
from openerp.osv import fields,osv
import xmlrpclib
import socket

def execute(connector, method, *args):
    res = False
    try:        
        res = getattr(connector,method)(*args)
    except socket.error,e:        
            raise e
    return res

class server_location(osv.Model):
    _description = 'Locais Servidores'
    _name = 'server.location'
    _rec_name = 'description'
    _columns = {
            'description':fields.char(u'Descrição', size=100, required=True),
            'url_server':fields.char('Url Servidor', size=100, required=True),                        
    }

server_location()

class database_template(osv.Model):
    _description = 'Templates de banco'
    _name = 'database.template'
    _rec_name = 'description'
    _columns = {
            'description':fields.char(u'Descrição', size=100, required=True),
            'template':fields.char('Banco de dados de template', size=100, required=True),   
    }

database_template()

class server_subdomain(osv.Model):
    _description = 'Subdominios'
    _name = 'server.subdomain'
    _rec_name = 'subdomain'
    _columns = {        
        'subdomain':fields.char('Empresa',size=30),
        'base_database_id': fields.many2one('database.template', 'Template Banco de dados',
              required=True),
        'base_database': fields.related('base_database_id', 'description', type='char', string='Template'),
        'default_server_id':fields.many2one('server.location', 'Servidor Default', required=True),
        'default_server': fields.related('default_server_id', 'description', type='char', string='Servidor'),
        'partner_id':fields.many2one('res.partner', 'Cliente', required=True),
        'customer': fields.related('partner_id', 'name', type='char', string='Cliente'),                 
    }
    
    def duplicate_database(self, cr, uid, ids, context=None):
        item = self.browse(cr, uid, ids[0], context)
        uri = 'http://localhost:8069' 
        conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
        retorno = execute(conn, 'duplicate_database', 'admin', item.base_database_id.template, item.subdomain)
        print retorno
        return True
    
server_subdomain()


class server_settings(osv.osv_memory):
    _description = u'Configurações gerenciamento servidores'
    _name = 'server.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
        'zerigo_email_api':fields.char('Zerigo Email API', size=50, help="Email de acesso a API do Zerigo DNS", required=True),
        'zerigo_dns_key': fields.char('Zerigo DNS Key',size=30, help="Chave de acesso a API do Zerigo DNS Service", required=True),
        'default_database_template_id': fields.many2one('database.template', 'Template Default Banco de dados',
                            required=True), 
        'default_server_id':fields.many2one('server.location', 'Servidor Default', required=True),
        'default_email_template':fields.many2one('email.template', 'Email Default', required=False),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        ids = self.search(cr, uid, [])
        values = self.browse(cr, uid, ids, context)
        val = {}
        if len(values)>0:
            val["zerigo_email_api"] = values[0].zerigo_email_api
            val["zerigo_dns_key"] = values[0].zerigo_dns_key
            val["default_database_template_id"] = values[0].default_database_template_id.id
            val["default_server_id"] = values[0].default_server_id.id
            val["default_email_template"] = values[0].default_email_template.id
            
        return val
    
    def create(self, cr, uid, vals, context=None):
        ids = self.search(cr, uid, [])
        if len(ids)>0:
            self.write(cr, uid, ids[0], vals, context)
            return ids[0]
        else:
            return super(server_settings,self).create(cr, uid, vals, context)        

server_settings()
