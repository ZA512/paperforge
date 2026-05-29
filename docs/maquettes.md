# Maquettes fonctionnelles

Ces maquettes decrivent les premiers ecrans produit. Elles ne figent pas le
style visuel; elles fixent les zones, les controles et les flux.

## 1. Choix du produit

```text
+--------------------------------------------------------------+
| Paperforge                                      [Rechercher] |
+--------------------------------------------------------------+
| Choisir un carnet                                            |
|                                                              |
| [Gestion de projets]  99 projets, journal, radar, index      |
| [Reunion / comite]    A definir                              |
| [Suivi personnel]     A definir                              |
|                                                              |
|                                    [Continuer]               |
+--------------------------------------------------------------+
```

Etat attendu:

- le bouton continuer est actif quand un produit est selectionne;
- chaque carte affiche nom, usage, format et nombre de pages estime;
- le produit selectionne determine le schema de parametrage suivant.

## 2. Parametrage du produit

```text
+--------------------------------------------------------------+
| <- Produit              Gestion de projets        [Apercu]   |
+----------------------+---------------------------------------+
| Parametres           | Titre du carnet                       |
| - General            | [Carnet de pilotage projets        ]  |
| - Pages              |                                       |
| - Nomenclature       | Format           [Tablette 16:10 v]   |
| - Export             | Orientation      [Paysage v]          |
|                      | Nombre de projets [99]                |
|                      | Pages / projet    [-] [2] [+]         |
|                      | Pages journal     [-] [2] [+]         |
|                      | Pages radar       [-] [2] [+]         |
|                      |                                       |
|                      | Nomenclature                          |
|                      | [•] Action  [-] Note  [?] Question    |
|                      | [!] Important [W] Attente             |
|                      | [B] Blocage  [D] Decision             |
|                      |                                       |
|                      |                  [Choisir le theme]   |
+----------------------+---------------------------------------+
```

Etat attendu:

- controles numeriques bornes selon le schema `ProductOption`;
- nomenclature affichee mais non modifiable dans la V1;
- apercu HTML possible avant generation PDF.

## 3. Choix du theme

```text
+--------------------------------------------------------------+
| <- Parametres                Theme                [Apercu]   |
+--------------------------------------------------------------+
| [Pro paysage 16:10]  Couleurs sobres, tablette, liens clairs |
| [A4 portrait]        Variante future                          |
| [Minimal print]      Variante future                          |
|                                                              |
| Format: tablette 16:10                                      |
| Pages estimees: 209                                         |
|                                                              |
|                           [Generer le PDF]                  |
+--------------------------------------------------------------+
```

Etat attendu:

- un theme est obligatoire;
- le choix du theme definit le CSS et le format `@page`;
- le nombre de pages estime reste visible avant export.

## 4. Generation PDF

```text
+--------------------------------------------------------------+
| Generation                                             [X]   |
+--------------------------------------------------------------+
| Produit: Gestion de projets                                  |
| Theme: Pro paysage 16:10                                     |
| Sortie: carnet_pilotage_projets_99.pdf                       |
|                                                              |
| [1] Validation configuration        OK                       |
| [2] Rendu HTML                      OK                       |
| [3] Conversion PDF                  En cours                 |
| [4] Verification liens internes     A venir                  |
|                                                              |
|                             [Ouvrir le PDF] [Regenerer]      |
+--------------------------------------------------------------+
```

Etat attendu:

- erreurs affichees par etape;
- HTML conserve possible pour debug;
- verification future: existence des ancres et nombre de pages.
