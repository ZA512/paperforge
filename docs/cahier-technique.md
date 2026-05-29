# Cahier technique Paperforge

## Objectif

Transformer un choix produit + des parametres + un theme en PDF finalise avec
liens internes. Le rendu canonique est HTML/CSS, puis conversion PDF via
WeasyPrint.

## Pipeline

1. Charger une configuration JSON.
2. Valider le produit, le theme et les options.
3. Construire un contexte de rendu stable.
4. Rendre un HTML Jinja2 unique.
5. Convertir en PDF avec WeasyPrint, ou sortir le HTML pour debug.

## Schema de fichiers

```text
configs/
  project_management_99.json      Exemple de configuration utilisateur.
docs/
  cahier-technique.md             Specification technique.
  maquettes.md                    Maquettes fonctionnelles des ecrans.
paperforge/
  cli.py                          Commande `paperforge render`.
  models.py                       Dataclasses Theme, ProductSpec, ProductOption.
  products.py                     Catalogue, valeurs par defaut, contexte.
  render.py                       Jinja2 + WeasyPrint.
templates/
  products/
    project_management_99.html.j2 Template PDF du carnet projets.
  shared/
    topline.html.j2               Navigation interne reutilisable.
  themes/
    pro_landscape.css             Theme paysage 16:10.
tests/
  test_products.py                Validation des options et du contexte.
```

## Modele de donnees

`RenderRequest`

```json
{
  "product": "project_management_99",
  "theme": "pro_landscape",
  "title": "Carnet de pilotage projets",
  "options": {
    "page_format": "tablet_16_10",
    "orientation": "landscape",
    "project_count": 99,
    "pages_per_project": 2,
    "journal_pages": 2,
    "radar_pages": 2
  },
  "metadata": {
    "format": "tablette 16:10",
    "subtitle": "Capture rapide, radar de relance, index hyperlie et 99 projets en deux pages."
  }
}
```

`ProductSpec`

```text
slug          Identifiant stable du produit.
label         Libelle affiche dans l'interface.
template_file Template Jinja2 a rendre.
options       Schema de parametrage du produit.
```

`Theme`

```text
slug       Identifiant stable du theme.
label      Libelle affiche.
css_file   CSS injecte dans le HTML.
page_size  Format logique, par exemple tablet_landscape_16_10.
```

## Produit 1: gestion de projets

Regles implementees:

- 99 projets maximum.
- Nombre de pages par projet configurable, defaut 2.
- Page 1 projet: synthese.
- Page 2 projet: actions / journal.
- Pages projet 3 et plus: notes supplementaires.
- Journal du jour configurable, defaut 2 pages.
- Radar non specialise configurable, defaut 2 pages.
- Format configurable: tablette 16:10, TCL NXTPAPER 11+, A4, A5.
- Orientation configurable: paysage ou portrait.
- Page priorites.
- Index par blocs de 25 lignes.
- Index reduit a `N / Projet / Etat`.
- Nomenclature `• - ? ! W B D`.
- Liens internes: accueil, methode, journal, radar, priorites, index, projets.

Pagination par defaut:

```text
1 accueil
1 methode
2 journal
2 radar
1 priorites
4 index
198 pages projet avec 2 pages par projet
= 209 pages
```

## Conventions de liens

```text
#home
#method
#journal-1
#radar-1
#priorities
#index-1
#project-01-summary
#project-01-actions
```

Ces identifiants restent stables pour permettre les liens internes PDF et les
tests automatiques.
