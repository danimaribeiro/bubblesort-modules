#coding=utf-8
'''
Created on 20/04/2013

@author: danimar
'''
import datetime
from openerp.osv import osv, fields
from openerp.osv import orm
from openerp.tools.translate import _


class res_users(osv.Model):
    _inherit = 'res.users'
    _columns = {      
            }
    
    def signup(self, cr, uid, values, token=None, context=None):
        created_user = super(res_users, self).signup(cr, uid, values, token, context)
        #TODO Pegar os valores e modificar o que é necessario
        if not values["licence_key"]:
            raise osv.except_osv(_('Warning !'), ("Chave da licença é obrigatório"))
        if not values["company_name"]:
            raise osv.except_osv(_('Warning !'), ("Nome da empresa é obrigatório"))
        licence_pool = self.pool.get('licence.software')
        licence_ids = licence_pool.search(cr, uid, [('licence_key','=',values['licence_key'])])
        if len(licence_ids) > 0:
            licence = licence_pool.browse(cr, uid, licence_ids[0], context)
            if licence.state != 'not_used':
                raise orm.except_orm(_('Error !'), ("Desculpe mas a licença já está em uso ou foi cancelada. Caso você comprou esta licença ligue para nós que resolveremos o seu problema."))
            
            user_ids = self.search(cr, uid, ['&',('login','=',created_user[1]),('password','=',created_user[2])])
            if user_ids:
                user = self.browse(cr, uid, user_ids[0], context)
                
                self.write(cr, uid, user_ids, {'customer':1, 'is_new':1, 'subdomain': values["company_name"]}, context)   
                licence_pool.write(cr, uid, licence_ids, {'state':'in_use', 'partner_id':user.partner_id.id,
                    'issued_date':datetime.datetime.today(),'expiry_date': datetime.datetime.today() + datetime.timedelta(days=365) }, context)         
                
                self._setup_environment(cr, uid, values, user, context)
            else:
                raise osv.except_osv(_('Warning !'), ("Erro ao criar o usuário"))
        else:
            raise osv.except_osv(_('Warning !'), ("A licença não é válida"))
        return created_user
    
    def _setup_environment(self, cr, uid, values, user , context=None):
        manager_pool = self.pool.get('server.subdomain')
        config_pool = self.pool.get('server.config.settings')
        config_ids = config_pool.search(cr, uid, [])
        if len(config_ids)>0:
            config = config_pool.browse(cr, uid, config_ids[0], context)
            
            values_insert = {'subdomain':user.subdomain, 'base_database_id': config.default_database_template_id.id,
                'default_server_id':config.default_server_id.id, 'partner_id': user.partner_id.id}        
            id_manager = manager_pool.create(cr, uid, values_insert , context)
            server = manager_pool.browse(cr, uid, id_manager, context)
            server.create_subdomain()
            server.duplicate_database()
            
            context = { "subdomain_id": id_manager }
            self.pool.get('email.template').send_mail(cr, uid, config.default_email_template.id, user.id, force_send=True, context=context)
            
        else:
            raise osv.except_osv(_('Warning !'), ("Desculpe nossa falha, ainda estamos configurando nosso sistema."))
        
    
    
    def get_signup_url(self,cr, uid, values, context=None):
        subdomain_pool = self.pool.get('server.subdomain')        
        subdomain = subdomain_pool.browse(cr, uid, context["subdomain_id"])
        if not subdomain is None:            
            return "http://" + subdomain.subdomain + "." + subdomain.default_server_id.url_server 
        else:        
            return "http://admin.emissaocte.com.br"
    
res_users()


class res_partner(osv.Model):
    _inherit = 'res.partner'
    _columns = {
        'is_new':fields.boolean("Cliente novo?"), 
        'subdomain':fields.char('Subdominio', size=50)         
    }
    _defaults = {
        'is_new':1,
    }