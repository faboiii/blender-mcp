# Fabiolous.org – Homepage

Moderne Homepage fur [Fabiolous.org](https://fabiolous.org), deployed auf **Cloudflare Pages**.

## Deployment auf Cloudflare Pages

### Option 1: Cloudflare Dashboard (empfohlen)

1. Gehe zu [dash.cloudflare.com](https://dash.cloudflare.com)
2. Klicke auf **Pages** → **Create a project**
3. Verbinde dein GitHub-Repository (`faboiii/blender-mcp`)
4. Konfiguriere den Build:
   - **Branch**: `claude/create-fabiolous-homepage-fQAni`
   - **Build command**: *(leer lassen)*
   - **Build output directory**: `homepage/public`
5. Klicke **Save and Deploy**
6. Verbinde deine Domain `fabiolous.org` unter **Custom domains**

### Option 2: Wrangler CLI

```bash
# Install Wrangler
npm install -g wrangler

# Login
wrangler login

# Deploy aus dem homepage/ Verzeichnis
cd homepage
wrangler pages deploy public --project-name fabiolous-homepage
```

### Custom Domain verbinden

Im Cloudflare Dashboard:
1. Pages → `fabiolous-homepage` → **Custom domains**
2. Klicke **Set up a custom domain**
3. Gib `fabiolous.org` und `www.fabiolous.org` ein
4. Cloudflare konfiguriert DNS automatisch (wenn die Domain bei Cloudflare registriert ist)

## Struktur

```
homepage/
├── public/
│   ├── index.html   # Haupt-Homepage
│   └── style.css    # Styling
├── _redirects       # Cloudflare Pages Routing
├── wrangler.toml    # Cloudflare Konfiguration
└── README.md
```

## Features

- Modernes Dark-Mode Design
- Responsive (Mobile-first)
- CSS 3D animierter Würfel
- Smooth Scroll Navigation
- Kein Framework – reines HTML/CSS/JS
- Optimiert für Cloudflare Pages CDN
