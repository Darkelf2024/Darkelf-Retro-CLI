# 🧙‍♂️ Darkelf Retro CLI Hub  
*A terminal-native research toolkit for retro gaming history*

**Darkelf Retro CLI Hub** is a local-first, command-line research environment designed for retro gaming historians, collectors, preservationists, and enthusiasts.

This repository contains **two complementary terminal tools** (click to view/download):

- **Darkelf Retro CLI** – a structured, menu-driven retro gaming research interface  
  - Source: **[Darkelf Retro CLI.py](Darkelf%20Retro%20CLI.py)**
- **Darkelf Retro AI** – a focused, local AI research assistant for classic games and hardware  
  - Source: **[Darkelf Retro Ai.py](Darkelf%20Retro%20Ai.py)**

Together, they form a distraction-free, ethics-first workflow for exploring the history, documentation, and cultural context of classic video games—directly from your terminal.

---

## 🔗 Quick Links

- ▶️ **Run the main tool:** **[Darkelf Retro CLI.py](Darkelf%20Retro%20CLI.py)**
- 🤖 **Run the assistant:** **[Darkelf Retro Ai.py](Darkelf%20Retro%20Ai.py)**
- **Ollama Setup Guide:** **[Ollama Setup Guide](https://github.com/Darkelf2024/Darkelf-Retro-CLI-Hub/blob/main/Ollama%20Setup%20Guide.md)**
- ⚖️ **License:** LGPL (see `LICENSE` / `LICENSE.md` in this repo)

> Tip: On GitHub, click a file → **Download raw file** (or use the `raw` view) to save it locally.

---

## 🗂 Repository Overview

```
Darkelf-Retro-CLI/
├── Darkelf Retro CLI.py      # Main retro research CLI
├── Darkelf Retro Ai.py       # Local streaming AI assistant
├── README.md                # Project hub documentation
├── LICENSE.md
└── assets/
    └── screenshots, logos
```

Each tool can be used **independently**, but they are designed to work best as a pair.

---

## 🕹️ Darkelf Retro CLI (Full Research Suite)

**Darkelf Retro CLI** is a launcher-style, keyboard-driven interface that serves as the **complete Darkelf Retro research suite**.

It integrates **web research, archival access, local history, and Darkelf Retro AI** into a single, cohesive terminal workflow.

### What it does
- Text-only web research
- Curated archival access
- Persistent local search history
- Fast, numbered navigation
- Integrated **Darkelf Retro AI**
- Zero tracking, zero accounts

### Key Features
- **Web Search**  
  Clean DuckDuckGo Lite queries for distraction-free results.
- **Retro Archives**  
  - Internet Archive (manuals, magazines, guides)  
  - Video Game History Foundation (metadata & catalog research)
- **Search History**  
  Automatically saved locally for efficient revisits.
- **Darkelf Retro AI Integration**  
  Ask focused retro-gaming questions without leaving the CLI.
- **Terminal-Native UX**  
  No mouse, no clutter—just fast, intentional navigation.

**Darkelf Retro CLI is the primary entry point** and is recommended for most users.  
It acts as your **research control panel**.

---

## 🤖 Darkelf Retro AI (Standalone / Slim Edition)

**Darkelf Retro AI** is a **standalone, slimmed-down version** of the AI component included in Darkelf Retro CLI.

It is designed for users who want **direct access to the AI only**, without the full research interface.

### What makes it different
- Runs **100% locally** using **Ollama**
- No cloud APIs
- No data collection
- No web search or archive navigation
- No history or launcher system

### Focus Areas
- Retro consoles & home computers  
- Arcade systems  
- Game manuals & documentation  
- Magazines & developer interviews  
- Hardware limitations & design decisions  
- Historical and cultural context  

The AI is intentionally scoped:  
**it does not emulate games, download ROMs, or bypass copyright**.

### When to use it
- You only want the AI component
- You prefer a minimal, single-purpose tool
- You plan to integrate it into your own workflow

Think of **Darkelf Retro AI** as a **lightweight research companion**, while **Darkelf Retro CLI** is the **complete research environment**.

---

## 🧠 Design Philosophy

Darkelf Retro tools are built around a few core principles:

- **Local-First** – Your research stays on your machine  
- **Terminal-Native** – Designed for CLI users, not web dashboards  
- **Archival Respect** – Metadata and documentation only  
- **Focused Scope** – No feature creep, no gimmicks  
- **Ethical Use** – Preservation, not piracy  

This is software for people who enjoy reading old manuals, studying magazine scans, and understanding *why* games were built the way they were.

---

## ⚙️ Requirements

- **Operating System**:  
  - macOS or Linux  
  - Windows may work with minor adjustments
- **Python**: 3.9+
- **Python Packages**:
  ```bash
  pip install requests beautifulsoup4 rich
  ```
- **Ollama** (for Darkelf Retro AI):
  ```bash
  ollama pull mistral
  ```

---

## 🚀 Installation & Launch

Clone the repository:
```bash
git clone https://github.com/Darkelf2024/Darkelf-Retro-CLI.git
cd Darkelf-Retro-CLI
```

### Run Darkelf Retro CLI
```bash
python "Darkelf Retro CLI.py"
```

### Run Darkelf Retro AI
```bash
python "Darkelf Retro Ai.py"
```

You can run them in **separate terminals** or side-by-side using tmux for a true retro research workflow.

---

## 📜 License & Ethics

This project is intended **strictly for educational and research purposes**.

Users are responsible for complying with:
- Internet Archive terms of use
- Video Game History Foundation guidelines
- Local and international copyright laws

**No ROM distribution. No emulation. No circumvention.**

---

## 🧙 Closing Thoughts

**Darkelf Retro CLI Hub** is for people who still remember:
- Reading game manuals cover to cover
- Learning hardware quirks the hard way
- Discovering secrets through magazines and word of mouth

If you care about **preservation, history, and understanding**, not just nostalgia—  
you’re exactly who this tool was made for.

*Rediscover the golden age of gaming—one terminal command at a time.*
