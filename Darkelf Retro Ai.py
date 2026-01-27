import sys
import requests
import subprocess
from dataclasses import dataclass
from typing import List, Optional

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text
from rich.live import Live

# =========================
# GLOBALS / CONSTANTS
# =========================

APP_NAME = "Darkelf Retro AI"
ARCHIVE_API = "https://archive.org/advancedsearch.php"
OLLAMA_MODEL = "llama3"

console = Console()

online = False
last_results: List["Result"] = []
last_query: Optional[str] = None
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
# NETWORK
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
    identifier: str
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
                identifier=d.get("identifier"),
                year=d.get("year"),
                mediatype=d.get("mediatype"),
            )
        )
    return results

# =========================
# DISPLAY RESULTS
# =========================

def show_results(results: List[Result]):
    if not results:
        console.print("\n[bold red]NO RESULTS FOUND[/bold red]")
        console.print("[dim]Try a broader search term.[/dim]\n")
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
    console.print("[dim]Enter number = view | a = AI | q = back[/dim]")

# =========================
# TERMINAL ITEM VIEWER
# =========================

def view_item_text(r: Result):
    console.clear()
    console.print(ASCII_ART, style="green")

    try:
        data = requests.get(
            f"https://archive.org/metadata/{r.identifier}",
            timeout=10
        ).json()

        meta = data.get("metadata", {})
        title = meta.get("title", "Unknown")
        description = meta.get("description", "No description available.")
        year = meta.get("year", "")
        mediatype = meta.get("mediatype", "")

        console.print(Panel(
            f"[bold cyan]{title}[/bold cyan]\n\n"
            f"[bold]Year:[/bold] {year}\n"
            f"[bold]Type:[/bold] {mediatype}\n\n"
            f"[bold]Description:[/bold]\n{description}",
            title="Archive Item",
            border_style="green",
            expand=True
        ))

    except Exception as e:
        console.print("[red]Failed to load item details[/red]")
        console.print(str(e))

    Prompt.ask("[dim]Press Enter to return[/dim]", default="")

# =========================
# AI ENGINE
# =========================

def ai_stream(prompt: str, mode="FREEFORM"):
    identity = f"""
You are Darkelf Retro AI.
Focus on retro computing, emulation, and digital preservation.
Output Mode: {mode}
Be concise and factual.
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

# =========================
# MAIN MENU (FIXED)
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

        choice = Prompt.ask("Select").strip().lower()

        # SEARCH
        if choice == "1":
            if not online:
                console.print("[red]Offline — search unavailable[/red]")
                Prompt.ask("Press Enter", default="")
                continue

            last_query = Prompt.ask("Search query")

            with console.status("Searching archive...", spinner="dots"):
                last_results = archive_search(last_query)

            show_results(last_results)

            if not last_results:
                Prompt.ask("Press Enter", default="")
                continue

            # 🔥 FIXED ACTION LOOP
            while True:
                cmd = Prompt.ask("Action").strip().lower()

                if cmd == "q":
                    break

                if cmd.isdigit():
                    idx = int(cmd) - 1
                    if 0 <= idx < len(last_results):
                        view_item_text(last_results[idx])
                        show_results(last_results)
                    else:
                        console.print("[red]Invalid item number[/red]")
                    continue

                if cmd == "a":
                    idx = int(Prompt.ask("Item number")) - 1
                    if 0 <= idx < len(last_results):
                        ai_stream(
                            f"Explain the historical significance of:\n{last_results[idx].title}"
                        )
                        show_results(last_results)
                    else:
                        console.print("[red]Invalid item number[/red]")
                    continue

                console.print("[red]Unknown command[/red]")

        # ASK AI
        elif choice == "2":
            q = Prompt.ask("Ask Darkelf Retro AI")
            ai_stream(q)

        # REPEAT SEARCH
        elif choice == "3":
            if last_query and online:
                with console.status("Repeating search...", spinner="dots"):
                    last_results = archive_search(last_query)
                show_results(last_results)
                Prompt.ask("Press Enter", default="")
            else:
                console.print("[dim]No previous search or offline[/dim]")
                Prompt.ask("Press Enter", default="")

        elif choice == "q":
            console.print("Goodbye.", style="bold green")
            sys.exit()

# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    main_menu()
