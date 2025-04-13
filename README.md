# 🖱️ Mini Cursor – AI-Powered Vibe Coding Tool

Mini Cursor is a terminal-based AI assistant that transforms your natural language into real coding actions. Built with Python and powered by [Gemini AI](https://ai.google.dev/), this tool helps you build, edit, and run code projects using pure vibes 🧙‍♂️✨.

> Think of it as a mini co-pilot in your terminal — plan, code, observe, fix, repeat.

---

## ⚡️ Features

- 🧠 Follows a `plan → action → observe → fix/output` cycle
- 🖥️ Executes shell commands via Python
- 📂 Reads, writes, and edits files with smart context awareness
- 🧪 Observes tool output and suggests intelligent fixes
- 🤖 All powered by Gemini AI's powerful reasoning engine
- 🪟 Optimized for **Windows 11**

---

## 🛠️ Tech Stack

- **Python**
- **Google Gemini API**
- **dotenv** for secure key management

---

## 🧰 Available Tools

| Tool Name     | Description |
|---------------|-------------|
| `run_command` | Executes terminal commands on your system |
| `write_file`  | Creates a file with raw (unescaped) code |
| `edit_file`   | Modifies an existing file's content |
| `read_file`   | Reads the content of a specified file |

---

## 🧠 System Prompt & AI Flow

Mini Cursor is guided by a rich system prompt designed for developer productivity. Here's how the AI thinks:

1. **Understands the user query**.
2. **Plans the steps** required to complete the task.
3. **Selects the right tool** from the available set.
4. **Performs the action** (write/edit/run).
5. **Observes results**, handles errors, and suggests **fixes**.

### Example Prompt Flow

```json
{ "step": "plan", "content": "User wants to build a React app." }
{ "step": "action", "function": "run_command", "input": "npm create vite@latest" }
{ "step": "observe", "output": "Project created successfully." }
{ "step": "action", "function": "write_file", "input": { "filename": "App.jsx", "content": "function App() { return <h1>Hello World</h1>; }" } }
```

## 🚀 Getting Started

### 🧩 Prerequisites

- Python 3.8+
- pip
- A [Gemini API Key](https://ai.google.dev/)

---

### ⚙️ Setup

#### 1. **Clone the repository**

```bash
git clone https://github.com/yourusername/mini-cursor.git
cd mini-cursor
```
---

#### 2. **Configure Environment Variables**

1. Create a `.env` file in the root of your project.
2. Add your [Gemini API Key](https://ai.google.dev/) 
---

#### 3. **Run the Agent**

Once everything is set up, start Mini Cursor by running:

```bash
python mini_cursor.py
```


