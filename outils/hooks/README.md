# outils/hooks/ -- hook pre-push de la surface PILOTE

> **COPIE DATEE** du 2026-09-18 de
> `C:\Users\cdats\Claude\CIN\analyses-de-films\outils\hooks\README.md`
> (depot de production) -- divergence non detectee automatiquement.
> BKL-CIN-096 (b) lot 5, T1.3. Les ecarts au texte de production sont nommes
> un a un ci-dessous ; le reste est repris tel quel.

Un hook git `pre-push` versionne dans le depot, qui rejoue une batterie de
controle avant tout push vers `main`. Decision RUN-001 (revue S3 du
31/07/2026, option B de `PROPOSITION-2026-07-29-CI-PUBLICATION.md`),
transposee ici.

## Ce qu'il fait, et ce qu'il ne fait pas

- Il ne regarde QUE les pushes vers `refs/heads/main`. Un push vers toute
  autre branche sort immediatement, sans rien lire ni afficher. C'est ce qui
  rend possible la conduite d'echec de la chaine pilote : un echec se commite
  sur une branche locale `echec-<slug>-<AAAAMMJJ>`, qui n'est jamais poussee.
- Avant de lancer la batterie sur un push vers main, il exige un arbre de
  travail propre (`git status --porcelain` vide). Les scripts de controle
  lisent les fichiers du disque, pas l'objet git du commit pousse : un arbre
  sale controlerait autre chose que ce qui part reellement en ligne.
- Il ne modifie AUCUN fichier du depot (tous les scripts tournent en mode
  lecture seule : `--strict`, `--verifier`, `--simuler`).
- Il ne touche pas aux scripts de controle de `outils\` : s'ils revelent un
  defaut, c'est signale, jamais corrige a la volee.

## Activation (geste separe, PAS fait par ce depot de fichiers)

```
git config core.hooksPath outils/hooks
```

A executer une fois par clone/poste. Sans cette commande, le hook existe dans
le depot mais n'est pas actif. Pour revenir au comportement par defaut de git
(`.git/hooks/`) :

```
git config --unset core.hooksPath
```

## Batterie jouee (dans l'ordre, sur push vers main uniquement)

1. `controle-vocabulaires.py --strict` -- axes fermes du registre (P-10),
   lus dans le `assets/vocabulaires.js` **du depot pilote**.
2. `genere-liste-pilote.py --verifier` -- pas de derive entre le HTML en dur
   d'`index.html` et le gabarit qui l'a produit. **ECART NOMME** : la
   production appelle ici `genere-liste-statique.py` (trois pages de liste) ;
   le pilote n'en a qu'une, et son generateur lui est propre.
3. `recompresse-affiches.py --seuil 300 --simuler` -- aucune affiche
   au-dessus de 300 Ko (P-36), verifie sans rien reecrire. **ECART NOMME** :
   `assets/posters` absent vaut 0 affiche a controler, donc succes -- la
   decision (3) d'AH du 18/09/2026 fait de "sans affiche" un cas nominal du
   pilote. Le seuil, lui, est celui de la production.
4. `controle-contraste.py` -- gate uniquement sur les ecarts CERTAINS (E1).
   Les ecarts PROBABLES (E2) restent affiches mais ne bloquent jamais.
   **ECART NOMME** : `films/` absent vaut 0 page d'analyse a balayer, et
   `404.html` entre au perimetre a cote d'`index.html`.

`controle-glyphes.py` reste EXCLU, pour le motif du depot de production : il
ne controle pas les pages du site et depend du reseau.

Echec de n'importe quel controle -> push refuse, avec le detail imprime par
le script lui-meme.

## La baseline E1 part VIDE, et c'est une decision

`baseline-e1.txt` ne porte **aucune** ligne d'ecart : le pilote n'herite
d'aucun des 14 E1 esthetiques de la production. Consequence immediate :
**tolerance zero**. Tout E1 mesure sur une page de cette surface est un E1
NOUVEAU et refuse le push. Une ligne ne s'ajoute a ce fichier que sur gate
d'AH -- jamais par la chaine pilote elle-meme, qui publie sans relecture.

## Si python est absent ou casse sur le poste

Le hook laisse alors le push vers main PASSER, avec un avertissement fort en
sortie d'erreur (arbitrage AH du 31/07/2026, repris tel quel). Corrige
l'environnement avant la publication suivante : aucun controle n'aura ete
rejoue.

## Contournement exceptionnel -- INTERDIT A LA CHAINE PILOTE

```
git push --no-verify
```

Le gate ne s'interdit jamais techniquement -- doctrine de gates, pas de
verrous. Mais **la skill `analyse-films-pilote` n'a pas le droit d'y
recourir** : une chaine qui publie sans relecture humaine ne peut pas, en
plus, court-circuiter le seul controle mecanique qui la precede. Hook refuse
= ARRET, jamais contournement.
