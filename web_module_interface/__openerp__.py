# __openerp__.py
# Danimar Ribeiro
{
    'name': "Customizacao Interface",
    'description': "Customizacao da interface do openerp",
    "version": "1.0",    
    "author": "Danimar Ribeiro",
    'category': 'Bubblesort',
    'license': 'AGPL-3',
    'website': 'http://www.bubblesort.com.br',
    'depends': ['web'],
    'js': ['static/src/js/first_module.js'],
    'css': ['static/src/css/openerp_overrides.css'],
    'active':False,
    'auto_install':False,
}