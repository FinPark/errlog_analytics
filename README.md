# 🔍 Error Log Analytics

> **Erweiterte Analyse von AMS-Fehlerlogs mit intelligenter Mustererkennung**

Eine moderne Webanwendung zur automatisierten Analyse von Visual Objects (E_*.LOG) und .NET (EC_*.LOG) Fehlerprotokollen mit fortschrittlichen Visualisierungen und Erkennungsalgorithmen.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)
![Vue.js](https://img.shields.io/badge/vue.js-3.x-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/fastapi-latest-blue.svg)

---

## 📋 Projektübersicht

### 🎯 **Aufgabe**
Diese Anwendung automatisiert die Analyse von AMS-Fehlerprotokollen und transformiert unstrukturierte Log-Dateien in aussagekräftige Erkenntnisse durch:

- **Dual-Format-Unterstützung**: Simultane Verarbeitung von Visual Objects und .NET Logs
- **Intelligente Fehlererkennung**: Automatische Klassifizierung und Kritikalitätsbewertung
- **Zeitbasierte Analyse**: Erkennung von Fehlermustern und Peak-Zeiten
- **Benutzer-Aktivitätsanalyse**: Identifikation problematischer Benutzerprofile
- **Interaktive Dashboards**: Real-time Visualisierungen und Export-Funktionen

### 🔍 **Erkannte Log-Strukturen**
```
Visual Objects (E_*.LOG):
***********************ERROR********************************
Error Code: 33 [ DATA TYPE ERROR ]
Timestamp: 26.06.2025 10:35:29
...

.NET Logs (EC_*.LOG):
------------------------------
Logged at: 01.07.2025 15:07:17
System.AccessViolationException
...
```

---

## 🛠️ Technologie-Stack

### **Backend-Architektur**
| Technologie | Version | Zweck |
|-------------|---------|-------|
| **Python** | 3.11+ | Basis-Laufzeitumgebung |
| **FastAPI** | Latest | Async REST API Framework |
| **Pandas** | 2.1.3 | Datenverarbeitung und -analyse |
| **NumPy** | 1.25.2 | Numerische Berechnungen |
| **Redis** | 7-alpine | Caching und Session-Management |
| **Pydantic** | 2.5.0 | Datenvalidierung und Serialisierung |
| **python-dateutil** | 2.8.2 | Erweiterte Zeitstempel-Verarbeitung |

### **Frontend-Architektur**
| Technologie | Version | Zweck |
|-------------|---------|-------|
| **Vue.js** | 3.3.8 | Reactive Frontend Framework |
| **TypeScript** | 5.2.2 | Typsichere Entwicklung |
| **Quasar** | 2.14.2 | Material Design UI-Komponenten |
| **Chart.js** | 4.4.0 | Interaktive Datenvisualisierung |
| **Vite** | 5.0.0 | Build-Tool und Development Server |
| **Pinia** | 2.1.7 | State Management |

### **DevOps & Tools**
- **Docker Compose**: Containerisierte Entwicklungsumgebung
- **uv**: Schnelles Python-Package-Management
- **ESLint + Prettier**: Code-Qualität und Formatierung
- **Pytest**: Backend-Testing Framework
- **Vitest**: Frontend-Testing Framework

---

## 🚀 Installation & Setup

### **📋 Voraussetzungen**

#### **Minimal-Setup (Docker) - Alle Betriebssysteme**
```bash
# Windows / macOS / Linux - Docker Desktop erforderlich
docker --version          # Docker 20.0+
docker-compose --version  # Compose 2.0+

# Windows: PowerShell oder Command Prompt verwenden
# macOS/Linux: Terminal verwenden
# Hinweis: Port 8080 statt 8000 für Windows-Kompatibilität
```

#### **Entwicklung-Setup (Optional)**
```bash
# Für lokale Entwicklung
python --version          # Python 3.11+
node --version            # Node.js 18+
npm --version             # npm 8+
```

### **⚡ Schnellstart (Empfohlen)**

```bash
# 1. Repository klonen
git clone <repository-url>
cd errlog_analytics

# 2. Container starten (automatisches Build & Setup)
# Windows PowerShell/CMD:
docker-compose up -d

# macOS/Linux Terminal:
docker-compose up -d

# 3. Anwendung öffnen (alle Betriebssysteme)
# Frontend: http://localhost:3001
# Backend:  http://localhost:8080
# API-Docs: http://localhost:8080/docs
```

### **🪟 Windows-spezifische Hinweise**

```powershell
# Docker Desktop für Windows installieren
# WSL2 Backend empfohlen für bessere Performance

# PowerShell Befehle:
git clone <repository-url>
Set-Location errlog_analytics
docker-compose up -d

# Bei Problemen mit Pfaden:
# Sicherstellen, dass Docker Desktop läuft
# Eventuell Docker Desktop neustarten
```

### **🔧 Manuelle Entwicklungsumgebung**

<details>
<summary><strong>Erweiterte Setup-Optionen anzeigen</strong></summary>

#### **Backend-Setup:**
```bash
cd backend

# Virtual Environment mit uv
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Dependencies installieren
uv pip install -r requirements.txt

# Redis starten (Docker)
docker run -d -p 6379:6379 --name errlog_redis redis:7-alpine

# Development Server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### **Frontend-Setup:**
```bash
cd frontend

# Dependencies installieren
npm install

# Development Server (Port 3001 - angepasst für Docker)
npm run dev

# Build für Production
npm run build
```

</details>

---

## 📖 Benutzeranleitung

### **1. 📁 Log-Dateien hochladen**

1. **Upload-Seite öffnen**: http://localhost:3001/upload
2. **Log-Typ auswählen**:
   - `Auto-detect`: Automatische Erkennung
   - `Visual Objects`: E_*.LOG Dateien
   - `.NET`: EC_*.LOG Dateien
3. **Dateien hinzufügen**:
   - Drag & Drop in die Upload-Zone
   - Oder "Select Files" für Datei-Browser
4. **Analyse starten**: "Analyze Files" klicken (Button befindet sich rechts neben "Selected Files")
5. **Echtzeit-Analyse**: Vollständige Verarbeitung aller Log-Dateien mit Fehler-Extraktion
6. **Automatische Weiterleitung**: Nach erfolgreicher Analyse automatische Weiterleitung zum Dashboard (2 Sekunden)

**Unterstützte Formate:**
- ✅ `.LOG` und `.log` Dateien
- ✅ Multiple Dateien gleichzeitig (getestet mit 500+ Dateien)
- ✅ Bis zu 100MB Gesamtgröße
- ✅ Automatische Format-Erkennung (E_*.LOG vs EC_*.LOG)
- ✅ Echtzeit-Parsing und Fehler-Extraktion

### **2. 📊 Ergebnisse analysieren**

Das Dashboard bietet verschiedene Analysebereiche:

#### **🔢 Übersichtskarten**
- **Total Errors**: Gesamtanzahl erkannter Fehler
- **Critical Errors**: Hochpriorisierte Fehler (Code 50, Access Violations)
- **Active Users**: Anzahl betroffener Benutzer
- **Files Analyzed**: Verarbeitete Dateien

#### **📈 Visualisierungen** (Interaktiv)
- **Error Timeline**: Zeitbasierte Fehlerverteilung mit Dual-Achsen
- **Error Types**: Kreisdiagramm der Fehlercode-Verteilung (klickbar für Filterung)
- **User Activity**: Balkendiagramm der Benutzer-Aktivitäten
- **Critical Alerts**: Liste hochpriorisierter Fehler

#### **🔍 Detailansicht**
- **Sortierbare Tabelle** mit allen Fehlern (zeigt alle hochgeladenen Einträge)
- **Suchfunktion** für spezifische Einträge
- **Interaktive Filterung** durch Klick auf Diagramm-Segmente
- **Refresh-Funktion** für Datenaktualisierung
- **Export-Funktionen** (CSV, JSON, PDF)

### **3. 🎯 Log-Format-Spezifikationen**

#### **Visual Objects Logs (E_*.LOG)**
```
Dateiname: E_YYYYMMDD_USER.LOG
Delimiter: ***********************ERROR********************************
Zeitformat: DD.MM.YYYY HH:MM:SS (deutsches Format)
Fehlercodes: Numerisch mit Beschreibung
Beispiel: "33 [ DATA TYPE ERROR ]"
```

#### **.NET Logs (EC_*.LOG)**
```
Dateiname: EC_YYYYMMDD_USER.LOG
Delimiter: ------------------------------
Zeitformat: "Logged at: DD.MM.YYYY HH:MM:SS"
Exceptions: Standard .NET Exception-Typen
Beispiel: "System.AccessViolationException"
```

---

## 🔧 Entwicklung & Erweiterung

### **📁 Projektstruktur**
```
errlog_analytics/
├── 🐍 backend/                  # Python FastAPI Backend
│   ├── app/
│   │   ├── 🌐 api/              # REST API Endpoints
│   │   ├── ⚙️  core/            # Konfiguration & Settings
│   │   ├── 📝 models/           # Pydantic Datenmodelle
│   │   ├── 🔍 parsers/          # Log-Parser (VO + .NET)
│   │   ├── 📊 analyzers/        # Datenanalyse-Algorithmen
│   │   ├── ✅ validators/       # Datei-Validierung
│   │   └── 🛠️  utils/           # Helper-Funktionen
│   ├── 🧪 tests/               # Backend Tests
│   └── 📦 requirements.txt     # Python Dependencies
├── 🎨 frontend/                # Vue.js Frontend
│   ├── src/
│   │   ├── 🧩 components/       # Wiederverwendbare Komponenten
│   │   ├── 📄 pages/            # Seiten-Komponenten
│   │   ├── 🔗 services/         # API-Integration
│   │   ├── 📋 types/            # TypeScript Definitionen
│   │   └── 🛠️  utils/           # Frontend-Utilities
│   ├── 🌐 public/              # Statische Assets
│   └── 📦 package.json         # Node.js Dependencies
├── 🐳 docker/                  # Docker-Konfigurationen
├── 📚 docs/                    # Projektdokumentation
├── 📊 sample_logs/             # Test-Log-Dateien
└── 🔧 scripts/                # Deployment-Skripte
```

### **🌐 API-Endpunkte**

<details>
<summary><strong>Vollständige API-Referenz anzeigen</strong></summary>

#### **📤 Upload-Endpoints**
```http
POST   /api/upload              # Multi-File Upload
GET    /api/upload-status/{id}  # Upload-Status abrufen
```

#### **🔍 Analyse-Endpoints**
```http
POST   /api/analyze/detect-types    # Log-Typ-Erkennung
POST   /api/analyze/visual-objects  # VO-Analyse
POST   /api/analyze/dotnet         # .NET-Analyse
```

#### **📊 Daten-Endpoints**
```http
GET    /api/errors/summary         # Fehlerübersicht
GET    /api/errors/timeline        # Zeitbasierte Daten
GET    /api/errors/critical        # Kritische Fehler
GET    /api/errors/users          # Benutzer-Analyse
GET    /api/errors/frequency      # Häufigkeitsanalyse
```

#### **📋 Utility-Endpoints**
```http
GET    /                         # API-Info
GET    /health                   # Health-Check
GET    /docs                     # Swagger-Dokumentation
```

</details>

### **🧪 Testing & Qualitätssicherung**

```bash
# Backend Tests
cd backend
pytest --cov=app tests/                    # Mit Coverage
pytest -v tests/test_parsers.py           # Spezifische Tests

# Frontend Tests
cd frontend
npm run test                               # Unit Tests
npm run test:coverage                      # Mit Coverage
npm run lint                              # Code-Qualität
npm run format                            # Code-Formatierung

# Integration Tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

---

## 💡 Tipps & Feinheiten

### **🔧 Performance-Optimierung**

#### **Backend-Optimierungen:**
```python
# Redis-Caching für wiederholte Analysen
REDIS_CACHE_TTL = 3600  # 1 Stunde

# Async-Processing für große Dateien
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Batch-Processing für Multiple Files
BATCH_SIZE = 10  # Dateien pro Batch
```

#### **Frontend-Optimierungen:**
```typescript
// Lazy Loading für Charts
const DashboardCharts = defineAsyncComponent(
  () => import('@/components/DashboardCharts.vue')
)

// Virtual Scrolling für große Tabellen
<q-table virtual-scroll :rows-per-page-options="[0]" />
```

### **🛠️ Entwicklungs-Tipps**

#### **Hot Reloading optimieren:**
```bash
# Backend: Nur Python-Dateien überwachen
uvicorn app.main:app --reload --reload-include="*.py"

# Frontend: Port-Konflikte vermeiden
VITE_API_URL=http://localhost:8000 npm run dev
```

#### **Debug-Modi aktivieren:**
```bash
# Backend Debug-Logging
ENVIRONMENT=development DEBUG=true

# Frontend Vue DevTools
NODE_ENV=development npm run dev
```

### **🔍 Troubleshooting**

#### **Häufige Probleme:**

**Container starten nicht:**
```bash
# Ports prüfen (Linux/macOS):
netstat -tulpn | grep -E ':(3001|8000|6379)'

# Ports prüfen (Windows):
netstat -an | findstr "3001 8080 6379"

# Container-Logs anzeigen (alle Systeme):
docker-compose logs backend
docker-compose logs frontend
```

**Windows-spezifische Probleme:**
```powershell
# Docker Desktop nicht gestartet:
# - Docker Desktop aus Startmenü starten
# - Warten bis "Docker Desktop is running" angezeigt wird

# WSL2 Probleme:
# - Windows Features: "Virtual Machine Platform" aktivieren
# - Windows Features: "Windows Subsystem for Linux" aktivieren
# - System neustarten

# Firewall/Antivirus:
# - Docker Desktop in Firewall-Ausnahmen hinzufügen
# - Ports 3001, 8080, 6379 freigeben
```

**Upload funktioniert nicht:**
```bash
# CORS-Einstellungen prüfen
curl -v -X POST http://localhost:8000/api/upload

# File-Size-Limits prüfen
# In backend/app/core/config.py:
MAX_FILE_SIZE = 100 * 1024 * 1024
```

**Parser-Fehler:**
```bash
# Log-Format validieren
head -20 sample_logs/E_20250626_SWE.LOG

# Test-Parser ausführen
python -m app.parsers.visual_objects_parser sample_logs/
```

### **🔒 Sicherheitsaspekte**

#### **Datei-Upload-Sicherheit:**
- ✅ Datei-Typ-Validierung (nur .LOG)
- ✅ Datei-Größen-Limits (100MB)
- ✅ Input-Sanitization für alle Uploads
- ✅ Temporäre Datei-Bereinigung

#### **API-Sicherheit:**
- ✅ Rate-Limiting für Upload-Endpoints
- ✅ CORS-Konfiguration für Production
- ✅ Input-Validierung mit Pydantic
- ✅ Error-Handling ohne Information-Leakage

---

## 🚀 Deployment

### **🐳 Production-Docker-Setup**
```bash
# Production Build
docker-compose -f docker-compose.prod.yml up -d

# Mit Load Balancer
docker-compose -f docker-compose.prod.yml \
               -f docker-compose.lb.yml up -d
```

### **☁️ Cloud-Deployment**
```bash
# AWS ECS / Azure Container Instances
docker build -t errlog-analytics .
docker tag errlog-analytics:latest your-registry/errlog-analytics:latest
docker push your-registry/errlog-analytics:latest
```

---

## 📞 Support & Beitrag

### **🐛 Bug Reports**
Für Fehlerberichte und Feature-Requests erstellen Sie bitte ein Issue im GitHub-Repository.

### **🤝 Beitragen**
1. Repository forken
2. Feature-Branch erstellen (`git checkout -b feature/amazing-feature`)
3. Änderungen committen (`git commit -m 'Add amazing feature'`)
4. Branch pushen (`git push origin feature/amazing-feature`)
5. Pull Request erstellen

### **📄 Lizenz**
Dieses Projekt steht unter der MIT-Lizenz. Details siehe [LICENSE](LICENSE) Datei.

---

<div align="center">

**🔍 Error Log Analytics** - Transforming chaos into insights

[![GitHub](https://img.shields.io/badge/github-repository-blue.svg)](https://github.com/your-username/errlog_analytics)
[![Docker Hub](https://img.shields.io/badge/docker-hub-blue.svg)](https://hub.docker.com/r/your-username/errlog_analytics)

</div>