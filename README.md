<p align="center">
  <img src="https://raw.githubusercontent.com/fabian-gubler/celllster/main/assets/logo-colorful.svg" alt="banner" width="750" height="300">
</p>
<p align="center">
  <strong>Empowering Offline Collaboration in Spreadsheets</strong>
</p>
<p align="center">
  Break free from the chains of constant connectivity with the power of local-first software. Dive into a revolutionary way of collaboratively editing spreadsheet formulas without the need for real-time online presence. Experience seamless merges using CRDTs and witness the power of structured conflict resolution.
</p>

## 🌟 Main Features

1. **AST-based Formula Representation**: Convert and visualize Excel formulas as structured Abstract Syntax Trees.
2. **Conflict-free Merges with CRDTs**: Tailored CRDT implementations that bring robustness to merging offline formula edits.
3. **Interactive UI**: Engage with an intuitive interface, input your formulas, and see the magic unfold.


## 🔍 About

### Introduction

In today's cloud-centric era, most collaboration tools rely on real-time connectivity. But what if there's a better way? Our project explores the vast potential of local-first applications, focusing on the niche of spreadsheet formula editing.

### Motivation

With an abundance of text-based collaborative tools, collaborative spreadsheet editing remains a daunting challenge. By harnessing the inherent structure of Excel formulas, we're crafting a solution that promises precise merging with reduced conflicts.


## 🚀 Getting Started

### Setting up the Application (Using Nix)

#### Prerequisites

1. **Install nix**: We use Nix for a reproducible development experience. Ensure you have it installed. Instructions for installation can be found [here](https://nixos.org/download.html).
   - **Note for Windows Users**: Nix does not run natively on Windows. To use Nix on Windows, you need to set up the Windows Subsystem for Linux (WSL). Follow the [WSL installation guide](https://docs.microsoft.com/en-us/windows/wsl/install) to get started.

2. **Enable nix flake**: The `flake` feature is still considered experimental thus a specific Nix configuration is necessary in `~/.config/nix/nix.conf`:

```sh
experimental-features = nix-command flakes
```

#### Create Environment
  
1. Clone the repository:
   ```sh
   git clone https://github.com/fabian-gubler/cellster.git
   ```

2. Navigate to the project directory:
   ```sh
   cd cellster
   ```

3. Using Nix, set up the development environment. This will ensure that all the required dependencies for both the backend (Python) and the frontend (Web tech) are installed:
   ```sh
   nix develop
   ```
### Setting Up the Application (Using Pip)

> [!IMPORTANT]
> **Using Pip vs Nix**:
> - **Nix**: Guarantees a consistent development environment by managing dependencies, ensuring reproducibility across different setups.
> - **Pip**: Prone to variations in package versions and local configurations, leading to potential inconsistencies.
> - **Recommendation**: We recommend using `nix` for a more reliable setup. If using `pip`, be aware of these limitations.

#### Prerequisites

1. **Python Installation**: Ensure that Python is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).
2. **Pip Installation**: Make sure you have `pip` installed, which is Python's package installer. It usually comes with Python installation.

To check if `pip` is already installed on your system, run the following command:
```sh
pip --version
```

#### Create Environment

1. Clone the repository:
   ```sh
   git clone https://github.com/fabian-gubler/cellster.git
   ```

2. Navigate to the project directory:
   ```sh
   cd cellster
   ```

3. Create a virtual environment:
   ```sh
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```sh
     .\venv\Scripts\activate
     ```
   - On Unix or MacOS:
     ```sh
     source venv/bin/activate
     ```

5. Install the requirements:
   ```sh
   pip install -r requirements.txt
   ```

## ⚙️ Usage

**Running the Application**:

- To start the interface, run:
 ```sh
 python main.py
 ```

**Running Tests with Pytest**:

- Ensure that you are in the project's root directory.
- Execute the following command to run the tests:
 ```sh
 pytest
 ```

## 💡 Feedback & Contributions

We're always open to feedback and contributions. Feel free to open issues, suggest features, or contribute to the codebase.
