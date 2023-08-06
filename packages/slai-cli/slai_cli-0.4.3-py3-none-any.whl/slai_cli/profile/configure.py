import click
import yaml
import os
import slai
import sys

from pathlib import Path
from slai_cli import log
from slai_cli.exceptions import InvalidApiKey
from slai.modules.runtime import ValidRuntimes


def get_credentials(profile_name="default", runtime=ValidRuntimes.Project):
    if runtime == ValidRuntimes.Local:
        profile_name = click.prompt(
            "Profile name", type=str, show_default=True, default=profile_name
        )

    client_id = click.prompt("Client ID", type=str)
    client_secret = click.prompt("Client Secret", type=str)

    try:
        store_credentials(
            profile_name=profile_name,
            client_id=client_id,
            client_secret=client_secret,
            runtime=runtime,
        )
    except InvalidApiKey:
        log.warn("Invalid credentials.")
        return

    log.action("Credentials configured.")


def store_credentials(*, profile_name, client_id, client_secret, runtime):
    new_profile = {
        "client_id": client_id,
        "client_secret": client_secret,
    }

    try:
        slai.login(client_id=client_id, client_secret=client_secret, key_type="USER")
    except slai.exceptions.InvalidCredentials:
        log.warn("Invalid credentials")
        sys.exit(1)

    if runtime == ValidRuntimes.Local:
        credentials_path = f"{Path.home()}/.slai"
        if not os.path.exists(credentials_path):
            os.makedirs(credentials_path)
    elif runtime == ValidRuntimes.Project:
        credentials_path = f"{Path.cwd()}/.slai"

    try:
        with open(f"{credentials_path}/credentials.yml", "r") as f_in:
            try:
                credentials = yaml.safe_load(f_in)
            except yaml.YAMLError:
                pass
    except:
        credentials = {}

    # save new profile
    if runtime == ValidRuntimes.Local:
        if credentials.get("default") is None:
            credentials["default"] = new_profile

        credentials[profile_name] = new_profile
    elif runtime == ValidRuntimes.Project:
        credentials = new_profile

    noalias_dumper = yaml.dumper.SafeDumper
    noalias_dumper.ignore_aliases = lambda self, data: True

    with open(f"{credentials_path}/credentials.yml", "w") as f_out:
        yaml.dump(credentials, f_out, default_flow_style=False, Dumper=noalias_dumper)
