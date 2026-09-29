// Registre des analyses publiées sur la SURFACE PILOTE.
//
// BKL-CIN-096 (b) lot 5, T1.4 — créé VIDE le 2026-09-18, et il doit le rester
// jusqu'au lot 6 : le lot 5 outille la chaîne, il ne l'active pas. Une entrée
// ici au sortir de cette fenêtre serait un dépassement de mandat (V1).
//
// Schéma v2 (annexe B de SPEC-SITE-V2), identique à celui de la production —
// c'est ce qui rend les deux corpus comparables (analyse §L4.8, C4). Rédacteur
// unique de ce fichier : la skill `analyse-films-pilote`, une entrée par
// publication, ajoutée à la FIN du tableau, avant le `];` de fermeture.
//
// Champs obligatoires (leur absence bloque la publication, contrôle
// outils/controle-vocabulaires.py --strict) :
//   slug, title, director, year, url, summary, datePublication,
//   pays, genreBase, technique, producteur, volet.
// `poster` est facultatif : sur cette surface, la décision (3) d'AH du
// 18/09/2026 borne les affiches à la base locale D: — sinon SANS AFFICHE, ce
// qui est un cas nominal, jamais un échec.
//
// Deux valeurs sont propres au pilote et ne se devinent pas :
//   volet      : toujours 'critique' — la chaîne pilote ne produit pas
//                d'Étude (skill de production §0, SPEC-PROCESS-SCHOLAR).
//   producteur : '<Modèle nommé> (chaîne pilote automatique)', jamais
//                '(session supervisée)' — il n'y a aucune supervision ici, et
//                le registre fait foi pour la phrase de signature de la page
//                (P-17, P-18 : jamais deviné, jamais vide).
//
// Les axes fermés (volet, genreBase, technique, pays) puisent EXCLUSIVEMENT
// dans assets/vocabulaires.js de CE dépôt (copie datée du 2026-09-18). Une
// valeur absente du vocabulaire est un ARRÊT de la chaîne, jamais un ajout :
// ajouter un terme est un acte délibéré d'AH (P-12).
//
// Gabarit d'une entrée, pour mémoire — à ne pas dé-commenter à la main :
//   {
//     slug: '<slug>',
//     title: '<Titre>',
//     director: '<Réalisateur·rice>',
//     year: <année du film>,
//     summary: "<phrase éditoriale — étape 6>",
//     url: 'films/<slug>.html',
//     poster: 'assets/posters/<slug>.jpg',   // facultatif
//     volet: 'critique',
//     datePublication: '<AAAA-MM-JJ hh:mm>',
//     genreBase: '<valeur du vocabulaire fermé>',
//     producteur: '<Modèle nommé> (chaîne pilote automatique)',
//     pays: ['<valeur>'],
//     technique: ['<valeur>']
//   }
//
// Il n'y a PAS de champ `promotion` sur cette surface : l'accueil du pilote
// ne met rien en une.
const FILMS = [
  {
    slug: 'le-chateau-ambulant',
    title: 'Le Château ambulant',
    director: 'Hayao Miyazaki',
    year: 2004,
    summary: "Une maison qui n'a pas de forme, une héroïne dont le visage suit la confiance qu'elle se porte : Miyazaki fait du désordre son sujet, et refuse jusqu'au bout de le remettre en ordre.",
    url: 'films/le-chateau-ambulant.html',
    poster: 'assets/posters/le-chateau-ambulant.jpg',
    volet: 'critique',
    datePublication: '2026-09-19 00:19',
    genreBase: 'fantastique',
    producteur: 'Claude Opus 5 (chaîne pilote automatique)',
    pays: ['Japon'],
    technique: ['couleur']
  },
  {
    slug: 'les-maitres-du-temps',
    title: 'Les Maîtres du temps',
    director: 'René Laloux',
    year: 1982,
    summary: "Un enfant seul sur une planète hostile, une voix qui le guide depuis l'espace : Laloux et Mœbius font d'un roman populaire une boucle où l'on ne sauve personne sans finir par se retrouver soi-même.",
    url: 'films/les-maitres-du-temps.html',
    poster: 'assets/posters/les-maitres-du-temps.jpg',
    volet: 'critique',
    datePublication: '2026-09-28 21:04',
    genreBase: 'science-fiction',
    producteur: 'Claude Opus 5.5 (chaîne pilote automatique)',
    pays: ['France', 'Hongrie', 'Allemagne', 'Suisse', 'Royaume-Uni'],
    technique: ['couleur']
  },
  {
    slug: 'le-salaire-de-la-peur',
    title: 'Le Salaire de la peur',
    director: 'Henri-Georges Clouzot',
    year: 1953,
    summary: "Quatre hommes, deux camions, cinq cents kilomètres de piste : Clouzot fait de la nitroglycérine l'instrument de mesure exact de ce que vaut une vie, le jour où une compagnie pétrolière en fixe le prix.",
    url: 'films/le-salaire-de-la-peur.html',
    poster: 'assets/posters/le-salaire-de-la-peur.jpg',
    volet: 'critique',
    datePublication: '2026-09-29 23:16',
    genreBase: 'thriller',
    producteur: 'Claude Opus 5.5 (chaîne pilote automatique)',
    pays: ['France', 'Italie'],
    technique: ['n&b']
  }
];
