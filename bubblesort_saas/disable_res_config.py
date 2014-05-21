'''
Created on May 21, 2014

@author: danimar
'''
from lxml import etree
from openerp.osv import osv

class disable_res_config(osv.osv_memory):
    _inherit = 'res.config.settings'    
    _columns = {}
    
    def _get_classified_fields(self, cr, uid, context=None):
        classifieds = super(disable_res_config, self)._get_classified_fields(cr, uid, context)
        classifieds['module'] = []
        return classifieds
    
    
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False): 

        if context is None: context={}     
        res = super(disable_res_config, self).fields_view_get(cr, uid, view_id=view_id, view_type=view_type, context=context, toolbar=toolbar, submenu=submenu) 
            
        if view_type=='form': 
            doc = etree.XML(res['arch']) 
            for node in doc.xpath("//field[starts-with(@name, 'module_')]"):                   
                field_name = node.attrib['name']   
                node.set('modifiers', '{"invisible":[[ "' + field_name + '", "!=", 0]]}')
            for node in doc.xpath("//label[starts-with(@for, 'module_')]"):                    
                field_name = node.attrib['for']   
                node.set('modifiers', '{"invisible":[[ "' + field_name + '", "!=", 0]]}')               
            res['arch'] = etree.tostring(doc)            
        return res
    
disable_res_config()