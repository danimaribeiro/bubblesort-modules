#coding=utf-8
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields,osv
import xmlrpclib
import socket
import os
import time
import base64
import zipfile
from ftplib import FTP

def execute(connector, method, *args):
    res = False
    try:        
        res = getattr(connector,method)(*args)
    except socket.error,e:        
            raise e
    return res

class opendb_backup(osv.osv):
    _name = 'opendb.backup'
    
    _columns = {
        'host' : fields.char('Endereço', size=100, required='True'),
        'port' : fields.char('Porta', size=10, required='True'),
        'name' : fields.char('Banco de dados', size=100, required='True',help='Database you want to schedule backups for'),
        'backup_dir' : fields.char('Local de backup', size=100, help='Absolute path for storing the backups'),
        'ftp_address':fields.char('Endereço FTP', size=100),
        'ftp_port':fields.integer('Porta FTP'),
        'ftp_username': fields.char('Usuário FTP',size=100),
        'ftp_password':fields.char('Senha FTP', size=100),
        'use_ftp':fields.boolean('Usar FTP?'),
        }
    
    _defaults = {
        'backup_dir' : lambda *a : os.getcwd() + '/auto_bkp/DBbackups',
        'host' : lambda *a : 'localhost',
        'port' : lambda *a : '8069',
        'ftp_port':lambda *a: 21,    
    }
    
    def get_db_list(self, cr, user, ids, host='localhost', port='8069', context={}):
        uri = 'http://' + host + ':' + port
        conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
        db_list = execute(conn, 'list')
        return db_list        
     
    
    def _check_db_exist(self, cr, user, ids):
        for rec in self.browse(cr,user,ids):
            db_list = self.get_db_list(cr, user, ids, rec.host, rec.port)
            if rec.name in db_list:
                return True
        return False
    _constraints = [
                    (_check_db_exist, 'Error ! No such database exist.', [])
                    ]
    
    def schedule_backup(self, cr, user, context={}):
        conf_ids= self.search(cr, user, [])
        confs = self.browse(cr,user,conf_ids)
        for rec in confs:
            db_list = self.get_db_list(cr, user, [], rec.host, rec.port)
            if rec.name in db_list:
                try:
                    if not os.path.isdir(rec.backup_dir):
                        os.makedirs(rec.backup_dir)
                except:
                    raise
                bkp_file='%s_%s.sql' % (rec.name, time.strftime('%Y%m%d_%H_%M_%S'))
                zip_file='%s_%s.zip' % (rec.name, time.strftime('%Y%m%d_%H_%M_%S'))
                file_path = os.path.join(rec.backup_dir,bkp_file)
                zip_path = os.path.join(rec.backup_dir,zip_file)
                fp = open(file_path,'wb')
                uri = 'http://' + rec.host + ':' + rec.port
                conn = xmlrpclib.ServerProxy(uri + '/xmlrpc/db')
                bkp=''
                try:
                    bkp = execute(conn, 'dump', 'admin', rec.name)
                except:
                    #logger.notifyChannel('backup', netsvc.LOG_INFO, "Could'nt backup database %s. Bad database administrator password for server running at http://%s:%s" %(rec.name, rec.host, rec.port))
                    continue
                bkp = base64.decodestring(bkp)
                fp.write(bkp)
                fp.close()
                with zipfile.ZipFile(zip_path, 'w') as zipped:
                    zipped.write(file_path)
                zipped.close()
                os.remove(file_path)
                self.send_for_ftp(cr, user, rec, zip_path, zip_file, context)
            else:
                pass            
                #logger.notifyChannel('backup', netsvc.LOG_INFO, "database %s doesn't exist on http://%s:%s" %(rec.name, rec.host, rec.port))
                
    def send_for_ftp(self, cr, user, db_backup, file_to_send, name_to_store, context=None):
        if db_backup.use_ftp:            
            ftp = FTP(db_backup.ftp_address)
            ftp.login(db_backup.ftp_username, db_backup.ftp_password)
            ftp.set_pasv(True)
            fp = open(file_to_send,'r')
            ftp.storbinary(name_to_store, fp)
            ftp.quit()                        
    
opendb_backup()
