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

### Project Description

We're building a tool to facilitate offline collaborative editing of spreadsheet formulas. Leveraging the structure of Excel formulas, we'll merge changes using their AST representations, ensuring more efficient and accurate results.


## 🚀 Getting Started

### Running the Application (Using Docker)

1. **Prerequisites**: Ensure you have Docker installed. If not, install Docker from [here](https://docs.docker.com/get-docker/).

2. Clone the repository:
   ```sh
   git clone https://github.com/fabian-gubler/cellster.git
   ```

3. Navigate to the project directory:
   ```sh
   cd cellster
   ```

4. Build and run the Docker container for the web application:
   ```sh
   docker build -t cellster .
   docker run -p 8080:8080 cellster
   ```

5. Open your browser and visit `http://localhost:8080`.

> **Note**: More detailed instructions and relevant scripts for Docker setup will be added shortly.


### Developing the Application (Using Nix)

1. **Prerequisites**: We use Nix for a reproducible development experience. Ensure you have it installed. Instructions for installation can be found [here](https://nixos.org/download.html).
  
2. Clone the repository:
   ```sh
   git clone https://github.com/fabian-gubler/cellster.git
   ```

3. Navigate to the project directory:
   ```sh
   cd cellster
   ```

4. Using Nix, set up the development environment. This will ensure that all the required dependencies for both the backend (Python) and the frontend (Web tech) are installed:
   ```sh
   nix-shell
   ```

> **Note**: Integration of Nix for development is currently in progress. More detailed instructions and relevant scripts will be added soon.


## 📖 Documentation

Further documentation on how to use the tool, contribute, and delve deeper into its features will be provided soon. Stay tuned!

## 💡 **Feedback & Contributions**: We're always open to feedback and contributions. Feel free to open issues, suggest features, or contribute to the codebase.
