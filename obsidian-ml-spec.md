# Obsidian Integration Guide
## Adding Knowledge Management to Data_Science_be_like Repository

---

## 0. Migration Overview

This guide will help you integrate Obsidian into your existing **Data_Science_be_like** repository without losing any of your current work. We'll reorganize the structure to support both your code/notebooks AND Obsidian notes for knowledge management.

**What you'll get:**
- All your existing notebooks and code preserved
- New Obsidian vault structure integrated
- Powerful linking between concepts and code
- Graph view of your knowledge
- GitHub sync for everything

---

## 1. Current → New Structure Migration

### 1.1 Backup First!
```bash
cd /path/to/Data_Science_be_like
git checkout -b obsidian-integration
git add .
git commit -m "Backup before Obsidian integration"
```

### 1.2 Proposed New Structure
```
Data_Science_be_like/
├── .obsidian/              # Obsidian settings (auto-generated)
├── notes/                  # 📝 New: Obsidian knowledge base
│   ├── 00-inbox/          # Quick capture
│   ├── 01-concepts/       # Core concepts
│   │   ├── linear-algebra/
│   │   ├── calculus/
│   │   ├── statistics/
│   │   └── machine-learning/
│   ├── 02-literature/     # Papers, articles, books
│   ├── 03-projects/       # Project documentation
│   ├── 04-MOCs/           # Maps of Content (hub notes)
│   └── templates/         # Note templates
├── code/                   # 💻 Your existing code (reorganized)
│   ├── notebooks/         # Jupyter notebooks
│   ├── scripts/           # Python scripts/modules
│   └── experiments/       # Experimental code
├── data/                   # 📊 Your datasets (if you have them)
│   ├── raw/
│   ├── processed/
│   └── external/
├── assets/                 # 🖼️ Images, PDFs, exports
├── .gitignore             # Updated gitignore
└── README.md              # Updated README
```

### 1.3 Migration Script
Create a file `migrate_to_obsidian.sh`:

```bash
#!/bin/bash
# Migration script for adding Obsidian to Data_Science_be_like

echo "🚀 Starting migration to Obsidian structure..."

# Create new directory structure
mkdir -p notes/{00-inbox,01-concepts/{linear-algebra,calculus,statistics,machine-learning},02-literature,03-projects,04-MOCs,templates}
mkdir -p code/{notebooks,scripts,experiments}
mkdir -p data/{raw,processed,external}
mkdir -p assets

# Move existing notebooks (adjust paths based on your current structure)
if [ -d "notebooks" ]; then
    echo "📓 Moving existing notebooks..."
    mv notebooks/* code/notebooks/ 2>/dev/null || true
    rmdir notebooks 2>/dev/null || true
fi

# Move existing Python files
echo "🐍 Moving Python scripts..."
find . -maxdepth 1 -name "*.py" -exec mv {} code/scripts/ \; 2>/dev/null || true

# Move existing data files
if [ -d "data" ]; then
    echo "📊 Preserving data directory..."
    # Data directory already exists, nothing to do
else
    echo "📊 Creating data directory..."
fi

# Move any existing images/PDFs
find . -maxdepth 1 \( -name "*.png" -o -name "*.jpg" -o -name "*.pdf" \) -exec mv {} assets/ \; 2>/dev/null || true

echo "✅ Migration complete! Review the changes before committing."
```

Make it executable and run:
```bash
chmod +x migrate_to_obsidian.sh
./migrate_to_obsidian.sh
```

**Manual adjustments**: Review and move any other files to appropriate folders.

---

## 2. Setting Up Obsidian

### 2.1 Open Your Repo as an Obsidian Vault
1. Open Obsidian
2. Click "Open folder as vault"
3. Select your `Data_Science_be_like` directory
4. Obsidian will create `.obsidian/` folder automatically

### 2.2 Essential Settings
**Settings → Files and Links:**
- New link format: Shortest path when possible
- Use [[Wikilinks]]: Enabled
- Default location for new notes: `notes/00-inbox`
- Default location for new attachments: `assets`

**Settings → Editor:**
- Strict line breaks: Disabled
- Show frontmatter: Enabled

---

## 3. Essential Plugins Installation

### 3.1 Core Plugins (Enable in Settings)
- [ ] Graph view
- [ ] Backlinks
- [ ] Outgoing links
- [ ] Tag pane
- [ ] Templates
- [ ] Daily notes (optional)

### 3.2 Community Plugins (Settings → Community plugins → Browse)

**Install these in order:**

1. **Obsidian Git** (Auto-backup to GitHub)
   - Settings:
     - Auto-backup interval: 15 minutes
     - Auto-pull on startup: Enabled
     - Commit message: `vault backup: {{date}}`

2. **Obsidian Wypst** (Typst math rendering)
   - Settings:
     - Enable fallback to LaTeX: Enabled

3. **Dataview** (Query and organize notes)
   - Enable JavaScript queries: Optional

4. **Templater** (Note templates)
   - Template folder: `notes/templates`

5. **Excalidraw** (Drawing diagrams)

6. **Advanced Tables** (Better table editing)

7. **QuickAdd** (Fast note creation)

---

## 4. Updated .gitignore

Create/update `.gitignore` in repo root:

```gitignore
# Obsidian
.obsidian/workspace*
.obsidian/cache
.trash/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Jupyter Notebook
.ipynb_checkpoints
*/.ipynb_checkpoints/*

# Data (uncomment if you don't want to track data)
# data/raw/*
# data/processed/*
# !data/raw/.gitkeep
# !data/processed/.gitkeep

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo

# Temporary files
*.tmp
*.log
```

---

## 5. Note Templates

### 5.1 Create Template Files in `notes/templates/`

**File: `notes/templates/concept.md`**
```markdown
---
type: concept
topic: {{topic}}
difficulty: beginner/intermediate/advanced
related_concepts: []
related_code: []
tags: []
created: {{date}}
---

# {{title}}

## Definition

## Intuition
Why does this matter? What's the big picture?

## Mathematical Formulation
Use Typst syntax for math:

$bold(x) in RR^n$

$$
f(x) = sum_(i=1)^n w_i x_i + b
$$

## Properties
- Property 1
- Property 2

## Implementation Notes
[[code/notebooks/related-notebook.ipynb]]

## Related Concepts
- [[concept-1]]
- [[concept-2]]

## References
- Source 1
- Source 2
```

**File: `notes/templates/moc.md`**
```markdown
---
type: moc
tags: [moc]
---

# Map of Content: {{title}}

## Overview
Brief description of this domain/topic area.

## Learning Path
1. Start with: [[]]
2. Then understand: [[]]
3. Build on: [[]]

## Core Concepts
- [[concept-1]]
- [[concept-2]]
- [[concept-3]]

## Code & Implementations
```dataview
TABLE file.name as "Notebook", file.mtime as "Last Modified"
FROM "code/notebooks"
WHERE contains(file.name, "{{topic}}")
SORT file.mtime DESC
```

## Projects Using This
- [[project-1]]
- [[project-2]]

## Key Resources
- Papers: 
- Books:
- Courses:
```

**File: `notes/templates/paper-notes.md`**
```markdown
---
type: literature
paper_title: "{{title}}"
authors: []
year: 
url: 
tags: [paper]
---

# {{title}}

## Metadata
- **Authors**: 
- **Year**: 
- **Venue**: 
- **URL**: 

## Summary
One paragraph summary of the main contribution.

## Key Insights
1. 
2. 
3. 

## Methods
What approaches/algorithms were used?

## Results
Key findings and numbers.

## Related Work
- [[related-paper-1]]
- [[related-concept]]

## Code/Implementation
- Official repo: 
- Related notebooks: [[code/notebooks/]]

## Personal Notes
Thoughts, questions, ideas for application.
```

**File: `notes/templates/notebook-reference.md`**
```markdown
---
type: code-reference
notebook: "{{notebook_path}}"
language: python
tags: [code]
created: {{date}}
---

# {{title}}

**Location**: `code/notebooks/{{filename}}.ipynb`

## Purpose
What does this notebook do?

## Key Functions/Classes
- `function_name()` - Description
  - Related concept: [[concept-name]]

## Datasets Used
- Dataset name: `data/path/to/data.csv`

## Results
- Metric 1: value
- Metric 2: value

## Related Concepts
- [[concept-1]]
- [[concept-2]]

## Dependencies
```python
import pandas as pd
import numpy as np
# ... other imports
```

## Usage Notes
How to run this notebook, any special requirements.
```

### 5.2 Configure Templater
1. Settings → Templater → Template folder location: `notes/templates`
2. Settings → Templater → Enable folder templates (optional)

---

## 6. Linking Strategy: Code ↔ Notes

### 6.1 Linking from Notes to Code
**In concept notes:**
```markdown
# Gradient Descent

## Implementation
See notebook: [[code/notebooks/gradient-descent-demo.ipynb]]

Python module: [[code/scripts/optimizer.py]]
```

### 6.2 Creating Reference Notes for Code
For each important notebook, create a reference note:

**File: `notes/01-concepts/machine-learning/gradient-descent-notebook.md`**
```markdown
---
notebook: code/notebooks/gradient-descent-demo.ipynb
concepts: [gradient-descent, optimization]
---

# Gradient Descent Implementation

This notebook implements [[gradient-descent]] using Python.

**Notebook**: [[code/notebooks/gradient-descent-demo.ipynb]]

## What it covers
- Basic gradient descent
- Learning rate experiments
- Convergence analysis

## Related Concepts
- [[optimization]]
- [[learning-rate]]
- [[convergence]]
```

### 6.3 Using Dataview to Query Code
Find all notebooks related to linear algebra:

```markdown
# Linear Algebra Implementations

\`\`\`dataview
TABLE 
  file.name as "File",
  file.mtime as "Modified"
FROM "code/notebooks"
WHERE contains(file.name, "linear-algebra") 
   OR contains(file.name, "matrix")
SORT file.mtime DESC
\`\`\`
```

---

## 7. Jupyter Notebook Integration

### 7.1 Using jupytext for Better Git Diffs
```bash
# Install jupytext
pip install jupytext

# Pair notebooks with .py files
cd code/notebooks
jupytext --set-formats ipynb,py:percent *.ipynb
```

This creates `.py` versions of your notebooks that are:
- Easier to diff in git
- Can be linked to specific functions
- Better for code review

### 7.2 Add to .gitignore (optional)
If you want to track only `.py` versions:
```gitignore
code/notebooks/*.ipynb
```

---

## 8. GitHub Workflow

### 8.1 Commit the Integration
```bash
git add .
git commit -m "Add Obsidian knowledge base structure"
git push origin obsidian-integration

# After reviewing, merge to main
git checkout main
git merge obsidian-integration
git push origin main
```

### 8.2 Obsidian Git Auto-Sync
The Obsidian Git plugin will now automatically:
- Commit changes every 15 minutes
- Pull on startup
- Push to GitHub

### 8.3 Manual Commands
**Via Command Palette (Cmd/Ctrl + P):**
- `Obsidian Git: Commit all changes`
- `Obsidian Git: Push`
- `Obsidian Git: Pull`

**Shell aliases** (add to `~/.bashrc` or `~/.zshrc`):
```bash
alias ds-sync='cd ~/path/to/Data_Science_be_like && git add . && git commit -m "sync: $(date +%Y-%m-%d)" && git push'
alias ds-pull='cd ~/path/to/Data_Science_be_like && git pull'
alias ds-status='cd ~/path/to/Data_Science_be_like && git status'
```

---

## 9. Example Workflow: Learning Linear Algebra

### Step 1: Create MOC (Hub Note)
**File: `notes/04-MOCs/linear-algebra-moc.md`**
```markdown
# Linear Algebra - MOC

## Core Concepts
- [[vectors]]
- [[matrices]]
- [[eigenvalues-eigenvectors]]
- [[matrix-decomposition]]

## Code Implementations
- [[code/notebooks/matrix-operations.ipynb]]
- [[code/notebooks/eigenvalue-demo.ipynb]]
```

### Step 2: Create Concept Notes
**File: `notes/01-concepts/linear-algebra/eigenvalues.md`**
```markdown
---
type: concept
topic: linear-algebra
difficulty: intermediate
related_code: 
  - code/notebooks/eigenvalue-demo.ipynb
tags: [linalg, eigenvalues]
---

# Eigenvalues and Eigenvectors

## Definition
For matrix $A$, vector $v$ is an eigenvector with eigenvalue $lambda$ if:

$$
A bold(v) = lambda bold(v)
$$

## Code Implementation
[[code/notebooks/eigenvalue-demo.ipynb]]
```

### Step 3: Link Notebook
Create `notes/01-concepts/linear-algebra/eigenvalue-notebook-ref.md` linking to the actual notebook.

### Step 4: View Graph
Open Graph view to see connections between concepts and code!

---

## 10. Advanced Features

### 10.1 Dataview Query Examples

**Find all unfinished concepts:**
```markdown
\`\`\`dataview
LIST
FROM "notes/01-concepts"
WHERE !completed
\`\`\`
```

**Recent notebook activity:**
```markdown
\`\`\`dataview
TABLE file.mtime as "Modified"
FROM "code/notebooks"
SORT file.mtime DESC
LIMIT 10
\`\`\`
```

**Concepts by difficulty:**
```markdown
\`\`\`dataview
TABLE topic, difficulty
FROM "notes/01-concepts"
WHERE type = "concept"
SORT difficulty, topic
\`\`\`
```

### 10.2 Using Canvas for Visual Planning
- Create project roadmaps
- Map out learning paths
- Visualize relationships between topics

### 10.3 Typst Math Tips
```markdown
# Common Typst patterns for ML/Math

# Vectors and matrices
$bold(w), bold(x), bold(y)$
$A = mat(a, b; c, d)$

# Calculus
$diff/(diff x) f(x)$
$integral_a^b f(x) dif x$

# ML notation
$hat(y) = sigma(bold(w)^T bold(x) + b)$
$cal(L) = sum_(i=1)^n (y_i - hat(y)_i)^2$

# Probability
$P(A | B) = (P(B | A) P(A)) / P(B)$
```

---

## 11. Updated README for Your Repo

Add this section to your `README.md`:

```markdown
## 📚 Knowledge Base Structure

This repository uses Obsidian for knowledge management. The structure is:

- `notes/` - Obsidian vault with concepts, MOCs, and documentation
- `code/` - Jupyter notebooks and Python scripts
- `data/` - Datasets (not tracked in git)
- `assets/` - Images, PDFs, and other resources

### Using the Knowledge Base

1. Install [Obsidian](https://obsidian.md/)
2. Open this repository folder as a vault
3. Install recommended plugins (see notes/templates/setup-guide.md)
4. Start with the MOCs in `notes/04-MOCs/`

### Linking Code and Concepts

Concepts in `notes/` link to implementations in `code/notebooks/`. Use the graph view to explore connections!
```

---

## 12. Installation Checklist

- [ ] Backup current repo state
- [ ] Run migration script
- [ ] Review and adjust moved files
- [ ] Install Obsidian
- [ ] Open Data_Science_be_like as Obsidian vault
- [ ] Install plugins: Obsidian Git, Wypst, Dataview, Templater
- [ ] Configure plugin settings
- [ ] Create template files in `notes/templates/`
- [ ] Update .gitignore
- [ ] Install jupytext: `pip install jupytext`
- [ ] Pair notebooks with .py files
- [ ] Create first MOC note
- [ ] Test Typst math rendering
- [ ] Configure Obsidian Git auto-backup
- [ ] Commit and push changes
- [ ] Update README.md

---

## 13. Maintaining Both Code and Notes

### Daily Workflow
1. **Start**: Obsidian Git auto-pulls latest changes
2. **Work**: 
   - Take notes in Obsidian
   - Work on notebooks/code in your IDE
   - Link concepts to code
3. **Save**: Obsidian Git auto-commits every 15 minutes
4. **End**: Manual push or wait for auto-push

### Best Practices
- Create a note when learning a new concept
- Link concept notes to implementations
- Use MOCs to organize major topics
- Tag consistently: `#ml`, `#linalg`, `#calculus`
- Review graph view weekly to find connections

---

## 14. Resources

- **Your Repo**: https://github.com/Luna-v0/Data_Science_be_like
- **Obsidian**: https://obsidian.md/
- **Obsidian Git**: https://github.com/denolehov/obsidian-git
- **Obsidian Wypst**: https://github.com/0xbolt/obsidian-wypst
- **Dataview**: https://blacksmithgu.github.io/obsidian-dataview/
- **Jupytext**: https://jupytext.readthedocs.io/
- **Typst Docs**: https://typst.app/docs/

---

**Happy learning! Your data science journey is now documented! 🚀📊🧠**