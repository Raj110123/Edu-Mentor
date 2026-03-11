# Project Name

## About the Hackathon

**Loop** is a **24-hour National Level Hackathon** organized by **Bharati Vidyapeeth College of Engineering, Navi Mumbai** in association with the **Centre for Development of Advanced Computing (C-DAC)**, Ministry of Electronics & Information Technology, Government of India.

The hackathon focuses on solving real-world problems using modern technologies such as automation, AI systems, and cyber security. Participants are encouraged to build practical, scalable, and impactful solutions.

---

# Team Development Guidelines

## 1. Repository Structure

The project will follow a **single monorepo structure**.  
All components such as frontend, backend, and services must be maintained within this same repository. Do not create separate repositories for individual parts.

---

## 2. Team Member Access

The **team leader must add all team members** to the repository so everyone can collaborate and contribute to the project.

---

## 3. Code Push Frequency

Every team member must **push their code at least once every hour**.

Recommended workflow:

```bash
git pull origin main
git add .
git commit -m "short meaningful message"
git push origin main
```

Always pull the latest changes before pushing to avoid merge conflicts.

---

## 4. API Keys and Secrets

**Do not push API keys, tokens, or sensitive credentials to the repository.**

Use environment variables instead and add the following files to `.gitignore`:

```
.env
.env.local
```

---

## 5. Documentation Requirement

Proper documentation is required for all parts of the project. It should include:

- Setup instructions
- How to run the project
- Project folder structure
- APIs or services used
- Dependencies and installation steps

---

## 6. Commit Message Standards

Use **clear and meaningful commit messages**.

Examples:

```
feat: add authentication module
fix: resolve login bug
docs: update README
refactor: optimize database queries
```

Avoid vague messages like `update` or `changes`.

---

## 7. Maintain Clean Code

Code should be readable, organized, and follow proper naming conventions.  
Avoid unnecessary files and keep the project structure clean. Add comments where needed.

## Run "npx next dev --webpack"