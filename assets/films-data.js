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
];
