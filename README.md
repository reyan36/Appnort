<div align="center">

# Appnort

**Smart Software Audit Tool for Windows**

Scan, categorize, and assess security risks of every installed program on your PC — powered by AI.

[![Download](https://img.shields.io/badge/Download-Windows%20Installer-2563eb?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/reyan36/appnort/releases/latest)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Website](https://img.shields.io/badge/Website-appnort.vercel.app-000?style=for-the-badge&logo=vercel&logoColor=white)](https://appnort.vercel.app)

<br>

[Download](#-installation) · [Features](#-features) · [How It Works](#-how-it-works) · [Tech Stack](#%EF%B8%8F-tech-stack) · [Development](#-development) · [Website](https://appnort.vercel.app)

</div>

<br>

## What is Appnort?

Appnort is a **local-first** software audit and inventory management tool built for Windows. It reads your Windows Registry to detect every installed program, then uses a two-tier approach — **rule-based matching** and **AI classification** (via Groq's Llama 3.3 70B) — to categorize each application and assign a security risk rating.

All data stays on your machine. No accounts. No cloud storage. Just a clean audit of your system in seconds.

<br>

## Features

| Feature | Description |
|---------|-------------|
| **One-Click Scan** | Scans both 64-bit and 32-bit registry paths to detect every installed program |
| **AI Categorization** | Uses Groq Llama 3.3 70B to classify unknown apps into 8 categories |
| **Rule-Based Fallback** | Known apps are categorized instantly via keyword matching — works offline |
| **Security Risk Ratings** | Every app gets a risk level: Low, Medium, or High |
| **PDF Audit Reports** | Export professional, color-coded PDF reports grouped by category |
| **Smart Caching** | AI results are cached locally to minimize API calls on repeat scans |
| **Dark & Light Themes** | Modern UI with system, dark, and light theme options |
| **Privacy First** | API keys stored locally. No data leaves your machine |

<br>

## How It Works

```
┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────┐
│  1. SCAN     │────▶│  2. RULE CHECK    │────▶│  3. AI CLASSIFY  │────▶│  4. REPORT   │
│  Click scan  │     │  Keyword matching │     │  Groq Llama 3.3  │     │  View in UI  │
│  button      │     │  for known apps   │     │  for unknowns    │     │  or PDF      │
└──────────────┘     └──────────────────┘     └──────────────────┘     └──────────────┘
```

1. **Scan** — Reads Windows Registry (`HKEY_LOCAL_MACHINE\SOFTWARE\...\Uninstall`) for installed programs
2. **Rule Check** — Known apps are instantly matched against 8 categories using keywords
3. **AI Classification** — Unknown apps are sent to Groq API in batches of 20 for categorization + risk rating
4. **Report** — Results displayed in the GUI and exportable as a color-coded PDF

<br>

## Categories & Risk Levels

**8 Categories:**

`Development` · `Productivity` · `Games` · `Browsers` · `Media` · `System` · `Communication` · `Utilities`

**3 Risk Levels:**

| Level | Meaning |
|-------|---------|
| 🟢 **Low** | Trusted commercial software from verified publishers |
| 🟡 **Medium** | P2P clients, freeware with potential adware, remote access tools |
| 🔴 **High** | Flagged software, keyloggers, cracked or suspicious applications |

<br>

## Installation

### Download Installer (Recommended)

1. Go to the [Releases](https://github.com/reyan36/appnort/releases/latest) page
2. Download **`Appnort_Setup.exe`**
3. Run the installer and follow the setup wizard
4. Launch Appnort from Start Menu or Desktop

> **Requirements:** Windows 10/11 • No admin rights needed • ~20 MB disk space

### Getting a Groq API Key (Optional)

Appnort works without an API key using rule-based categorization only. For AI-powered classification:

1. Go to [console.groq.com](https://console.groq.com)
2. Create a free account and generate an API key
3. Paste the key into Appnort's Settings tab

<br>

## Development

### Prerequisites

- Python 3.10 or higher
- Windows OS (Registry scanning is Windows-only)

### Setup

```bash
# Clone the repository
git clone https://github.com/reyan36/appnort.git
cd appnort

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
python -m appnort.main
```

### Build Executable

```bash
# Step 1: Build with PyInstaller
build_exe.bat

# Step 2: Create installer (requires Inno Setup)
# Open appnort_setup.iss in Inno Setup Compiler and click Compile
```

<br>

## Tech Stack

| Technology | Role |
|------------|------|
| [Python 3](https://python.org) | Core language |
| [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) | Modern GUI framework |
| [Groq API](https://groq.com) | AI-powered classification (Llama 3.3 70B) |
| [ReportLab](https://www.reportlab.com) | PDF report generation |
| [psutil](https://github.com/giampaolo/psutil) | System process utilities |
| [winreg](https://docs.python.org/3/library/winreg.html) | Windows Registry access |
| [PyInstaller](https://pyinstaller.org) | Executable packaging |
| [Inno Setup](https://jrsoftware.org/isinfo.php) | Windows installer creation |

<br>

## Project Structure

```
appnort/
├── appnort/
│   ├── main.py              # GUI application (CustomTkinter)
│   ├── scanner.py            # Windows Registry scanner
│   ├── categorizer.py        # AI + rule-based categorization
│   ├── pdf_generator.py      # PDF report generation
│   └── config.py             # Configuration manager
├── website/
│   ├── index.html            # Landing page
│   ├── styles.css            # Styles (light + blue theme)
│   ├── script.js             # GSAP animations
│   └── favicon.ico           # Site icon
├── appnort.ico               # App icon
├── build_exe.bat             # PyInstaller build script
├── requirements.txt          # Python dependencies
├── LICENSE                   # MIT License
└── README.md                 # This file
```

<br>

## Website

Appnort has a landing page deployed on Vercel:

**[appnort.vercel.app](https://appnort.vercel.app)**

The website source is in the `/website` directory — static HTML, CSS, and JS with GSAP scroll animations.

<br>

## License

This project is licensed under the [MIT License](LICENSE).

<br>

## Author

**Reyan Arshad** — [@reyan36](https://www.linkedin.com/in/reyan36/)

---

<div align="center">

**[Download Appnort](https://github.com/reyan36/appnort/releases/latest)** · **[View Website](https://appnort.vercel.app)** · **[Report Bug](https://github.com/reyan36/appnort/issues)**

</div>
