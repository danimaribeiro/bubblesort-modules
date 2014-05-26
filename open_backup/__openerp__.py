{
    "name": "OpenDB Backup",
    "version": "1.0",    
    "author": "Danimar Ribeiro",
    "category": "Tools",
    "description": """
    Este módulo permite configurar backup das bases de dados para rodar periodicamente
    """,
    "depends": ["base", "server_manager"],    
    'update_xml': ["open_backup.xml"],
    'data':["security/ir.model.access.csv"],    
    'installable': True,
    'active': False,
}