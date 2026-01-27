#!/usr/bin/env python3
# Darkelf Retro AI — Enhanced Edition

import os
import sys
import json
import time
import requests
import subprocess
import threading
import webbrowser
from collections import deque
from dataclasses import dataclass
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.prompt import Prompt
from rich.spinner import Spinner

# =========================
# GLOBALS / CONSTANTS
# =========================

APP_NAME = "Darkelf Retro AI"
ARCHIVE_API = "https://archive.org/advancedsearch.php"
OLLAMA_MODEL = "llama3"

console = Console()

online = False
last_results = []
last_query = None
ai_memory = []

ASCII_ART = r"""
██████╗  █████╗ ██████╗ ██╗  ██╗███████╗██╗     ███████╗
██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║     ██╔════╝
██║  ██║███████║██████╔╝█████╔╝ █████╗  ██║     █████╗  
██║  ██║██╔══██║██╔══██╗██╔═██╗ ██╔══╝  ██║     ██╔══╝  
██████╔╝██║  ██║██║  ██║██║  ██╗███████╗███████╗██╗
╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝══╝
"""

# =========================
# NETWORK CHECK
# =========================

def check_online():
    global online
    try:
        requests.get(
            "https://archive.org/metadata/opensource",
            timeout=4,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        online = True
    except requests.RequestException:
        online = False


def network_status():
    return "[green]ONLINE[/green]" if online else "[red]OFFLINE[/red]"

# =========================
# DATA STRUCTURES
# =========================

@dataclass
class Result:
    title: str
    url: str
    year: Optional[str] = None
    mediatype: Optional[str] = None

# =========================
# ARCHIVE SEARCH
# =========================

def archive_search(query: str, rows=10) -> List[Result]:
    params = {
        "q": query,
        "output": "json",
        "rows": rows,
        "fl[]": ["title", "year", "mediatype", "identifier"]
    }

    r = requests.get(ARCHIVE_API, params=params, timeout=10)
    r.raise_for_status()

    docs = r.json()["response"]["docs"]

    results = []
    for d in docs:
        results.append(
            Result(
                title=d.get("title", "Unknown"),
                year=d.get("year"),
                mediatype=d.get("mediatype"),
                url=f"https://archive.org/details/{d.get('identifier')}"
            )
        )
    return results

# =========================
# DISPLAY RESULTS
# =========================

def show_results(results: List[Result]):
    if not results:
        console.print("\n[bold red]NO RESULTS FOUND[/bold red]")
        console.print("[dim]The Internet Archive returned zero matches.[/dim]")
        console.print("[dim]Try broader keywords or a different query.[/dim]\n")
        return

    table = Table(
        title="Results",
        header_style="bold cyan",
        border_style="green",
        show_lines=True
    )

    table.add_column("#", style="yellow", justify="right", width=3)
    table.add_column("Title", overflow="fold")
    table.add_column("Year", width=6, justify="center")
    table.add_column("Type", width=10, justify="center")

    for i, r in enumerate(results, 1):
        table.add_row(
            str(i),
            r.title,
            str(r.year or ""),
            r.mediatype or ""
        )

    console.print(table)
    console.print("[dim]Shortcuts: [a] ask AI | [o] open | [q] back[/dim]")

# =========================
# AI ENGINE
# =========================

def ai_stream(prompt: str, mode="FREEFORM"):
    identity = f"""
You are Darkelf Retro AI.
Focus on retro computing, emulation, and digital preservation.
Output Mode: {mode}
Be concise, factual, and structured when possible.
"""

    full_prompt = identity + "\n\n" + prompt
    cmd = ["ollama", "run", OLLAMA_MODEL, full_prompt]

    text = Text()
    with Live(text, refresh_per_second=8, console=console):
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        for line in proc.stdout:
            text.append(line)

    ai_memory.append(prompt)

# =========================
# RESULT → AI HANDOFF
# =========================

def ask_about_result(r: Result):
    mode = Prompt.ask(
        "AI Mode",
        choices=["FREEFORM", "FACT_SHEET", "TIMELINE"],
        default="FACT_SHEET"
    )

    prompt = f"""
Analyze this archival item:

Title: {r.title}
Year: {r.year}
Type: {r.mediatype}
URL: {r.url}

Explain its historical relevance and technical context.
"""
    ai_stream(prompt, mode=mode)

# =========================
# MAIN MENU
# =========================

def main_menu():
    global last_results, last_query

    while True:
        check_online()

        console.clear()
        console.print(ASCII_ART, style="green")

        console.print(Panel(
            "[1] Search Internet Archive\n"
            "[2] Ask Retro AI\n"
            "[3] Repeat Last Search\n"
            "[q] Quit\n\n"
            f"Network: {network_status()}",
            title=APP_NAME,
            style="green"
        ))

        choice = Prompt.ask("Select")

        if choice == "1":
            if not online:
                console.print("[red]Offline mode — archive search unavailable[/red]")
                Prompt.ask("[dim]Press Enter to continue[/dim]", default="")
                continue

            query = Prompt.ask("Search query")
            last_query = query

            with console.status("Searching archive...", spinner="dots"):
                last_results = archive_search(query)

            show_results(last_results)

            # 🔥 FIX: do NOT enter action loop if no results
            if not last_results:
                Prompt.ask("[dim]Press Enter to return to menu[/dim]", default="")
                continue

            while True:
                cmd = Prompt.ask("Action", default="q")
                if cmd == "q":
                    break
                elif cmd == "a":
                    idx = int(Prompt.ask("Item number")) - 1
                    if 0 <= idx < len(last_results):
                        ask_about_result(last_results[idx])
                elif cmd == "o":
                    idx = int(Prompt.ask("Item number")) - 1
                    if 0 <= idx < len(last_results):
                        webbrowser.open(last_results[idx].url)

        elif choice == "2":
            q = Prompt.ask("Ask Darkelf Retro AI")
            ai_stream(q)

        elif choice == "3":
            if last_query and online:
                with console.status("Repeating last search...", spinner="dots"):
                    last_results = archive_search(last_query)
                show_results(last_results)

                # 🔥 FIX: same guard here
                if not last_results:
                    Prompt.ask("[dim]Press Enter to return to menu[/dim]", default="")
            else:
                console.print("[dim]No previous search or offline[/dim]")
                Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

        elif choice == "q":
            console.print("Goodbye.", style="bold green")
            sys.exit()

        else:
            console.print("[red]Invalid option[/red]")
            Prompt.ask("[dim]Press Enter to continue[/dim]", default="")

# =========================
# BOOT SEQUENCE
# =========================

def boot():
    console.clear()
    console.print(ASCII_ART, style="green")
    console.print("[dim]Darkelf Retro AI initializing…[/dim]\n")
    Prompt.ask("[bold green]Press Enter to continue[/bold green]", default="")

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    boot()
    main_menu()
