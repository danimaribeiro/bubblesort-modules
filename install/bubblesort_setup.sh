#!/bin/bash

echo "Iniciando a atualização da lista de pacotes"
apt-get update

echo "Iniciando a atualização"
apt-get upgrade --yes

echo "Instalando python"
apt-get install python

echo "Instalando python dependencias"
apt-get install graphviz ghostscript postgresql-client \
          python-dateutil python-feedparser python-gdata \
          python-ldap python-libxslt1 python-lxml python-mako \
          python-openid python-psycopg2 python-pybabel python-pychart \
          python-pydot python-pyparsing python-reportlab python-simplejson \
          python-tz python-vatnumber python-vobject python-webdav \
          python-werkzeug python-xlwt python-yaml python-imaging \
          python-matplotlib python-pip libpq-dev python-dev --yes

pip install unittest2
pip install psutil
pip install jinja2
pip install docutils
pip install requests

echo "Instalando PySped, aqui pode dar erro facilmente"
apt-get install libxmlsec1-dev --yes
apt-get install libxml2-dev --yes

if [ $(uname -m) == 'x86_64' ]; then
	pip install https://github.com/aricaldeira/pyxmlsec/archive/master.zip
	echo "skipping"
else
	pip install pyxmlsec
fi

pip install https://github.com/aricaldeira/geraldo/archive/master.zip
pip install pysped

echo "Instalando git"
apt-get install git --yes

echo "Instalando bzr"
apt-get install bzr --yes

echo "Efetuando download do fonte"
if [ -d odoo ]
then
	echo "Atualizando o código fonte odoo"
	cd odoo
	git pull
	cd ..
else
	echo "Clonando dados odoo"
	git clone https://github.com/odoo/odoo.git
fi

if [ -d nfe ]
then
	echo "Atualizando o código fonte nfe"
	cd nfe
	git pull
	cd ..
else
	echo "Clonando dados nfe"
	git clone https://github.com/openerpbrasil-fiscal/nfe.git
fi

if [ -d localizacao ]
then
	echo "Atualizando o código fonte localizacao"
	cd localizacao
	git pull
	cd ..
else
	echo "Clonando dados localizacao"
	git clone https://github.com/openerpbrasil-fiscal/l10n_br_core.git localizacao
	cd localizacao
	git checkout 8.0
	cd ..
fi

if [ -d bubblesort ]
then
	echo "Atualizando o código fonte bublesort"
	cd bubblesort
	git pull
	cd ..
else
	echo "Clonando dados bubblesort"
	git clone https://github.com/danimaribeiro/bubblesort-modules.git bubblesort
fi

if [ -d contas ]
then
	echo "Atualizando o código fonte contas"
	cd contas
	bzr update
	cd ..
else
	echo "Clonando dados contas"
	bzr checkout --lightweight lp:account-payment/7.0 contas
fi

if [ -d regras ]
then
	echo "Atualizando o código fonte regras"
	cd regras
	bzr update
	cd ..
else
	echo "Clonando dados regras"
	bzr checkout --lightweight lp:openerp-fiscal-rules regras
fi

echo "Instalando banco de dados"
apt-get install postgresql --yes

echo "Criando usuario"
sudo -u postgres createuser --superuser bubblesort

echo "Alterando senha"
sudo -u postgres psql -c"ALTER user bubblesort WITH PASSWORD '123456'"

cd odoo

CAMINHO="openerp/addons,addons,../contas,../regras,../localizacao,../nfe,../bubblesort"
sudo -u $SUDO_USER bash << EOF


echo "Iniciando o openerp para gerar arquivo de configuração: $CAMINHO"

timeout --kill=3 3 ./openerp-server -s --db_host=127.0.0.1 --db_port=5432 \
		--db_user=bubblesort --db_password=123456 \
		--data-dir=/home/danimar/dados --addons-path=$CAMINHO

EOF

echo "Movendo arquivo de configuracao"
cd ..
mv .openerp_serverrc openerp-config

local=$(pwd)
echo $local
echo "Iniciando instalação do servidor de aplicação"
apt-get install nginx --yes
service nginx start

if [ -h /etc/nginx/sites-enabled/default ]
then
	rm /etc/nginx/sites-enabled/default
fi
cp nginx-openerp /etc/nginx/sites-available/nginx-openerp

if [ ! -h /etc/nginx/sites-enabled/nginx-openerp ]
then
	ln -s /etc/nginx/sites-available/nginx-openerp /etc/nginx/sites-enabled/nginx-openerp
fi

service nginx restart

echo "Copiando arquivo openerp-config e iniciando o servidor para ver se tudo deu certo :)"

cp openerp-config odoo/openerp-config
chown $SUDO_USER:$SUDO_USER odoo/openerp-config
cd odoo

sudo -u $SUDO_USER bash << EOF

echo "Iniciando o openerp para testar instalação"
./openerp-server --config=openerp-config

EOF

cd ..

