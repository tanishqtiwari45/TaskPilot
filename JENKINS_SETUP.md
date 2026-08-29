# Jenkins CI/CD Setup Guide for TaskPilot

**Project:** TaskPilot  
**Pipeline:** Jenkins Declarative Pipeline  
**Repository:** https://github.com/tanishqtiwari45/TaskPilot  
**Status:** Ready for Implementation  

---

## 1. PREREQUISITES

### 1.1 Jenkins Server Requirements

**Jenkins Installation:**
```bash
# Windows (via Chocolatey)
choco install jenkins

# Or download from: https://www.jenkins.io/download/
# Then run the installer
```

**Jenkins Version:** 2.400+

**Java:** OpenJDK 11 or higher (usually included with Jenkins)

**Jenkins Home:** Default is `C:\ProgramData\Jenkins\`

**Port:** `8080` (default)

### 1.2 Node Requirements

**Windows Jenkins Controller Node:**
- OS: Windows 10/11 or Windows Server
- RAM: 4GB minimum (8GB recommended)
- Disk: 20GB minimum
- Network: Access to GitHub and MySQL

**Software Installed:**
```powershell
# Check Python
python --version          # Should be 3.13+

# Check Node.js
node --version            # Should be 18+
npm --version             # Usually included with Node

# Check Git
git --version             # Should be 2.30+
```

### 1.3 Jenkins Plugins Required

**Essential Plugins:**
1. **Pipeline** - Core pipeline support
2. **Pipeline: Groovy** - Declarative pipeline syntax
3. **Git** - Git repository integration
4. **GitHub** - GitHub integration
5. **GitHub Branch Source** - GitHub webhook support

**Installation Steps:**
```
1. Go to Jenkins Dashboard
2. Click "Manage Jenkins" → "Manage Plugins"
3. Go to "Available" tab
4. Search for each plugin name
5. Check the checkbox
6. Click "Install without restart"
7. Restart Jenkins when prompted
```

---

## 2. CREDENTIALS SETUP

### 2.1 GitHub Credentials

**Purpose:** Allow Jenkins to clone the repository from GitHub

**Steps:**

1. **Go to Credentials:**
   - Jenkins Dashboard → Credentials → System → Global credentials

2. **Add GitHub SSH Key or Token:**
   
   **Option A: SSH Key (Recommended)**
   ```
   - Click "Add Credentials"
   - Kind: "SSH Username with private key"
   - ID: github-credentials
   - Username: git
   - Private Key: [Paste your GitHub SSH private key]
     (Or select "From the Jenkins controller" and paste key)
   - Passphrase: [If key has passphrase]
   - Click Save
   ```

   **Option B: GitHub Personal Access Token**
   ```
   - Click "Add Credentials"
   - Kind: "Username with password"
   - ID: github-credentials
   - Username: [Your GitHub username]
   - Password: [Your GitHub Personal Access Token]
   - Click Save
   ```

**Get GitHub SSH Key:**
```powershell
# Generate SSH key if you don't have one
ssh-keygen -t ed25519 -C "your_email@example.com"

# Get the public key
type C:\Users\[YourUsername]\.ssh\id_ed25519.pub

# Add to GitHub:
# GitHub.com → Settings → SSH and GPG keys → New SSH key
```

**Get GitHub Personal Access Token:**
```
1. Go to GitHub.com
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. Click "Generate new token"
4. Select scopes: 
   - repo (Full control)
   - admin:repo_hook (Write access to hooks)
5. Copy the token
6. Paste into Jenkins credentials
```

### 2.2 Database Credentials (Optional - For Future Phases)

For now, database credentials will be in environment variables. For future deployment phases:

```
Kind: "Secret text"
ID: taskpilot-db-password
Secret: [Your MySQL root password]

Kind: "Secret text"
ID: taskpilot-secret-key
Secret: [Your Flask SECRET_KEY]
```

---

## 3. JENKINS JOB CONFIGURATION

### 3.1 Create a New Pipeline Job

**Steps:**

1. **Navigate to Jenkins Dashboard**
   - Open `http://localhost:8080`

2. **Create New Job**
   - Click "New Item"
   - Enter job name: `TaskPilot-CI`
   - Select "Pipeline"
   - Click "OK"

3. **Configure Job**
   ```
   General:
   ├─ Discard old builds: Keep 10 most recent
   ├─ GitHub project: https://github.com/tanishqtiwari45/TaskPilot
   └─ Pipeline definition: Pipeline script from SCM

   Build Triggers:
   ├─ GitHub hook trigger for GITScm polling
   └─ Enable "Build when a change is pushed to GitHub"

   Pipeline:
   ├─ Definition: Pipeline script from SCM
   ├─ SCM: Git
   ├─ Repository URL: https://github.com/tanishqtiwari45/TaskPilot.git
   ├─ Credentials: github-credentials
   ├─ Branch: */main
   ├─ Script Path: Jenkinsfile
   └─ Lightweight checkout: Leave checked
   ```

4. **Click Save**

### 3.2 Test the Pipeline

**First Test Run (Manual):**

1. Go to job page: `TaskPilot-CI`
2. Click "Build Now"
3. Watch the build execute
4. Check console output for logs

**Expected Output:**
```
╔════════════════════════════════════════════════╗
║             STAGE: CHECKOUT                    ║
╚════════════════════════════════════════════════╝
✓ Repository cloned successfully

╔════════════════════════════════════════════════╗
║          STAGE: BACKEND SETUP                  ║
╚════════════════════════════════════════════════╝
✓ Backend setup completed successfully

╔════════════════════════════════════════════════╗
║          STAGE: BACKEND TESTS                  ║
╚════════════════════════════════════════════════╝
✓ Backend tests completed

╔════════════════════════════════════════════════╗
║         STAGE: FRONTEND SETUP                  ║
╚════════════════════════════════════════════════╝
✓ Frontend setup completed successfully

╔════════════════════════════════════════════════╗
║         STAGE: FRONTEND BUILD                  ║
╚════════════════════════════════════════════════╝
✓ Frontend build completed successfully

╔════════════════════════════════════════════════╗
║               ✓ BUILD SUCCESSFUL                ║
╚════════════════════════════════════════════════╝
```

**If Build Fails:**
- Check console output for error message
- Verify Python and Node.js are installed
- Verify Python/Node versions are compatible
- Check Git repository URL and credentials

---

## 4. GITHUB WEBHOOK INTEGRATION

### 4.1 Configure Jenkins Webhook

**In Jenkins:**

1. Go to `TaskPilot-CI` job
2. Click "Configure"
3. Go to "Build Triggers" section
4. Check: "GitHub hook trigger for GITScm polling"
5. Click Save

**Jenkins Webhook URL:** `http://localhost:8080/github-webhook/`

### 4.2 Add Webhook to GitHub Repository

**Steps:**

1. Go to GitHub repository: https://github.com/tanishqtiwari45/TaskPilot
2. Click "Settings"
3. Go to "Webhooks"
4. Click "Add webhook"
5. Fill in the form:
   ```
   Payload URL: http://localhost:8080/github-webhook/
   Content type: application/json
   Which events would you like to trigger this webhook?
   ├─ Just the push event (selected)
   └─ Or custom events → Select:
      ├─ Push
      ├─ Pull requests
      └─ Releases
   
   Active: Checked
   ```
6. Click "Add webhook"

**Note for Remote Jenkins:**
If Jenkins is running on a remote server (not localhost):
- Use your server's public IP: `http://[server-ip]:8080/github-webhook/`
- Ensure firewall allows port 8080
- Or use ngrok for tunneling: `ngrok http 8080`

### 4.3 Test Webhook

**Verify Webhook Connection:**

1. Go to webhook settings on GitHub
2. Scroll to "Recent Deliveries"
3. Check if Jenkins received the payload
4. Green checkmark = successful delivery
5. Red X = failed delivery

**Manual Test:**

1. Push a commit to GitHub:
   ```bash
   git add Jenkinsfile
   git commit -m "Add Jenkins CI pipeline"
   git push origin main
   ```

2. Check Jenkins:
   - Go to `TaskPilot-CI` job
   - Verify a new build appeared in "Build History"
   - Build should start automatically within 1-2 seconds

---

## 5. ENVIRONMENT SETUP FOR CI

### 5.1 Database for CI Builds

The Jenkinsfile currently runs syntax checks only. For future phases that include database:

**Option 1: Docker Container (Recommended for CI)**
```bash
# Run MySQL in Docker
docker run -d --name mysql-taskpilot \
  -e MYSQL_ROOT_PASSWORD=ci_password \
  -e MYSQL_DATABASE=task_pilot \
  -p 3306:3306 \
  mysql:8.0
```

**Option 2: Local MySQL Installation**
```bash
# Ensure MySQL is running
net start MySQL80          # Windows
# or use MySQL Shell
```

### 5.2 Environment Variables in Jenkinsfile

**Current Configuration (In Jenkinsfile):**
```groovy
environment {
    BACKEND_DIR = '.'
    FRONTEND_DIR = 'frontend'
    VENV_DIR = "${WORKSPACE}/.venv"
    PYTHONPATH = "${WORKSPACE}"
    NODE_PATH = "${FRONTEND_DIR}/node_modules"
}
```

**To Add Database Variables (Future):**

1. Create a `.env.ci` file in repository:
   ```
   FLASK_ENV=testing
   SECRET_KEY=ci-secret-key
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=ci_password
   DB_NAME=task_pilot_ci
   ```

2. Update Jenkinsfile to load it:
   ```groovy
   stage('Backend Setup') {
       steps {
           sh '''
               . ${VENV_DIR}/bin/activate
               export $(cat .env.ci | xargs)
               pip install -r requirements.txt
           '''
       }
   }
   ```

---

## 6. BUILD PIPELINE FLOW

### 6.1 Automated Flow (GitHub to Jenkins)

```
Developer commits to GitHub
       ↓
GitHub sends webhook to Jenkins
       ↓
Jenkins receives webhook
       ↓
Jenkins-CI job triggers automatically
       ↓
Pipeline Stages Execute:
├─ Checkout: Clone code
├─ Backend Setup: Install deps
├─ Backend Tests: Run tests
├─ Frontend Setup: npm install
├─ Frontend Build: npm run build
└─ Success/Failure
       ↓
Build completes
       ↓
Developer notified (email/GitHub)
```

### 6.2 Manual Flow

```
Go to Jenkins Dashboard
       ↓
Click "TaskPilot-CI"
       ↓
Click "Build Now"
       ↓
Pipeline executes
       ↓
View results in console output
```

---

## 7. TROUBLESHOOTING

### Issue: Webhook Not Triggering Build

**Solution:**
1. Verify webhook is active on GitHub (green hook)
2. Check "Recent Deliveries" on GitHub webhook page
3. Verify Jenkins URL is reachable from GitHub
4. Check Jenkins firewall settings
5. Restart Jenkins if needed

**Test Command:**
```powershell
# Test GitHub webhook delivery (from Jenkins controller)
curl -X POST http://localhost:8080/github-webhook/ `
  -H "Content-Type: application/json"
```

### Issue: Build Fails at "Checkout"

**Solution:**
1. Verify SSH key is added to GitHub
2. Check credentials ID in Jenkins job config
3. Test Git connection:
   ```bash
   git clone https://github.com/tanishqtiwari45/TaskPilot.git
   ```

### Issue: Python Virtual Environment Error

**Solution:**
1. Ensure Python 3.13 is installed
2. Check Python is in PATH:
   ```powershell
   python --version
   ```
3. Clear old virtual environments:
   ```bash
   rm -r .venv
   ```

### Issue: NPM Install Fails

**Solution:**
1. Ensure Node.js 18+ is installed
2. Check npm cache:
   ```bash
   npm cache clean --force
   ```
3. Use `npm ci` instead of `npm install` (Jenkinsfile already does this)

### Issue: Frontend Build Failed

**Solution:**
1. Verify Vite config is correct
2. Check for TypeScript errors:
   ```bash
   npm run build -- --debug
   ```
3. Ensure dist/ directory is empty before rebuild

---

## 8. NEXT PHASES

### Phase 2: GitHub Integration (Automated Triggering)
- ✅ Webhook configured
- ✅ Tests automated
- Next: Add status checks to GitHub

### Phase 3: Dockerization
- Create Dockerfile for backend
- Create docker-compose for testing
- Add Docker build to pipeline

### Phase 4: UAT/PROD Deployment
- Create UAT environment
- Create PROD environment
- Add manual approval gates
- Add health checks
- Add rollback capability

---

## 9. QUICK START CHECKLIST

- [ ] Jenkins installed and running (port 8080)
- [ ] Python 3.13+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] Required Jenkins plugins installed
- [ ] GitHub credentials added to Jenkins
- [ ] TaskPilot-CI job created
- [ ] Jenkinsfile present in repository root
- [ ] GitHub webhook configured
- [ ] First manual build successful
- [ ] GitHub push triggers build automatically

---

## 10. USEFUL COMMANDS

### Jenkins Management

```powershell
# Start Jenkins (Windows)
net start Jenkins

# Stop Jenkins
net stop Jenkins

# Access Jenkins
Start-Process http://localhost:8080

# View Jenkins logs
Get-Content "C:\ProgramData\Jenkins\logs\*"
```

### Git Commands

```bash
# Add Jenkinsfile to repository
git add Jenkinsfile
git commit -m "Add Jenkins CI pipeline"
git push origin main

# View recent commits
git log --oneline -5
```

### Test Commands

```bash
# Test Python setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Test Frontend setup
cd frontend
npm ci
npm run build
```

---

## 11. SUPPORT & DOCUMENTATION

**Jenkins Documentation:** https://www.jenkins.io/doc/

**Declarative Pipeline Guide:** https://www.jenkins.io/doc/book/pipeline/syntax/

**GitHub Actions Docs:** https://docs.github.com/webhooks/

**TaskPilot Documentation:** See [README.md](README.md) and [JENKINS_CI_ANALYSIS.md](JENKINS_CI_ANALYSIS.md)

