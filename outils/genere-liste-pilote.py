#!/usr/bin/env python3
# -*- coding: ascii -*-
"""genere-liste-pilote.py -- la liste du corpus PILOTE, ecrite en dur.

DERIVE DATE du 2026-09-18 de
  C:\\Users\\cdats\\Claude\\CIN\\analyses-de-films\\outils\\genere-liste-statique.py
(depot de production) -- divergence non detectee automatiquement.
BKL-CIN-096 (b) lot 5, T1.2. Ce n'est pas une copie : c'est un DERIVE, et les
ecarts au script de production sont nommes un a un ci-dessous.

CE QUI CHANGE PAR RAPPORT A LA PRODUCTION, ET POURQUOI

  1. UNE SEULE page de liste. La production en a trois (index, critiques,
     etudes, meme composant, trois filtres -- P-07). La surface pilote n'a
     qu'`index.html`, et ne produit que des Critiques (la skill de production
     ne produit pas d'Etude : SKILL.md section 0). PAGES ne porte donc qu'une
     entree, sans filtre, et le marqueur d'Etude (`span.marq`) est retire --
     il ne pourrait jamais sortir.

  2. GABARIT DE VIGNETTE PROPRE. La production ecrit ses <li> a l'interieur
     d'un <ol class="liste"> permanent, pose a la main dans la page. Le pilote
     n'a pas de <ol> permanent : son `index.html` porte un BLOC D'ETAT VIDE.
     Le gabarit d'ici produit donc l'enveloppe <ol> elle-meme, et la retire
     quand le registre est vide. Il n'y a pas de `corpus.js` sur le pilote :
     aucun second gabarit ne peut deriver de celui-ci (le risque que
     --verifier surveille en production n'existe donc pas ici sous cette
     forme ; ce que --verifier surveille ici, c'est la derive entre le
     registre et le HTML servi).

  3. ETAT VIDE REPRODUIT A L'OCTET. Registre vide => le script re-ecrit
     EXACTEMENT le bloc d'etat vide d'origine (constante VIDE ci-dessous), de
     sorte que `--verifier` sorte 0 sans aucun changement visible sur une
     surface qui n'a rien publie. C'est l'etat NOMINAL du pilote au lot 5 :
     un generateur qui viderait la page serait un generateur qui casse la
     recette du lot 4.

  4. AUCUN GENERATEUR DE SITEMAP, ET C'EST VOULU. La production regenere
     `sitemap.xml` au meme endroit (BKL-CIN-089). Ici, JAMAIS : un sitemap
     sert l'INDEXATION, que la borne A6 de la surface pilote interdit (toute
     page porte `noindex, nofollow`). Ni sitemap.xml, ni robots.txt.

  5. Les tables ETIQUETTES et PLI sont une COPIE DATEE du 2026-09-18 de
     celles du script de production -- elles y sont elles-memes le jumeau de
     `assets/corpus.js`. Divergence non detectee automatiquement.

Les SEUILS, les CODES DE SORTIE et la doctrine (le HTML en dur, relisible tel
quel dans le depot, frontiere P-31) sont inchanges.

Usage : python genere-liste-pilote.py [--depot CHEMIN] [--verifier]
Codes : 0 conforme -- 1 derive ou marqueur absent -- 2 fichier introuvable.
"""

import argparse
import io
import os
import sys

DEBUT = "<!-- LISTE-STATIQUE:DEBUT (genere par outils/genere-liste-pilote.py) -->"
FIN = "<!-- LISTE-STATIQUE:FIN -->"

# La seule page de liste de la surface pilote, sans filtre de volet.
PAGES = [("index.html", None)]

# Bloc d'ETAT VIDE -- byte pour byte celui que le lot 4 a publie dans
# index.html. Ecrit en point de code (\u00e9) parce que ce fichier est en
# ASCII pur (skill de production, section 0 bis) ; la page, elle, est en
# UTF-8 accentue normal.
VIDE = u"      <p>Aucune page n'est encore publi\u00e9e ici.</p>"

# Copie datee du 2026-09-18 de la table du script de production (jumelle de
# celle de assets/corpus.js cote production). Toute valeur absente prend une
# majuscule initiale.
ETIQUETTES = {
    "critique": "Critiques", "etude": "&Eacute;tudes", "n&b": "N&amp;B",
    "melodrame": "M&eacute;lodrame", "comedie": "Com&eacute;die",
    "tragedie": "Trag&eacute;die",
    "Etats-Unis": "&Eacute;tats-Unis",
    "Union sovietique": "Union sovi&eacute;tique",
}


def lire(chemin):
    with io.open(chemin, "r", encoding="utf-8") as f:
        return f.read()


def ecrire(chemin, texte):
    with io.open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(texte)


def echappe(s):
    """Meme echappement que la production : & < > " et rien d'autre."""
    if s is None:
        return ""
    return (unicode_str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def unicode_str(s):
    return s if isinstance(s, type(u"")) else u"%s" % s


def etiquette(v):
    """Rend du HTML PRET A POSER -- deja echappe, entites comprises.

    Les valeurs de la table portent des entites (&eacute;) : les repasser
    dans echappe() afficherait litteralement "M&eacute;lodrame". La table est
    donc rendue telle quelle, et seules les valeurs absentes sont echappees.
    """
    if v in ETIQUETTES:
        return ETIQUETTES[v]
    v = unicode_str(v)
    return echappe(v[:1].upper() + v[1:])


# Repli des diacritiques -- copie datee de la table PLI du script de
# production. Ecrite en points de code : le fichier reste ASCII pur. Elle est
# la CLE DE TRI, donc ce qui garantit un ordre stable d'une passe a l'autre.
_ACCENTUES = (u"\u00e0\u00e2\u00e4\u00e3\u00e5\u00e1\u00e7\u00e9\u00e8\u00ea"
              u"\u00eb\u00ee\u00ef\u00ec\u00ed\u00f1\u00f4\u00f6\u00f2\u00f3"
              u"\u00f5\u00f8\u00f9\u00fb\u00fc\u00fa\u00ff\u00fd")
_PLATS = u"aaaaaaceeeeiiiinoooooouuuuyy"
PLI = dict(zip(_ACCENTUES, _PLATS))
PLI[u"\u0153"] = u"oe"   # oe lie
PLI[u"\u00e6"] = u"ae"   # ae lie


def norm(s):
    s = unicode_str(s or u"").lower()
    return u"".join(PLI.get(c, c) for c in s)


def ordre_catalogue(f):
    """Ordre du catalogue : alphabetique par titre replie (comme en
    production). Le titre brut departage deux titres de meme repli."""
    return (norm(f["title"]), unicode_str(f["title"] or u""))


def decoupe_entrees(source):
    debut = source.find("const FILMS")
    if debut < 0:
        raise ValueError("tableau FILMS introuvable")
    corps = source[debut:]
    entrees, profondeur, courant = [], 0, []
    for ch in corps:
        if ch == "{":
            profondeur += 1
            if profondeur == 1:
                courant = []
                continue
        elif ch == "}":
            profondeur -= 1
            if profondeur == 0:
                entrees.append(u"".join(courant))
                continue
        if profondeur >= 1:
            courant.append(ch)
    return entrees


def champ(bloc_texte, nom):
    import re
    m = re.search(re.escape(nom) + r"\s*:\s*\[(.*?)\]", bloc_texte, re.S)
    if m:
        return [a or b for a, b in
                re.findall(r"'([^']*)'|\"([^\"]*)\"", m.group(1))]
    for motif in (r"\s*:\s*'((?:[^'\\]|\\.)*)'", r'\s*:\s*"((?:[^"\\]|\\.)*)"'):
        m = re.search(re.escape(nom) + motif, bloc_texte)
        if m:
            return m.group(1).replace("\\'", "'").replace('\\"', '"')
    m = re.search(re.escape(nom) + r"\s*:\s*(\d+)", bloc_texte)
    if m:
        return int(m.group(1))
    return None


def entree(bloc_texte):
    return {
        "slug": champ(bloc_texte, "slug"),
        "title": champ(bloc_texte, "title"),
        "director": champ(bloc_texte, "director"),
        "year": champ(bloc_texte, "year"),
        "url": champ(bloc_texte, "url"),
        "genreBase": champ(bloc_texte, "genreBase"),
        "volet": champ(bloc_texte, "volet") or "critique",
        "datePublication": champ(bloc_texte, "datePublication"),
    }


def derniere_publiee(films):
    dates = [f for f in films if f["datePublication"]]
    if not dates:
        return None
    dates.sort(key=lambda f: (f["datePublication"], f["title"]), reverse=True)
    return dates[0]


def li(f, derniere):
    """Gabarit de vignette PROPRE AU PILOTE.

    Pas de `span.marq` (aucune Etude ne sort de cette chaine). Le marqueur
    `span.neuf` est conserve : c'est le meme composant CSS que la production,
    et la comparabilite des deux surfaces est l'objet meme du pilote.
    """
    neuf = ('<span class="neuf">derni&egrave;re publi&eacute;e</span>'
            if derniere and f["slug"] == derniere["slug"] else "")
    suite = (u" &mdash; " + etiquette(f["genreBase"])) if f["genreBase"] else u""
    return (u'      <li><a class="entree" href="%s" data-volet="%s">'
            u'<span class="t">%s%s</span>'
            u'<span class="a">%s</span>'
            u'<span class="d">%s%s</span>'
            u'</a></li>'
            % (echappe(f["url"]), f["volet"], echappe(f["title"]), neuf,
               f["year"] or "", echappe(f["director"]), suite))


def bloc(films, filtre, derniere):
    """Le contenu entre les deux marqueurs.

    Registre VIDE -> le bloc d'etat vide d'origine, a l'octet (voir VIDE).
    Registre non vide -> l'enveloppe <ol class="liste"> et ses vignettes.
    """
    vus = [f for f in films if filtre is None or f["volet"] == filtre]
    if not vus:
        corps = VIDE
    else:
        corps = (u'      <ol class="liste">\n'
                 + u"\n".join(li(f, derniere) for f in vus)
                 + u'\n      </ol>')
    return DEBUT + u"\n" + corps + u"\n    " + FIN


def applique(chemin, contenu):
    src = lire(chemin)
    i, j = src.find(DEBUT), src.find(FIN)
    if i < 0 or j < 0:
        sys.stderr.write("Marqueurs absents dans %s\n" % chemin)
        return None, None
    neuf = src[:i] + contenu + src[j + len(FIN):]
    return src, neuf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--depot", default=os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))))
    ap.add_argument("--verifier", action="store_true")
    args = ap.parse_args()

    registre = os.path.join(args.depot, "assets", "films-data.js")
    if not os.path.isfile(registre):
        sys.stderr.write("Introuvable : %s\n" % registre)
        return 2

    films = [entree(b) for b in decoupe_entrees(lire(registre))]
    films = [f for f in films if f["slug"]]
    derniere = derniere_publiee(films)
    films.sort(key=ordre_catalogue)

    code = 0
    for nom, filtre in PAGES:
        chemin = os.path.join(args.depot, nom)
        if not os.path.isfile(chemin):
            sys.stderr.write("Introuvable : %s\n" % chemin)
            return 2
        contenu = bloc(films, filtre, derniere)
        src, neuf = applique(chemin, contenu)
        if src is None:
            return 1
        n = len([f for f in films if filtre is None or f["volet"] == filtre])
        etat_vide = " (etat vide)" if n == 0 else ""
        if args.verifier:
            etat = "conforme" if src == neuf else "DERIVE"
            if src != neuf:
                code = 1
            print("%-24s %-9s %d entrees en dur%s" % (nom, etat, n, etat_vide))
        else:
            if src != neuf:
                ecrire(chemin, neuf)
            print("%-24s %d entrees ecrites en dur%s" % (nom, n, etat_vide))

    if args.verifier and code == 0:
        print("")
        print("Aucune derive entre le gabarit du script et le HTML du depot.")
    elif args.verifier:
        print("")
        print("DERIVE : le HTML ne correspond plus au registre. Regenerer.")
    return code


if __name__ == "__main__":
    sys.exit(main())
