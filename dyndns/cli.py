from pathlib import Path

import httpx
import typer
from tomli import load

from dyndns.schemas import DynDnsDict

app = typer.Typer(name="DynDNS")


@app.command()
def single(
    domain: str = typer.Argument(..., help="Domain to update"),
    username: str = typer.Option(..., "--username", "-u", help="Username to use"),
    password: str = typer.Option(..., "--password", "-p", help="Password to use"),
):
    typer.echo(f"Updating {domain}... ", nl=False)

    r = httpx.get(
        f"https://{username}:{password}@domains.google.com/nic/update?hostname={domain}"
    )

    r.raise_for_status()

    typer.echo("Done.")


@app.command()
def update(
    input: Path = typer.Option(..., "--input", "-i", help="Input TOML file to use"),
):
    with input.open("rb") as f:
        data = load(f)

    domains = DynDnsDict.validate_python(data)

    for domain, dyn_dns in domains.items():
        single(
            domain,
            dyn_dns.username.get_secret_value(),
            dyn_dns.password.get_secret_value(),
        )
