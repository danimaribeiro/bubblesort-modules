# -*- encoding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2014  Danimar Ribeiro 21/05/2014                              #
#                                                                             #
#This program is free software: you can redistribute it and/or modify         #
#it under the terms of the GNU Affero General Public License as published by  #
#the Free Software Foundation, either version 3 of the License, or            #
#(at your option) any later version.                                          #
#                                                                             #
#This program is distributed in the hope that it will be useful,              #
#but WITHOUT ANY WARRANTY; without even the implied warranty of               #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
#GNU Affero General Public License for more details.                          #
#                                                                             #
#You should have received a copy of the GNU Affero General Public License     #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.        #
###############################################################################
{
    "name": "Customizações para modelo SAAS",
    "version": "1.0",    
    "author": "Danimar Ribeiro",
    'category': 'Bubblesort',
    'license': 'AGPL-3',
    'website': 'http://www.bubblesort.com.br',
    "description": "Implementa várias customizações necessárias para rodar o openerp com segurança em modelo SAAS",
    'depends': [
        'base'
    ],
    "init_xml": [],
    'update_xml': ['res_config_view.xml'],
    'demo_xml': [],
    'installable': True,
    'active': False,
}