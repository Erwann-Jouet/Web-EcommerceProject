#! /usr/bin/env python3
"""
WebTool - Gestionnaire de projet Web pour étudiants.

Ce script abstrait les commandes Git pour permettre aux étudiants
de travailler sur différentes branches (TP) sans connaître Git.
"""

import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import NoReturn


class ExitCode(Enum):
    """Codes de sortie du programme."""

    SUCCESS = 0
    ERROR = 1
    INVALID_USAGE = 2


class Color:
    """Codes ANSI pour la colorisation du terminal."""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


@dataclass
class Config:
    """Configuration du projet étudiant."""

    repository_url: str
    project_group_name: str
    branches: list[str]
    upstream_url: str | None = None
    members: dict[str, dict[str, str]] | None = None


class WebTool:
    """Gestionnaire principal des commandes webTool."""

    def __init__(self) -> None:
        """Initialise le gestionnaire webTool."""
        self.project_root = self._find_project_root()
        self.webtool_dir = self.project_root / ".webTool"
        self.projet_dir = self.project_root / "tp-projet"
        self.git_dir = self.projet_dir / ".git"
        self.config_file = self.webtool_dir / "config.json"
        self.config = self._load_config()
        self.ssh_dir = self.webtool_dir / ".ssh"
        self.ssh_key = self.ssh_dir / self.config.project_group_name

    def _find_project_root(self) -> Path:
        """
        Trouve la racine du projet en remontant l'arborescence.

        Returns:
            Path: Chemin absolu vers la racine du projet.

        Raises:
            SystemExit: Si le dossier .webTool n'est pas trouvé.
        """
        current = Path.cwd()

        for parent in [current, *current.parents]:
            webtool_dir = parent / ".webTool"
            if webtool_dir.is_dir():
                return parent

        self._print_error(
            "Erreur : Vous devez lancer webTool depuis le dossier du projet !"
        )
        self._print_info(
            "Assurez-vous d'être dans le dossier 'projet-web-groupeX/'"
        )
        sys.exit(ExitCode.ERROR.value)

    def _load_config(self) -> Config:
        """
        Charge la configuration depuis config.json.

        Returns:
            Config: Configuration du projet.

        Raises:
            SystemExit: Si la configuration est invalide.
        """
        if not self.config_file.exists():
            self._print_error(
                f"Erreur : Fichier de configuration introuvable : "
                f"{self.config_file}"
            )
            sys.exit(ExitCode.ERROR.value)

        try:
            with open(self.config_file, encoding="utf-8") as f:
                data = json.load(f)
                return Config(
                    repository_url=data["repository_url"],
                    project_group_name=data["project_group_name"],
                    branches=data["branches"],
                    upstream_url=data.get("upstream_url"),
                    members=data.get("members"),
                )
        except (json.JSONDecodeError, KeyError) as e:
            self._print_error(f"Erreur de configuration : {e}")
            sys.exit(ExitCode.ERROR.value)

    def _get_git_env(self) -> dict[str, str]:
        """
        Construit l'environnement pour les commandes Git.

        Returns:
            dict: Variables d'environnement pour Git.
        """
        env = os.environ.copy()
        env["GIT_DIR"] = str(self.git_dir)
        env["GIT_WORK_TREE"] = str(self.projet_dir)

        # Configuration SSH avec clé privée du projet
        if self.ssh_key.exists():
            env["GIT_SSH_COMMAND"] = (
                f'ssh -i "{self.ssh_key}" -o StrictHostKeyChecking=no '
                f'-o UserKnownHostsFile=/dev/null'
            )

        return env

    def _run_git(
        self, args: list[str], capture_output: bool = False
    ) -> subprocess.CompletedProcess[str]:
        """
        Execute une commande Git avec la configuration appropriée.

        Args:
            args: Arguments de la commande Git.
            capture_output: Si True, capture stdout et stderr.

        Returns:
            CompletedProcess: Résultat de la commande.

        Raises:
            SystemExit: Si Git n'est pas installé.
        """
        try:
            return subprocess.run(
                ["git", *args],
                env=self._get_git_env(),
                cwd=self.project_root,
                capture_output=capture_output,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            self._print_error(
                "Erreur : Git n'est pas installé sur votre ordinateur !"
            )
            self._print_info(
                "Téléchargez Git sur : https://git-scm.com/downloads"
            )
            sys.exit(ExitCode.ERROR.value)

    def _get_current_branch(self) -> str | None:
        """
        Récupère le nom de la branche courante.

        Returns:
            str | None: Nom de la branche ou None en cas d'erreur.
        """
        result = self._run_git(
            ["rev-parse", "--abbrev-ref", "HEAD"], capture_output=True
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None

    def _has_uncommitted_changes(self) -> bool:
        """
        Vérifie s'il y a des modifications non commitées.

        Returns:
            bool: True si des modifications existent.
        """
        result = self._run_git(["status", "--porcelain"], capture_output=True)
        return bool(result.stdout.strip())

    def _print_header(self, message: str) -> None:
        """Affiche un en-tête formaté."""
        print(f"\n{Color.BOLD}{Color.CYAN}═══ {message} ═══{Color.RESET}\n")

    def _print_success(self, message: str) -> None:
        """Affiche un message de succès."""
        print(f"{Color.GREEN}✓{Color.RESET} {message}")

    def _print_error(self, message: str) -> None:
        """Affiche un message d'erreur."""
        print(f"{Color.RED}✗{Color.RESET} {message}", file=sys.stderr)

    def _print_warning(self, message: str) -> None:
        """Affiche un avertissement."""
        print(f"{Color.YELLOW}⚠{Color.RESET} {message}")

    def _print_info(self, message: str) -> None:
        """Affiche une information."""
        print(f"{Color.BLUE}ℹ{Color.RESET} {message}")

    def cmd_status(self) -> None:
        """Affiche l'état actuel du projet."""
        self._print_header("État du projet")

        current_branch = self._get_current_branch()
        if current_branch:
            print(
                f"📍 Branche actuelle : "
                f"{Color.BOLD}{current_branch}{Color.RESET}"
            )
        else:
            self._print_error("Impossible de déterminer la branche actuelle")
            self._print_info(
                "Lancez './webTool init' pour initialiser le projet"
            )
            return

        if self._has_uncommitted_changes():
            self._print_warning("Vous avez des modifications non sauvegardées")
            print("\n📝 Fichiers modifiés :")
            self._run_git(["status", "--short"])
            print(
                f"\n💡 Utilisez {Color.BOLD}./webTool submit{Color.RESET} "
                f"pour sauvegarder"
            )
        else:
            self._print_success("Aucune modification en attente")

        # Vérifier si la branche locale est en retard par rapport à origin
        result = self._run_git(
            ["fetch", "origin", current_branch], capture_output=True
        )
        if result.returncode == 0:
            result = self._run_git(
                ["rev-list", "--count", f"HEAD..origin/{current_branch}"],
                capture_output=True,
            )
            if result.returncode == 0 and result.stdout.strip():
                behind_count = int(result.stdout.strip())
                if behind_count > 0:
                    self._print_warning(
                        f"Votre branche locale est en retard de "
                        f"{behind_count} commit(s)"
                    )
                    print(
                        f"💡 Utilisez {Color.BOLD}./webTool sync{Color.RESET} "
                        f"pour synchroniser avec le dépôt distant"
                    )

        print(
            f"\n🎯 Groupe : "
            f"{Color.BOLD}{self.config.project_group_name}{Color.RESET}"
        )
        print(f"🌿 Branches disponibles : {', '.join(self.config.branches)}")

    def cmd_init(self) -> None:
        """
        Initialise le projet en clonant le dépôt dans .webTool.
        """
        self._print_header("Initialisation du projet")
        if self.git_dir.exists():
            self._print_info(
                "Le dépôt est déjà initialisé dans le dossier 'tp-projet'."
            )
            return

        # Charger l'URL du dépôt depuis config.json
        repo_url = self.config.repository_url
        if not repo_url:
            repo_url = input(
                f"{Color.YELLOW}Entrez l'URL du dépôt à cloner : "
                f"{Color.RESET}"
            ).strip()
            if not repo_url:
                self._print_error("Aucune URL fournie, annulation.")
                return

        # Demander à l'étudiant de s'identifier parmi les membres
        user_login = None
        user_info = None
        if self.config.members:
            print(f"\n{Color.BOLD}👥 Membres du projet :{Color.RESET}\n")
            logins = list(self.config.members.keys())
            for i, login in enumerate(logins, 1):
                member = self.config.members[login]
                firstname = member.get("firstname", "")
                lastname = member.get("lastname", "")
                print(f"  {i}. {login} - {firstname} {lastname}")

            print()
            while True:
                choice = input(
                    f"{Color.YELLOW}Entrez votre numéro (1-{len(logins)}) "
                    f"ou votre login : {Color.RESET}"
                ).strip()

                # Vérifier si c'est un numéro
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(logins):
                        user_login = logins[idx]
                        user_info = self.config.members[user_login]
                        break
                # Vérifier si c'est un login
                elif choice in self.config.members:
                    user_login = choice
                    user_info = self.config.members[choice]
                    break
                else:
                    self._print_error("Choix invalide. Veuillez réessayer.")

            # Confirmer l'identité
            firstname = user_info.get("firstname", "")
            lastname = user_info.get("lastname", "")
            email = user_info.get("email", "")
            print(
                f"\n{Color.GREEN}✓{Color.RESET} Vous êtes : "
                f"{Color.BOLD}{firstname} {lastname}{Color.RESET} "
                f"({email})"
            )

        # Créer le dossier 'tp-projet' si nécessaire
        self.projet_dir.mkdir(exist_ok=True)

        # Cloner le dépôt dans 'tp-projet' en forçant la clé SSH locale
        self._print_info("Clonage du dépôt dans le dossier 'tp-projet'...")
        git_env = os.environ.copy()
        if self.ssh_key.exists():
            git_env["GIT_SSH_COMMAND"] = (
                f'ssh -i "{self.ssh_key}" -o IdentitiesOnly=yes '
                f"-o StrictHostKeyChecking=no "
                f"-o UserKnownHostsFile=/dev/null"
            )
        result = subprocess.run(
            ["git", "clone", repo_url, str(self.projet_dir)],
            cwd=self.project_root,
            env=git_env,
            check=False,
        )
        if result.returncode != 0:
            self._print_error(
                "Échec du clonage du dépôt ! "
                "Vérifiez l'URL ou votre connexion internet."
            )
            return

        # Configurer Git avec les informations de l'utilisateur
        if user_info:
            firstname = user_info.get("firstname", "")
            lastname = user_info.get("lastname", "")
            email = user_info.get("email", "")
            full_name = f"{firstname} {lastname}".strip()

            self._print_info("Configuration de votre identité Git...")
            self._run_git(["config", "user.name", full_name])
            self._run_git(["config", "user.email", email])
            self._print_success(f"Identité configurée : {full_name} <{email}>")

        self._print_success(
            "Dépôt cloné et initialisé dans le dossier 'tp-projet' !"
        )
        print(
            f"\n💡 Vous pouvez maintenant modifier les fichiers dans le "
            f"dossier 'tp-projet' et utiliser "
            f"{Color.BOLD}'./webTool go <branche>'{Color.RESET} "
            f"pour changer de branche."
        )

    def cmd_go(self, branch: str) -> None:
        """
        Change de branche de travail.

        Args:
            branch: Nom de la branche cible.
        """
        if branch not in self.config.branches:
            self._print_error(f"Branche inconnue : {branch}")
            self._print_info(
                f"Branches disponibles : {', '.join(self.config.branches)}"
            )
            sys.exit(ExitCode.INVALID_USAGE.value)

        current_branch = self._get_current_branch()
        if current_branch == branch:
            self._print_info(f"Vous êtes déjà sur la branche {branch}")
            return

        # Affichage minimal
        self._print_header(f"Changement vers : {branch}")

        # Vérifier les modifications non commitées
        if self._has_uncommitted_changes():
            self._print_warning(
                "Vous avez des modifications non sauvegardées !"
            )
            response = (
                input(
                    "Voulez-vous sauvegarder ces modifications avant de "
                    "changer de branche ? (o/N) : "
                )
                .strip()
                .lower()
            )
            if response in ("o", "oui", "y", "yes"):
                self._commit_changes(
                    f"Sauvegarde automatique avant passage à {branch}"
                )
            else:
                result = self._run_git(
                    ["stash", "push", "-u"], capture_output=True
                )
                if result.returncode != 0:
                    self._print_error(
                        "Échec de la mise de côté des modifications"
                    )
                    sys.exit(ExitCode.ERROR.value)

        # Changer de branche (sortie masquée)
        result = self._run_git(["checkout", branch], capture_output=True)
        if result.returncode != 0:
            self._print_error(f"Échec du changement vers {branch}")
            sys.exit(ExitCode.ERROR.value)

        # Récupérer les dernières modifications du dépôt (sortie masquée)
        result = self._run_git(["pull", "origin", branch], capture_output=True)
        if result.returncode != 0:
            self._print_warning(
                "La branche distante n'existe pas ou n'est pas à jour. "
                "Travail en local."
            )

        # Nettoyage des fichiers/dossiers non suivis
        # (pour éviter les restes d'une branche à l'autre)
        subprocess.run(
            ["git", "clean", "-fdx"], cwd=self.projet_dir, check=False
        )
        self._print_success(f"Vous êtes maintenant sur la branche {branch}")
        print(
            f"\n💡 Lancez {Color.BOLD}./webTool submit{Color.RESET} "
            f"pour sauvegarder vos modifications"
        )

    def _commit_changes(self, message: str) -> None:
        """
        Commit les modifications actuelles.

        Args:
            message: Message du commit.
        """
        self._run_git(["add", "-A"])
        result = self._run_git(["commit", "-m", message])
        if result.returncode == 0:
            self._print_success("Modifications commitées")

    def cmd_submit(self, title: str | None = None) -> None:
        """Sauvegarde et envoie les modifications sur GitLab."""
        self._print_header("Sauvegarde de vos modifications")

        current_branch = self._get_current_branch()
        if not current_branch:
            self._print_error("Impossible de déterminer la branche actuelle")
            sys.exit(ExitCode.ERROR.value)

        if not self._has_uncommitted_changes():
            self._print_info("Aucune modification à sauvegarder")
            # Vérifier s'il y a des commits non pushés
            result = self._run_git(
                ["rev-list", "--count", f"origin/{current_branch}..HEAD"],
                capture_output=True,
            )
            if result.returncode == 0 and result.stdout.strip() == "0":
                self._print_success("Tout est déjà à jour sur GitLab")
                return

        # Commit des modifications
        if self._has_uncommitted_changes():
            print("\n📝 Fichiers à sauvegarder :")
            self._run_git(["status", "--short"])
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if title is None:
                print(
                    f"\n{Color.BOLD}📝 Consignes pour le titre :{Color.RESET}"
                )
                print(
                    "  • Commencez par le code de la user story "
                    "(ex: TP.US1, PRJ.US2)"
                )
                print("  • Choisissez un titre court et explicite")
                print("  • Si pas fini, commencez par WIP (Work In Progress)")
                print(
                    "  • Évitez les titres génériques "
                    "(sauvegarde, modif, test)"
                )
                print(f"\n  {Color.CYAN}Exemple :{Color.RESET}\n")
                print("     TP.US3 : Correction bug affichage fiche produit")
                print("     WIP PRJ.US2 : Développement en cours\n")
                title = input(
                    f"{Color.YELLOW}Titre de la sauvegarde : {Color.RESET}"
                ).strip()
            commit_message = title if title else f"Travail du {timestamp}"
            self._commit_changes(commit_message)

        # Push vers GitLab
        self._print_info("Envoi des modifications sur GitLab...")
        result = self._run_git(["push", "origin", current_branch])
        if result.returncode != 0:
            self._print_error("Échec de l'envoi sur GitLab")
            self._print_info(
                "Vérifiez votre connexion internet ou contactez "
                "votre enseignant"
            )
            sys.exit(ExitCode.ERROR.value)

        self._print_success(
            f"Modifications envoyées avec succès sur la branche "
            f"{current_branch} !"
        )
        print("\n🧪 Les tests automatiques vont se lancer sur GitLab")
        print(f"📊 Consultez les résultats sur : {self.config.repository_url}")

    def cmd_history(self) -> None:
        """Affiche la liste des titres des commits de la branche courante."""
        current_branch = self._get_current_branch()
        if not current_branch:
            self._print_error("Impossible de déterminer la branche actuelle")
            return
        self._print_header(f"Historique des sauvegardes ({current_branch})")
        result = self._run_git(
            [
                "log",
                "--pretty=format:%s (%ad)",
                "--date=format:%Y-%m-%d %H:%M:%S",
                current_branch,
            ],
            capture_output=True,
        )
        if result.returncode != 0 or not result.stdout.strip():
            self._print_info("Aucun commit trouvé.")
            return
        lines = result.stdout.strip().splitlines()
        # Inverser la liste pour afficher du plus ancien au plus récent
        lines.reverse()
        for i, line in enumerate(lines, 1):
            # Cherche la date et l'heure entre parenthèses
            m = re.search(
                r"\((\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})\)$", line
            )
            if m:
                date_fr = (
                    f"{m.group(3)}-{m.group(2)}-{m.group(1)} "
                    f"{m.group(4)}:{m.group(5)}:{m.group(6)}"
                )
                titre = line[: m.start()].strip()
                print(f"> {i:2d}:  {titre} {date_fr}")
            else:
                print(f"> {i:2d}:  {line}")

    def cmd_help(self) -> None:
        help_text = f"""
        {Color.BOLD}{Color.CYAN}
        ╔════════════════════════════════════════════════╗
        ║       WebTool - Gestionnaire de projet         ║
        ║          {self.config.project_group_name} - Web 2025        ║
        ╚════════════════════════════════════════════════╝{Color.RESET}

        {Color.BOLD}📚 Commandes disponibles :{Color.RESET}

        {Color.BOLD}./webTool init{Color.RESET}
            → Initialise le projet en clonant le dépôt du projet dans le
              dossier 'tp-projet'
            → À lancer une seule fois au début d'une séance de TP

        {Color.BOLD}./webTool status{Color.RESET}
            → Affiche la branche actuelle et l'état du projet

        {Color.BOLD}./webTool go <branche>{Color.RESET}
            → Change de branche (tp ou projet)
            → Sauvegarde automatiquement vos modifications

        {Color.BOLD}./webTool submit [titre]{Color.RESET}
            → Sauvegarde et envoie vos modifications
            → Vous pouvez donner un titre en argument, ou il vous sera
              demandé lors de la sauvegarde

        {Color.BOLD}📝 Recommandations pour le titre de sauvegarde :{Color.RESET}
                • Commencez par le code de la user story concernée par le rendu
                    (ex : 'TP.US1', 'TP.US2', 'PRJ.US1', 'PRJ.US2')
                •  Choisissez un titre court et explicite
                    (ex : 'Correction bug login', 'Ajout page profil',
                     'Finalisation TP')
                • Le titre doit permettre de garder une mémoire de ce qui a
                  été fait
                • Évitez les titres trop génériques comme 'sauvegarde',
                  'modif', 'test'
                • Si une user story n'est pas finie, commencez par WIP
                  (comme pour Work In Progress)

        {Color.BOLD}./webTool history{Color.RESET}
            → Affiche la liste des sauvegardes (titre, date, heure) du
              projet, sans hash

        {Color.BOLD}./webTool update{Color.RESET}
            → Récupère les mises à jour de l'enseignant
            → À utiliser uniquement si demandé par votre enseignant

        {Color.BOLD}./webTool help{Color.RESET}
            → Affiche cette aide

        {Color.BOLD}📋 Exemple d'utilisation :{Color.RESET}

            ./webTool init         # Initialiser le projet (à faire une fois)
            ./webTool go tp        # Commencer le TP
            # ... Vous codez ...
            ./webTool submit "TP.US1 : Correction bug login"
                                   # Sauvegarder avec un titre
            ./webTool submit       # Sauvegarder, le titre sera demandé
                                   # en ligne de commande

            ./webTool history      # Afficher l'historique des sauvegardes

            ./webTool go projet    # Passer au projet
            ./webTool submit       # Sauvegarder le projet

        Exemple d'affichage de ./webTool history :
            >  1 TP.US1 : Correction bug login 07-11-2025 14:32:10
            >  2 TP.US2 : Ajout page profil 07-11-2025 15:10:05
            >  3 WIP TP.US3 : User story en cours de développement
                              07-11-2025 15:55:05
            >  4 TP.US3 : Finalisation User story 10-11-2025 16:00:00

        {Color.BOLD}⚠️  Important :{Color.RESET}
            • Lancez toujours webTool depuis la racine du projet !
            • N'oubliez pas de faire './webTool submit' dès que vous avez terminé une user story ou à la fin d'une séance de TP.
            • Les modifications non sauvegardées peuvent être perdues

        {Color.BOLD}💡 Astuces :{Color.RESET}
            • Faites des sauvegardes fréquentes avec 'submit'
            • Utilisez 'status' pour voir où vous en êtes
            • En cas de problème, contactez votre enseignant

        {Color.BOLD}🌿 Branches disponibles :{Color.RESET} {', '.join(self.config.branches)}
        """

        print(help_text)

    def cmd_sync(self) -> None:
        """Synchronise le dépôt local avec le dépôt distant (origin)."""
        self._print_header("Synchronisation avec le dépôt distant")

        current_branch = self._get_current_branch()
        if not current_branch:
            self._print_error("Impossible de déterminer la branche actuelle")
            sys.exit(ExitCode.ERROR.value)

        # Avertir l'étudiant des modifications non sauvegardées
        if self._has_uncommitted_changes():
            self._print_warning(
                "Vous avez des modifications non sauvegardées qui seront perdues !"
            )
            print("\n📝 Fichiers modifiés :")
            self._run_git(["status", "--short"])
            response = (
                input(
                    f"\n{Color.YELLOW}Voulez-vous vraiment synchroniser ? "
                    f"Les modifications locales seront perdues (o/N) : {Color.RESET}"
                )
                .strip()
                .lower()
            )
            if response not in ("o", "oui", "y", "yes"):
                self._print_info("Synchronisation annulée")
                return

            # Annuler toutes les modifications locales
            self._print_info("Annulation des modifications locales...")
            self._run_git(["reset", "--hard", "HEAD"])
            self._run_git(["clean", "-fd"])

        # Récupérer les dernières modifications du dépôt distant
        self._print_info(
            f"Récupération des modifications de la branche {current_branch}..."
        )
        result = self._run_git(["fetch", "origin", current_branch])
        if result.returncode != 0:
            self._print_error("Échec de la récupération des modifications")
            self._print_info(
                "Vérifiez votre connexion internet ou contactez "
                "votre enseignant"
            )
            sys.exit(ExitCode.ERROR.value)

        # Réinitialiser la branche locale à l'état du dépôt distant
        result = self._run_git(
            ["reset", "--hard", f"origin/{current_branch}"],
            capture_output=True,
        )
        if result.returncode != 0:
            self._print_error("Échec de la synchronisation")
            sys.exit(ExitCode.ERROR.value)

        self._print_success(
            f"Branche {current_branch} synchronisée avec le dépôt distant !"
        )
        print(
            "\n💡 Vous pouvez maintenant continuer votre travail "
            "avec la dernière version"
        )

    def cmd_update(self) -> None:
        """Récupère les mises à jour du dépôt enseignant (upstream)."""
        self._print_header("Mise à jour des fichiers de base")

        # Vérifier si upstream est configuré
        if not self.config.upstream_url:
            self._print_warning(
                "Aucun dépôt de mise à jour configuré pour ce projet"
            )
            self._print_info(
                "Cette fonctionnalité est utilisée uniquement si l'enseignant "
                "doit corriger ou mettre à jour les fichiers de départ"
            )
            return

        current_branch = self._get_current_branch()
        if not current_branch:
            self._print_error("Impossible de déterminer la branche actuelle")
            sys.exit(ExitCode.ERROR.value)

        # Avertir l'étudiant
        self._print_warning(
            "Votre enseignant a publié une mise à jour des fichiers de base"
        )
        print(
            f"\n📌 Branche actuelle : {Color.BOLD}{current_branch}{Color.RESET}"
        )

        # Vérifier les modifications locales
        if self._has_uncommitted_changes():
            self._print_warning("Vous avez des modifications non sauvegardées")
            print("\n💡 Il est recommandé de sauvegarder avant la mise à jour")

            response = (
                input(
                    f"\n{Color.YELLOW}Voulez-vous sauvegarder maintenant ? (o/N) : "
                    f"{Color.RESET}"
                )
                .strip()
                .lower()
            )

            if response in ("o", "oui", "y", "yes"):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._commit_changes(
                    f"Sauvegarde avant mise à jour - {timestamp}"
                )
            else:
                self._print_warning(
                    "Vous conservez vos modifications non sauvegardées"
                )
                print("⚠️  En cas de conflit, elles seront préservées\n")

        # Confirmer l'action
        response = (
            input(
                f"{Color.CYAN}Voulez-vous récupérer la mise à jour ? (o/N) : "
                f"{Color.RESET}"
            )
            .strip()
            .lower()
        )

        if response not in ("o", "oui", "y", "yes"):
            self._print_info("Mise à jour annulée")
            return

        # Vérifier si upstream existe déjà
        result = self._run_git(
            ["remote", "get-url", "upstream"], capture_output=True
        )

        if result.returncode != 0:
            # Ajouter upstream
            self._print_info("Configuration du dépôt de mise à jour...")
            result = self._run_git(
                ["remote", "add", "upstream", self.config.upstream_url]
            )
            if result.returncode != 0:
                self._print_error(
                    "Impossible d'ajouter le dépôt de mise à jour"
                )
                sys.exit(ExitCode.ERROR.value)

        # Fetch upstream
        self._print_info("Récupération des mises à jour...")
        result = self._run_git(["fetch", "upstream"])
        if result.returncode != 0:
            self._print_error("Impossible de récupérer les mises à jour")
            self._print_info(
                "Vérifiez votre connexion internet ou contactez "
                "votre enseignant"
            )
            sys.exit(ExitCode.ERROR.value)

        # Merge upstream
        self._print_info(
            f"Application des mises à jour sur {current_branch}..."
        )
        result = self._run_git(
            ["merge", f"upstream/{current_branch}", "--no-edit"],
            capture_output=True,
        )

        if result.returncode != 0:
            # Vérifier s'il y a des conflits
            status_result = self._run_git(
                ["status", "--porcelain"], capture_output=True
            )

            if "UU" in status_result.stdout or "AA" in status_result.stdout:
                self._print_error("⚠️  Conflit détecté !")
                print(
                    f"\n{Color.YELLOW}Des fichiers ont été modifiés à la fois par "
                    f"vous et par votre enseignant.{Color.RESET}\n"
                )

                print("📝 Fichiers en conflit :")
                self._run_git(["diff", "--name-only", "--diff-filter=U"])

                print(f"\n{Color.BOLD}Comment résoudre :{Color.RESET}")
                print(
                    "1. Ouvrez les fichiers listés ci-dessus dans votre éditeur"
                )
                print("2. Cherchez les marqueurs de conflit : <<<<<<< HEAD")
                print(
                    "3. Choisissez quelle version garder (la vôtre ou celle du prof)"
                )
                print("4. Supprimez les marqueurs de conflit")
                print(
                    f"5. Lancez : {Color.BOLD}./webTool submit{Color.RESET}\n"
                )

                self._print_warning(
                    "Si vous avez besoin d'aide, contactez votre enseignant"
                )
            else:
                self._print_error("Échec de la mise à jour")
                self._print_info("Contactez votre enseignant pour assistance")

            sys.exit(ExitCode.ERROR.value)

        self._print_success("Mise à jour appliquée avec succès !")

        # Afficher ce qui a changé
        result = self._run_git(
            ["log", "--oneline", "HEAD@{{1}}..HEAD"], capture_output=True
        )

        if result.stdout.strip():
            print("\n📋 Modifications de l'enseignant :")
            print(result.stdout)

        print("\n💡 Vous pouvez maintenant continuer votre travail")
        print(
            f"💾 N'oubliez pas de faire {Color.BOLD}./webTool submit{Color.RESET} "
            f" dès que vous avez terminé une user story ou à la fin d'une séance de TP.\n"
        )

    def run(self, args: list[str]) -> None:
        """
        Point d'entrée principal du programme.

        Args:
            args: Arguments de la ligne de commande (sans le nom du script).
        """
        if not args or args[0] in ("help", "--help", "-h"):
            self.cmd_help()
            return

        command = args[0]

        match command:
            case "status":
                self.cmd_status()
            case "go":
                if len(args) < 2:
                    self._print_error("Usage : ./webTool go <branche>")
                    self._print_info(
                        f"Branches : {', '.join(self.config.branches)}"
                    )
                    sys.exit(ExitCode.INVALID_USAGE.value)
                self.cmd_go(args[1])
            case "submit":
                # Récupérer le titre optionnel
                title = " ".join(args[1:]).strip() if len(args) > 1 else None
                # Si le titre est vide, le mettre à None pour forcer la demande
                if title == "":
                    title = None
                self.cmd_submit(title)
            case "history":
                self.cmd_history()
            case "sync":
                self.cmd_sync()
            case "update":
                self.cmd_update()
            case "init":
                self.cmd_init()
            case _:
                self._print_error(f"Commande inconnue : {command}")
                self._print_info(
                    "Lancez './webTool help' pour voir les commandes disponibles"
                )
                sys.exit(ExitCode.INVALID_USAGE.value)


def main() -> NoReturn:
    """Point d'entrée du programme."""
    try:
        tool = WebTool()
        # Ajout automatique de la clé SSH du projet à l'agent SSH
        if tool.ssh_key.exists():
            # Vérifier si la clé est déjà chargée dans l'agent SSH
            result = subprocess.run(
                ["ssh-add", "-l"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                check=False,
            )

            # Vérifier si la clé du projet est déjà dans l'agent
            key_loaded = False
            if result.returncode == 0:
                # Extraire l'empreinte de la clé du projet
                key_fingerprint_result = subprocess.run(
                    ["ssh-keygen", "-lf", str(tool.ssh_key)],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    check=False,
                )
                if key_fingerprint_result.returncode == 0:
                    key_fingerprint = key_fingerprint_result.stdout.split()[1]
                    if key_fingerprint in result.stdout:
                        key_loaded = True

            # Ajouter la clé seulement si elle n'est pas déjà chargée
            if not key_loaded:
                subprocess.run(
                    ["ssh-add", str(tool.ssh_key)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
        tool.run(sys.argv[1:])
        sys.exit(ExitCode.SUCCESS.value)
    except KeyboardInterrupt:
        print(f"\n\n{Color.YELLOW}Interruption par l'utilisateur{Color.RESET}")
        sys.exit(ExitCode.ERROR.value)
    except Exception as e:
        print(
            f"{Color.RED}Erreur inattendue : {e}{Color.RESET}",
            file=sys.stderr,
        )
        sys.exit(ExitCode.ERROR.value)


if __name__ == "__main__":
    main()
