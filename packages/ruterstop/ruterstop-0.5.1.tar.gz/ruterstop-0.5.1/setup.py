# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ruterstop', 'ruterstop.tests']

package_data = \
{'': ['*']}

install_requires = \
['bottle>=0.12.19,<0.13.0', 'requests>=2.25.1,<3.0.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['ruterstop = ruterstop:main']}

setup_kwargs = {
    'name': 'ruterstop',
    'version': '0.5.1',
    'description': 'Et program som viser sanntidsinformasjon for stoppesteder i Oslo og deler av Viken.',
    'long_description': '# ruterstop\n\nEt program som viser sanntidsinformasjon for stoppesteder i Oslo og deler av Viken.\n\n- Lister 20 av de neste avgangene\n- Bruk filtre som `--direction`, `--grouped` og `--min-eta`\n- Start en HTTP server med `--server`\n- Søk etter stoppesteder med `--search-stop`\n- Sett når du ønsker å se klokkeslett med `--long-eta`\n- Bruk `--help` for full hjelp\n\nInnspill, tanker og feilmeldinger mottas med glede!\n\n![Adafruit Feather HUZZAH ESP8266 med OLED FeatherWing som kjører ruterstop.py][demopic-1]\n\n## Installasjon\n\nTrenger Python >=3.6 for å kjøre.\n\n### Installer fra PyPi\n\n```\n$ pip install ruterstop\n```\n\n### Bygg fra kildekode\n\nLast ned kildekoden og installer programmet med avhengigheter fra kildekodemappen\n\n```\n$ pip install poetry\n$ poetry build\n```\n\n## Brukerveiledning\n\nSøk etter stoppested\n\n```\n$ ruterstop --search-stop stig\n6013    Stig (Oslo, Oslo)\n59445   Stige (Ålesund, Møre og Romsdal)\n13479   Stigen (Ringebu, Innlandet)\n18602   Stigen (Sandefjord, Vestfold og Telemark)\n18605   Stiger (Sandefjord, Vestfold og Telemark)\n21507   Stigen (Porsgrunn, Vestfold og Telemark)\n3857    Stigen (Aurskog-Høland, Viken)\n45978   Stigen (Nærøysund, Trøndelag)\n54253   Stigen (Lyngen, Troms og Finnmark)\n7844    Stigen (Trysil, Innlandet)\n```\n\nKjør programmet med et valgt stoppested\n\n```\n$ ruterstop --stop-id 6013 --direction outbound\n31 Snaroeya       naa\n31 Fornebu     10 min\n31 Snaroeya    20 min\n25 Majorstuen  28 min\n31 Fornebu     30 min\n```\n\nEller start som en HTTP server\n\n```\n$ ruterstop --server\n```\n\nStoppested og filtre velges i adressen til spørringen\n\n```\n$ curl localhost:4000/6013?direction=outbound&long_eta=10\n31 Fornebu        naa\n31 Snaroeya     5 min\n31 Fornebu      8 min\n31 Fornebu     10 min\n25 Majorstuen   20:21\n31 Snaroeya     20:24\n31 Snaroeya     20:36\n25 Majorstuen   20:36\n31 Fornebu      20:42\n```\n\n## Utvikling\n\n### Kjør tester\n\n```\n$ poetry install\n$ poetry run python -m unittest\n```\n\n### Kjør multi-versjon tester i Docker\n\n```\n$ make matrix\n```\n\nSe Makefile for detaljer\n\n### Tag ny versjon\n\n```\n$ ./.deploy/bump_version.py\n```\n\nVerktøyet hjelper til å huske å bytte versjonsnummer før tagging og sjekke\nat man er på riktig branch.\n\n## Motivasjon\n\nJeg vil se avganger fra mitt nærmeste stoppested mens jeg sitter ved\nkjøkkenbordet, uten å måtte bruke mobilen.\n\nDette prosjektet blir også utnyttet til å prøve ut alle ting om Python jeg\nbåde kan og ikke kan.\n\nJeg skrev dette programmet som en backend til en ESP8266-variant med en\nOLED skjerm.\nFungerende klient-kode for en Adafruit Feather HUZZAH ESP8266 med en OLED\nFeatherWing finnes i [eksempel-mappen](./examples/arduino-esp8266-feather-oled).\n\n## Referanser og linker\n- [Søk etter stoppesteder][stoppesteder] (Logg inn med guest:guest)\n- [EnTur JourneyPlanner docs](https://developer.entur.org/pages-journeyplanner-journeyplanner)\n- [EnTur JourneyPlanner IDE](https://api.entur.io/journey-planner/v2/ide/)\n\n[demopic-1]: ./demo-1.png\n[stoppesteder]: https://stoppested.entur.org/?stopPlaceId=NSR:StopPlace:6013\n',
    'author': 'Stig Otnes Kolstad',
    'author_email': 'stig@stigok.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stigok/ruterstop',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
