# -*- coding: utf-8 -*-
# Copyright 2014-now Equitania Software GmbH - Pforzheim - Germany
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from .utils import parse_yaml_folder, retrieve_valid_input, execute_commands
import click
import os

def welcome():
    click.echo("Welcome to the nginx_set_conf!")


# Help text conf
eq_config_support = """
Insert the conf-template.
\f
We support:\f
\b
- ngx_odoo_ssl_pagespeed (Odoo with ssl and PageSpeed)
- ngx_fast_report (FastReport with ssl)
- ngx_code_server (code-server with ssl)
- ngx_nextcloud (NextCloud with ssl)
- ngx_odoo_http (Odoo only http)
- ngx_odoo_ssl (Odoo with ssl)
- ngx_pgadmin (pgAdmin4 with ssl)
- ngx_pwa (Progressive Web App with ssl)
- ngx_redirect_ssl (Redirect Domain with ssl)
- ngx_redirect (Redirect Domain without ssl)
"""


@click.command()
@click.option('--config_template',
              help=eq_config_support)
@click.option('--ip',
              help='IP address of the server')
@click.option('--domain',
              help='Name of the domain')
@click.option('--port',
              help='Primary port for the Docker container')
@click.option('--cert_name',
              help='Name of certificate')
@click.option('--pollport',
              help='Secondary Docker container port for odoo pollings')
@click.option('--config_path', help='Yaml configuration folder')
def start_nginx_set_conf(config_template, ip, domain, port, cert_name, pollport, config_path):
    if config_path:
        yaml_config_files = parse_yaml_folder(config_path)
        for yaml_config_file in yaml_config_files:
            for _, yaml_config in yaml_config_file.items():
                config_template = yaml_config["config_template"]
                ip = yaml_config["ip"]
                domain = yaml_config["domain"]
                port = str(yaml_config["port"])
                cert_name = yaml_config["cert_name"]
                try:
                    pollport = str(yaml_config["pollport"])
                except:
                    pollport = None
                execute_commands(config_template, domain, ip, cert_name, port, pollport)
    elif config_template and ip and domain and port and cert_name:
        execute_commands(config_template, domain, ip, cert_name, port, pollport)
    else:
        config_template = retrieve_valid_input(eq_config_support + "\n")
        ip = retrieve_valid_input("IP address of the server" + "\n")
        domain = retrieve_valid_input("Name of the domain" + "\n")
        port = retrieve_valid_input("Primary port for the Docker container" + "\n")
        cert_name = retrieve_valid_input("Name of certificate" + "\n")
        pollport = retrieve_valid_input("Secondary Docker container port for odoo pollings" + "\n")
        execute_commands(config_template, domain, ip, cert_name, port, pollport)
    # Restart and check the nginx service
    os.system("systemctl start nginx.service")
    os.system("systemctl status nginx.service")
    os.system("nginx -t")
    os.system("nginx -V")


if __name__ == "__main__":
    welcome()
    start_nginx_set_conf()