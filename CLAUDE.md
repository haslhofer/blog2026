# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A personal blog/portfolio site built with Flask, featuring a clean editorial design with warm paper aesthetics. The site showcases technical writing, travel itineraries, and personal essays. Deployed as a containerized application to Azure Web App using GitHub Actions CI/CD.

## Architecture

**Simple Flask Application:**
- `app.py` - Single-file Flask app with route definitions
- `templates/` - Jinja2 HTML templates, each corresponding to a route
- `static/` - CSS, images, and other static assets
  - `static/css/style.css` - Complete styling system with custom CSS variables
  - `static/images/` - Blog images and assets

**Key Design System:**
- Uses CSS custom properties (variables) for theming
- Color scheme: Warm paper theme with Orbital (blue) and NGCC (brown) accent colors
- Typography: Newsreader (serif), Inter (sans), JetBrains Mono (mono)
- Editorial/technical paper styling throughout

## Development Commands

### Local Development
```bash
# Create/activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
# Runs on http://localhost:5000 with debug=True
```

### Docker
```bash
# Build image
docker build -t blog2026 .

# Run container locally
docker run -p 8000:80 blog2026
# Access at http://localhost:8000

# Build for production (multi-platform)
docker buildx build --platform linux/amd64 -t blog2026 .
```

## Deployment

**GitHub Actions Workflow** (`.github/workflows/docker-ghcr.yml`):
1. Triggers on push to `main` branch
2. Builds Docker image using buildx
3. Pushes to GitHub Container Registry (ghcr.io)
4. Tags with both `sha-<short-sha>` and `latest`
5. Deploys to Azure Web App (if Azure credentials configured)

**Required GitHub Secrets/Variables:**
- `AZURE_CREDENTIALS` - Service principal JSON for Azure login
- `AZURE_WEBAPP_NAME` (variable) - Name of the Azure Web App

**Azure Resources:**
- Container Registry: For storing Docker images
- App Service Plan: B1 Basic tier (~$13/month)
- Web App: Runs the container

See `AZURE_DEPLOYMENT.md` for complete Azure setup instructions.

## Adding New Pages

1. Add route in `app.py`:
```python
@app.route('/page-name')
def page_name():
    return render_template('page-name.html')
```

2. Create template in `templates/page-name.html`
3. Add link to homepage in `templates/index.html` if desired

**Template Structure:**
- All pages use the editorial design system from `style.css`
- Common patterns: `.hero`, `.container`, `.section`, `.prose` classes
- Navigation: Use `.nav` and `.nav-back` for back links

## Key Files

- `app.py:1-42` - All routes and Flask app configuration
- `Dockerfile:1-16` - Production container setup with gunicorn
- `templates/index.html:1-176` - Homepage with page cards grid
- `static/css/style.css:1-731` - Complete design system and components
