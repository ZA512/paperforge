# Paperforge

Paperforge est un atelier local pour composer des carnets PDF parametrables.
L'utilisateur choisit un produit, ajuste ses parametres, choisit un theme, puis
genere un HTML/PDF ou recupere la commande Python finale.

Le rendu canonique est HTML/CSS avec templates Jinja2. La conversion PDF est
deleguee a WeasyPrint afin de conserver les liens internes du carnet.

## Produit disponible

`project_management_99` genere un carnet de pilotage projets:

- 99 projets maximum;
- nombre de pages par projet configurable, avec 2 pages par defaut: synthese et actions / journal;
- journal du jour;
- radar non specialise;
- priorites;
- index `N / Projet / Etat`;
- nomenclature `• - ? ! W B D`;
- ancres et liens internes (`#journal-1`, `#project-01-summary`, etc.).

## Installation

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
```

## Utilisation web

```powershell
.\.venv\Scripts\python.exe -m paperforge.cli web --host 127.0.0.1 --port 8765
```

Puis ouvrir:

```text
http://127.0.0.1:8765
```

L'interface permet de:

- choisir le produit;
- modifier titre, format, orientation, sous-titre et quantites de pages;
- choisir le nombre de pages par projet;
- choisir le theme;
- generer un HTML;
- tenter une generation PDF;
- produire une commande CLI rejouable.

## Utilisation CLI

Generer un PDF:

```powershell
.\.venv\Scripts\python.exe -m paperforge.cli render `
  --config configs\project_management_99.json `
  --output dist\carnet_pilotage_projets_99.pdf
```

Generer seulement le HTML:

```powershell
.\.venv\Scripts\python.exe -m paperforge.cli render `
  --config configs\project_management_99.json `
  --output dist\carnet_pilotage_projets_99.html `
  --html-only
```

## Structure

```text
paperforge/
  cli.py              Commandes `render` et `web`
  models.py           Modeles de donnees generiques
  products.py         Catalogue produit/theme et contexte de rendu
  render.py           Moteur Jinja2 + WeasyPrint
  web.py              Application web locale
templates/
  products/           Templates de carnets
  themes/             CSS de rendu PDF
  web/                Interface web locale
configs/              Configurations de generation
docs/                 Notes techniques et maquettes
tests/                Tests du modele et du rendu HTML
```

## Tests

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Note Windows / WeasyPrint

Sur Windows, le package Python `weasyprint` peut aussi demander les librairies
natives Pango/GTK. Si la generation PDF echoue avec `libgobject-2.0-0`, le rendu
HTML reste disponible avec `--html-only`. Il faut installer les dependances
natives indiquees par la documentation WeasyPrint avant de relancer la conversion
PDF.

Alternative pratique: placer l'executable officiel `weasyprint.exe` a la racine
du projet. Paperforge l'utilise automatiquement en fallback si la librairie
Python WeasyPrint ne peut pas charger les DLL natives.

Le format `TCL NXTPAPER 11+` utilise une page de 2200 x 1440 px en paysage
afin de conserver le ratio de la tablette.
