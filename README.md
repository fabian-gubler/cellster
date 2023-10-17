<p align="center">
  <img src="https://raw.githubusercontent.com/fabian-gubler/celllster/main/assets/logo-colorful.png" alt="Logo" width="750" height="300">
</p>
<p align="center">
  <strong>Empowering Offline Collaboration in Spreadsheets</strong>
</p>
<p align="center">
  Break free from the chains of constant connectivity with the power of local-first software. Dive into a revolutionary way of collaboratively editing spreadsheet formulas without the need for real-time online presence. Experience seamless merges using CRDTs and witness the power of structured conflict resolution.
</p>

---

## 🌟 Main Features

1. **AST-based Formula Representation**: Convert and visualize Excel formulas as structured Abstract Syntax Trees.
2. **Conflict-free Merges with CRDTs**: Tailored CRDT implementations that bring robustness to merging offline formula edits.
3. **Interactive UI**: Engage with an intuitive interface, input your formulas, and see the magic unfold.

---

## 🔍 About

### Introduction

In today's cloud-centric era, most collaboration tools rely on real-time connectivity. But what if there's a better way? Our project explores the vast potential of local-first applications, focusing on the niche of spreadsheet formula editing.

### Motivation

With an abundance of text-based collaborative tools, collaborative spreadsheet editing remains a daunting challenge. By harnessing the inherent structure of Excel formulas, we're crafting a solution that promises precise merging with reduced conflicts.

### Project Description

We're building a tool to facilitate offline collaborative editing of spreadsheet formulas. Leveraging the structure of Excel formulas, we'll merge changes using their AST representations, ensuring more efficient and accurate results.

---

## 🚀 Getting Started

### Running the Application (Using Docker)

1. **Prerequisites**: Ensure you have Docker installed. If not, install Docker from [here](https://docs.docker.com/get-docker/).

2. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/PROJECT_NAME.git
   ```

3. Navigate to the project directory:
   ```sh
   cd PROJECT_NAME
   ```

4. Build and run the Docker container for the web application:
   ```sh
   docker build -t PROJECT_NAME .
   docker run -p 8080:8080 PROJECT_NAME
   ```

5. Open your browser and visit `http://localhost:8080`.

> **Note**: More detailed instructions and relevant scripts for Docker setup will be added shortly.

---

### Developing the Application (Using Nix)

1. **Prerequisites**: We use Nix for a reproducible development experience. Ensure you have it installed. Instructions for installation can be found [here](https://nixos.org/download.html).
  
2. Clone the repository:
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/PROJECT_NAME.git
   ```

3. Navigate to the project directory:
   ```sh
   cd PROJECT_NAME
   ```

4. Using Nix, set up the development environment. This will ensure that all the required dependencies for both the backend (Python) and the frontend (Web tech) are installed:
   ```sh
   nix-shell
   ```

> **Note**: Integration of Nix for development is currently in progress. More detailed instructions and relevant scripts will be added soon.

---

## 📖 Documentation

Further documentation on how to use the tool, contribute, and delve deeper into its features will be provided soon. Stay tuned!

---

💡 **Feedback & Contributions**: We're always open to feedback and contributions. Feel free to open issues, suggest features, or contribute to the codebase.

---

Thank you for being a part of this revolutionary journey. Let's redefine collaborative spreadsheet editing together!


---  

# More Formal

## Introduction

In the age of cloud-based collaboration, real-time connectivity is often taken as a given. However, this model is not always feasible nor efficient. The realm of local-first applications offers an array of alternatives that allow for operations like text-editing to be performed offline and later synchronized seamlessly. This project seeks to take the concept of local-first collaboration to a novel domain - spreadsheet formula editing.

## Motivation

While text-based collaborative tools have thrived, collaborative spreadsheet editing remains a challenge. Directly editing text can lead to myriad complications due to the freeform nature of the content. Excel formulas, however, come with inherent structures and semantics that could be leveraged to facilitate more effective collaborative editing.

## Project Description

Our goal is to facilitate offline collaborative editing for spreadsheet formulas, more specifically, Excel formulas. Rather than using a text-based approach, we will utilize the inherent structure of Excel formulas to merge changes. This structural approach promises more accurate merging with fewer conflicts.

### Key Contributions

1. **Leveraging Abstract Syntax Trees (ASTs) for Excel Formulas**: Excel formulas, when viewed as strings, have underlying structures that can be represented as ASTs. We intend to harness existing libraries to convert these formulas into their AST representations.
  
2. **Implementing CRDTs for Merging ASTs**: CRDTs (Conflict-free Replicated Data Types) have demonstrated robust capabilities in real-time collaborative platforms. For our project, we will develop CRDTs specifically designed to merge Excel formula ASTs. This approach will ensure that edits made offline can be seamlessly integrated without conflicts when reconnected.

3. **Interactive Front-end Interface**: To provide a hands-on experience, we will create a minimalistic front-end where users can input Excel formulas and witness the merged results. Our interface will not only display the merged formula but also, if feasible, elucidate the merging process to users.

### Future Aspirations

Given adequate time and resources, we aim to extend this project's functionality to encompass entire spreadsheets, thus paving the way for comprehensive local-first collaborative spreadsheet editing.

## Current Status

1. **Formula Parsing**: Initial steps have been taken to parse Excel formulas and convert them to ASTs.
2. **CRDT Development**: Work is in progress to design and implement CRDTs suitable for merging formula ASTs.
3. **Front-end Interface**: Planning phase to design an intuitive and user-friendly interface.

## How Can You Contribute?

1. **Library Suggestions**: If you know of any reliable libraries that can effectively transform Excel formulas into ASTs, your recommendations are most welcome.
2. **CRDT Insights**: Any insights or experiences related to CRDTs can significantly benefit our implementation process.
3. **Feedback**: As we progress, testing and feedback are crucial. You can test our prototype, report issues, or suggest features.

---

Thank you for your interest in our project. Your support and contributions are pivotal in making this endeavor a success. Together, we can redefine the boundaries of collaborative spreadsheet editing.

---
# GPT Prompt

I want you to help me with the project description. To fill out some details ask clarification questions. The final output should be a draft of a README file used and updated during the project phase on a public github repository. This README should interest the reader, also providing the motivation and contribution of this project.

--- Current Project Notes:

In our graduate studies we are doing an implementation Project. Here we selected the topic of local-first applications. Currently collaboration in the cloud is done through real-time (i.e. people must be online). In the local-first realm there exist a lot of alternatives that allows e.g. text-editing to be done offline and then resolved using for instance CRDTs. We envision something similar but for collaborative spreadsheet editing. Here we start with merging changes in editing excel formulas. We do not want to make a text-based approach, as here we would face a lot of difficulties. In contrast, we want to make use of the structure provided of excel formulas. The given structure of excel formulas provide us certain guarantees and boundaries. Our plan is to make use of existing libaries that can transform excel formulas (as strings) into Abstract syntax trees. We can then develop CRDTs in order to merge these ASTs. This is what our project is all about and the main contribution in the development. 

At an initial stage this project must be able to parse excel formulas and convert them to ASTs. Then we implement CRDTs to Merge two formulas (in the form of ASTs) in order to enable collaboration and resolving potential conflicts. In the end, we will create a minimal front-end (and would also link it in the github repo), that allows users to enter excel formulas and see the merged formula. It is still open, but if possible we would like to give an explanation in the front-end that allows the user to know how this result came to be.

If the time allows, we would like to extend the functionality to an entire spreadsheet.
