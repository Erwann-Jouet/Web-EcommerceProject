════════════════════════════════════════════════════════════════
    PROJET WEB - GUIDE DE DÉMARRAGE RAPIDE
════════════════════════════════════════════════════════════════

Bienvenue dans votre projet Web ! Ce document explique comment 
utiliser l'outil webTool pour travailler sur vos TPs.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 PRÉREQUIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Avant de commencer, assurez-vous d'avoir installé :

1. Git : https://git-scm.com/downloads
2. Python 3.8+ : https://www.python.org/downloads/

Pour vérifier :
  git --version
  python3 --version    (Linux/Mac)
  python --version     (Windows)

Il faut également connaître votre **passphrase**. Il est disponible dans votre home du site https://pwa-dashboard.istic.univ-rennes1.fr/

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 DÉMARRAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Décompressez le fichier ZIP dans un dossier de votre choix
2. Ouvrez un terminal dans ce dossier
3. Tapez : ./webTool help    (Linux/Mac)
         ou : webTool help    (Windows)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💻 COMMANDES PRINCIPALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

./webTool init
  → Initialise le projet en clonant le dépôt dans le dossier 'projet'
  → À lancer une seule fois au début d'une séance de TP

./webTool status
  → Voir sur quelle branche vous êtes et l'état du projet

./webTool go tp
  → Passer au TP

./webTool submit [titre]
  → Sauvegarder et envoyer vos modifications
  → Vous pouvez donner un titre en argument, ou il vous sera demandé lors de la sauvegarde
  → Recommandations de rédaction du titre : 
    • Commencer par le code de la user story concernée par le rendu
          (ex : 'TP.US1', 'TP.US2', 'PRJ.US1', 'PRJ.US2')
    • Suivi d'un court descriptif de ce qui a été fait
          (ex : 'Correction bug login', 'Ajout page profil', 'Finalisation TP')
    • Le titre doit permettre de garder une mémoire de ce qui a été fait
    • Évitez les titres trop génériques comme 'sauvegarde', 'modif', 'test'
    • Si une user story n'est pas finie, commencez par WIP (comme pour Work In Progress)

./webTool history
  → Affiche la liste des sauvegardes (titre, date, heure) du projet, sans hash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔎 EXEMPLE HISTORIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Après plusieurs sauvegardes, la commande ./webTool history affiche :

>  1 TP.US1 : Correction bug login 07-11-2025 14:32:10
>  2 TP.US2 : Ajout page profil 07-11-2025 15:10:05
>  3 WIP TP.US3 : User story en cours de développement 07-11-2025 15:55:05
>  4 TP.US3 : Finalisation User story 10-11-2025 16:00:00

./webTool update
  → Récupérer une mise à jour de votre enseignant
  → À utiliser uniquement si demandé par votre enseignant

./webTool help
  → Afficher l'aide complète

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 WORKFLOW TYPIQUE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Initialiser le projet (à faire une fois au début) :
   ./webTool init

2. Commencer les activités du cycle TP :
   ./webTool go tp

3. Coder votre solution
   (modifiez les fichiers dans le projet)

4. Sauvegarder à la fin de chaque user story ou à la fin d'une séance de TP :
   ./webTool submit

5. Passer au cycle PROJET :
   ./webTool go projet

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  IMPORTANT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Lancez TOUJOURS webTool depuis la RACINE du projet
• Faites des sauvegardes (submit) A LA FIN DE CHAQUE US terminé ou à la fin d'une séance de TP
• Ne modifiez PAS le dossier .webTool/ (caché)
• Si vous changez d'ordinateur, emportez TOUT le dossier

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🆘 PROBLÈMES FRÉQUENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"command not found: webTool"
  → Vous n'êtes pas dans le bon dossier. Allez à la racine
     du projet (là où se trouve le fichier webTool)

"Git n'est pas installé"
  → Installez Git depuis https://git-scm.com/downloads

"Python n'est pas installé"
  → Installez Python depuis https://www.python.org/downloads/

"Échec de l'envoi sur GitLab"
  → Vérifiez votre connexion internet
  → Contactez votre enseignant si le problème persiste

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📞 BESOIN D'AIDE ?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

En cas de problème, contactez votre enseignant en indiquant :
• Le message d'erreur complet
• La commande que vous avez tapée
• Votre numéro de groupe

Bon courage ! 🎓

