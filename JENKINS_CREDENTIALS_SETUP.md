# Jenkins Credentials Setup - TaskPilot CI/CD Security Upgrade

## Status: Code Changes Complete ✅

**Date:** 2026-09-01  
**Changes:** All Jenkinsfile, .env.example, and .gitignore modifications have been committed and pushed to GitHub.

### What Changed

The TaskPilot CI/CD pipeline has been upgraded to use secure Jenkins Credentials instead of hardcoded secrets. The following files were modified:

1. **Jenkinsfile**: 
   - Removed `DB_PASSWORD` from environment block
   - Added `withCredentials()` binding to UAT Health Check stage
   - Added `withCredentials()` binding to PROD Health Check stage
   - Updated .env creation to use credential variables

2. **.env.example**: 
   - Added documentation about Jenkins Credentials
   - Clarified that secrets are managed by Jenkins in CI/CD

3. **.gitignore**: 
   - Enhanced protection for .env files and variants
   - Added patterns for IDE files, OS files, and build artifacts

### Git Commit

```
Commit: 1e60a36
Message: ci: move secrets to Jenkins Credentials, separate UAT/PROD config with withCredentials binding
Status: Pushed to https://github.com/tanishqtiwari45/TaskPilot.git
```

---

## Next Step: Create Jenkins Credentials (MANUAL)

**⚠️ CRITICAL:** The Jenkins Credentials must be created manually through the Jenkins UI before running the next build.

---

## Instructions: Create Credentials in Jenkins UI

### Step 1: Navigate to Jenkins Credentials

1. Open Jenkins: **http://localhost:8080** (or your ngrok URL)
2. Click **"Manage Jenkins"** (top-left sidebar)
3. Click **"Credentials"**
4. Click **"(global)"** (under "Stores scoped to Jenkins")

### Step 2: Create First Credential - taskpilot-uat-db

Click **"+ Add Credentials"** and fill in the form:

| Field | Value |
|-------|-------|
| **Kind** | Username with password |
| **Scope** | Global (Jenkins, nodes, items, all child items, etc) |
| **Username** | `root` |
| **Password** | `Octe@2026$#` |
| **ID** | `taskpilot-uat-db` |
| **Description** | TaskPilot UAT Database Credentials |

Click **"Create"**

### Step 3: Create Second Credential - taskpilot-uat-secret-key

Click **"+ Add Credentials"** and fill in the form:

| Field | Value |
|-------|-------|
| **Kind** | Secret text |
| **Scope** | Global (Jenkins, nodes, items, all child items, etc) |
| **Secret** | `taskpilot-uat-secret-key-2026` |
| **ID** | `taskpilot-uat-secret-key` |
| **Description** | TaskPilot UAT Flask SECRET_KEY |

Click **"Create"**

### Step 4: Create Third Credential - taskpilot-prod-db

Click **"+ Add Credentials"** and fill in the form:

| Field | Value |
|-------|-------|
| **Kind** | Username with password |
| **Scope** | Global (Jenkins, nodes, items, all child items, etc) |
| **Username** | `root` |
| **Password** | `YourProdPassword123!` (⚠️ DIFFERENT from UAT) |
| **ID** | `taskpilot-prod-db` |
| **Description** | TaskPilot PROD Database Credentials |

Click **"Create"**

### Step 5: Create Fourth Credential - taskpilot-prod-secret-key

Click **"+ Add Credentials"** and fill in the form:

| Field | Value |
|-------|-------|
| **Kind** | Secret text |
| **Scope** | Global (Jenkins, nodes, items, all child items, etc) |
| **Secret** | `taskpilot-prod-secret-key-2026-production` |
| **ID** | `taskpilot-prod-secret-key` |
| **Description** | TaskPilot PROD Flask SECRET_KEY |

Click **"Create"**

---

## Verification: All Credentials Created

After creating all four credentials, navigate to **"Manage Jenkins" → "Credentials" → "(global)"** and verify:

- ✅ **taskpilot-uat-db** (Username with password)
- ✅ **taskpilot-uat-secret-key** (Secret text)
- ✅ **taskpilot-prod-db** (Username with password)
- ✅ **taskpilot-prod-secret-key** (Secret text)

All four credentials should be listed with their respective icons.

---

## Next Steps After Creating Credentials

### 1. Trigger a Test Build

Push a test commit to GitHub to trigger Jenkins build #N:

```powershell
cd "c:\Users\Tanishq Tiwari\OneDrive\Desktop\task_pilot"
echo "# Security upgrade test - $(Get-Date)" >> README.md
git add README.md
git commit -m "test: verify Jenkins credentials integration"
git push origin main
```

### 2. Monitor Build Progress

Jenkins will automatically trigger a build. Watch the stages:

- **Stages 1-7**: Build, test, package (no credentials needed)
- **Stage 8 (UAT Health Check)**: 
  - ✅ Should load `taskpilot-uat-db` credentials
  - ✅ Should load `taskpilot-uat-secret-key`
  - ✅ No passwords should appear in console logs (should show `****`)
  - ✅ Flask should start on port 5000
  - ✅ Health check should pass
- **Stage 9**: Manual approval gate (click "Deploy to PROD")
- **Stage 10**: Copy package to PROD
- **Stage 11 (PROD Health Check)**:
  - ✅ Should load `taskpilot-prod-db` credentials
  - ✅ Should load `taskpilot-prod-secret-key`
  - ✅ No passwords should appear in console logs
  - ✅ Flask should start on port 5001
  - ✅ Health check should pass

### 3. Verify Security

**CRITICAL:** Check that no passwords appear in the Jenkins console output:

1. Open Jenkins Build #N
2. Click **"Console Output"**
3. Search for your database password: `Octe@2026$#`
   - ❌ Should NOT appear anywhere
4. Search for credential strings: `taskpilot-uat-secret-key`
   - ❌ Should NOT appear anywhere
5. You should only see masked values like: `****`

---

## Environment Variable Mapping

### UAT Build Stage

```
Jenkins Credential ID: taskpilot-uat-db
  ↓
usernameVariable: UAT_DB_USER → set to "root"
passwordVariable: UAT_DB_PASSWORD → set to "Octe@2026$#"
  ↓
.env file created with:
  DB_USER=%UAT_DB_USER% (resolves to "root")
  DB_PASSWORD=%UAT_DB_PASSWORD% (resolves to "Octe@2026$#" - MASKED in logs)

Jenkins Credential ID: taskpilot-uat-secret-key
  ↓
variable: UAT_SECRET_KEY → set to "taskpilot-uat-secret-key-2026"
  ↓
.env file created with:
  SECRET_KEY=%UAT_SECRET_KEY% (resolves to "taskpilot-uat-secret-key-2026" - MASKED in logs)
```

### PROD Build Stage (After Approval)

```
Jenkins Credential ID: taskpilot-prod-db
  ↓
usernameVariable: PROD_DB_USER → set to "root"
passwordVariable: PROD_DB_PASSWORD → set to "YourProdPassword123!"
  ↓
.env file created with:
  DB_USER=%PROD_DB_USER% (resolves to "root")
  DB_PASSWORD=%PROD_DB_PASSWORD% (resolves to "YourProdPassword123!" - MASKED in logs)

Jenkins Credential ID: taskpilot-prod-secret-key
  ↓
variable: PROD_SECRET_KEY → set to "taskpilot-prod-secret-key-2026-production"
  ↓
.env file created with:
  SECRET_KEY=%PROD_SECRET_KEY% (resolves to "taskpilot-prod-secret-key-2026-production" - MASKED in logs)
```

---

## Troubleshooting

### Issue: "Credentials not found" error in Jenkins build

**Cause:** Credential ID in Jenkinsfile doesn't match Jenkins UI

**Solution:**
1. Check Jenkins Credentials → verify exact credential IDs
2. Ensure no typos in Jenkinsfile `credentialsId` values
3. Rebuild after fixing

### Issue: Passwords still appearing in console logs

**Cause:** `withCredentials()` block not wrapping the bat script

**Solution:**
1. Review Jenkinsfile UAT Health Check and PROD Health Check stages
2. Verify `withCredentials()` wraps the entire bat block
3. Check for manual password prints in the script

### Issue: UAT passes but PROD fails

**Cause:** PROD credentials wrong or not created

**Solution:**
1. Verify `taskpilot-prod-db` and `taskpilot-prod-secret-key` exist
2. Check credential values match the database setup
3. Rebuild PROD stage after fixing

### Issue: "withCredentials is not defined" error

**Cause:** Jenkins Credentials Plugin not installed

**Solution:**
1. Go to Jenkins → Manage Jenkins → Manage Plugins
2. Search for "Credentials Plugin"
3. Install if missing
4. Restart Jenkins

---

## Security Best Practices

### Password Rotation (Quarterly)

To rotate PROD database password:
1. Update password in MySQL/MariaDB
2. Update `taskpilot-prod-db` credential in Jenkins UI
3. Next build uses new password
4. No code changes needed

### Credential Access Audit

Jenkins tracks all credential access. To view:
1. Jenkins → Manage Jenkins → System Log
2. Search for "Credentials accessed" entries
3. Verify only trusted builds accessed credentials

### Future Enhancement: Credential Restriction

Currently, all global credentials are accessible by all jobs. For better security:
1. Create a credential scoped to just the TaskPilot job
2. Go to Jenkins → TaskPilot job → Configure → Advanced
3. Restrict credentials to this job only

---

## Rollback Instructions

If the new credentials break the build, here's how to rollback:

### Quick Rollback (< 5 minutes)

```powershell
cd "c:\Users\Tanishq Tiwari\OneDrive\Desktop\task_pilot"

# Revert to previous commit
git revert --no-edit HEAD

# Or reset to previous
git reset --hard HEAD~1

# Push to trigger Jenkins with old code
git push origin main
```

### Delete Problematic Build

1. Jenkins → TaskPilot job
2. Find failed build number
3. Right-click → "Delete Build"

### Restore Previous Credentials

If credentials are the problem:
1. Jenkins → Credentials → (global)
2. Find credential → "Update"
3. Restore old value
4. Rebuild

---

## Success Checklist

- [ ] All 4 Jenkins credentials created
- [ ] Test build triggered (via git push)
- [ ] Stages 1-7 complete successfully
- [ ] Stage 8 (UAT Health Check) loads UAT credentials
- [ ] No passwords visible in console output
- [ ] Stage 9 (Manual Approval) requires click
- [ ] Stage 11 (PROD Health Check) loads PROD credentials
- [ ] PROD health check passes on port 5001
- [ ] GitHub webhook still triggers builds automatically
- [ ] Next build also succeeds with new config

---

## Support & Questions

For detailed analysis and troubleshooting, see:
- `JENKINS_SETUP.md` - Initial Jenkins setup
- `JENKINS_CI_ANALYSIS.md` - Security analysis that led to these changes
- `.env.example` - Environment variable documentation
- `Jenkinsfile` - Pipeline implementation with withCredentials blocks

For issues, review the "Troubleshooting" section above or consult the Rollback Instructions.

---

**Last Updated:** 2026-09-01  
**Status:** Ready for Credentials Setup and Testing
