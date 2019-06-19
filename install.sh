#!/bin/bash

IS_BASIC=${1:-'1'}

echo "Updating system"
apt-get -y update
apt-get -y upgrade

echo "Installing git"
apt-get -y install git-core

echo "Installing docker"
apt-get -y install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get -y update
apt-get -y install docker-ce
systemctl start docker
systemctl enable docker

echo "Installing docker compose"
curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

echo "Cloning basic modules"

git clone https://gitlab.com/rash07/facturaloperu_odoo_facturacion.git ./addons/facturaloperu_odoo_facturacion
git clone https://gitlab.com/rash07/facturaloperu_odoo_pos.git ./addons/facturaloperu_odoo_pos

if ! [ $IS_BASIC = '1' ]; then
	git clone https://gitlab.com/rash07/facturaloperu_odoo_reportes.git ./addons/facturaloperu_odoo_reportes
	git clone https://gitlab.com/rash07/facturaloperu_odoo_guias.git ./addons/facturaloperu_odoo_guias
	git clone https://gitlab.com/rash07/facturaloperu_odoo_kardex.git ./addons/facturaloperu_odoo_kardex
fi

echo "Configuring"
docker-compose up -d
