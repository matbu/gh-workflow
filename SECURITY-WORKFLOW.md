# Security Scan Workflow Documentation

## Overview

This repository has two security workflows:

1. **security.yml** - Runs on Pull Requests (using the official Anthropic action)
2. **security-scan.yml** - Runs on commits and daily scans (custom Claude CLI integration)

## Configuration

### Required GitHub Secrets

Set these in your repository settings (Settings → Secrets and variables → Actions):

1. **GOOGLE_APPLICATION_CREDENTIALS**
   - Your GCP service account JSON key (entire JSON content)
   - Must have Vertex AI API access

2. **ANTHROPIC_VERTEX_PROJECT_ID**
   - Your GCP project ID where Vertex AI is enabled

### Workflows

#### security-scan.yml (Commit & Daily Scans)

**Triggers:**
- Push to `main` or `develop` branches
- Daily at 9:15 AM UTC
- Manual trigger via GitHub Actions UI

**What it does:**
1. Installs Claude Code CLI
2. Authenticates with Google Vertex AI
3. Runs comprehensive security scan
4. Creates a GitHub Issue with findings
5. Uploads results as artifacts

**Features:**
- Scans for: hardcoded secrets, SQL injection, XSS, insecure dependencies, auth issues, crypto weaknesses, path traversal, command injection
- Creates labeled issues (`security`, `automated`)
- Keeps scan results as artifacts for 30 days

#### security.yml (PR Reviews)

**Triggers:**
- Pull Requests to `main` or `develop`
- Manual trigger

**What it does:**
1. Reviews the changes in the PR
2. Posts findings as PR comments
3. Uploads results as artifacts

## How to Verify It's Working

### Test 1: Verify Vertex AI Authentication

1. Go to **Actions** tab in GitHub
2. Select **Security Scan (Commit & Daily)**
3. Click **Run workflow** (manual trigger)
4. Watch the workflow run - it should:
   - ✓ Install Claude CLI successfully
   - ✓ Create GCP credentials file
   - ✓ Run the security scan
   - ✓ Create a GitHub issue

### Test 2: Verify Vulnerability Detection

The repository includes `test-vulnerable.py` with intentional vulnerabilities:
- Hardcoded passwords and API keys
- SQL injection
- Command injection
- Path traversal
- Weak cryptography (MD5)

**To test:**

```bash
# Make a small change to trigger the workflow
echo "# Test scan" >> test-vulnerable.py
git add test-vulnerable.py
git commit -m "Test security scan"
git push origin main
```

**Expected results:**
- Workflow runs automatically on push
- Creates a GitHub issue titled "🔒 Security Scan Results - [date]"
- Issue should list all 5 vulnerabilities found
- Results artifact uploaded to Actions run

### Test 3: Check the GitHub Issue

After the workflow runs:

1. Go to **Issues** tab
2. Look for issue with title "🔒 Security Scan Results - [date]"
3. Should have labels: `security`, `automated`
4. Should contain:
   - Scan type (Scheduled/Commit)
   - Branch and commit info
   - List of findings with severity, files, descriptions

### Test 4: Download Scan Results

1. Go to **Actions** tab
2. Click on the completed workflow run
3. Scroll to **Artifacts** section
4. Download `security-scan-results-[commit-sha]`
5. Unzip and review the detailed results

## Troubleshooting

### Workflow fails with authentication error

**Symptom:** "Failed to create GCP credentials file"

**Fix:**
- Verify `GOOGLE_APPLICATION_CREDENTIALS` secret contains valid JSON
- Check the JSON is not corrupted (no extra quotes or escaping)
- Ensure the service account has Vertex AI permissions

### No issues created

**Symptom:** Workflow completes but no GitHub issue appears

**Possible causes:**
1. Check workflow logs for "Failed to create issue"
2. Ensure `issues: write` permission is set
3. Verify `GITHUB_TOKEN` has proper permissions

### Claude CLI fails

**Symptom:** "Claude scan failed"

**Fix:**
- Check `ANTHROPIC_VERTEX_PROJECT_ID` is correct
- Verify Vertex AI API is enabled in your GCP project
- Check Claude model availability in your region

### Daily scan not running

**Check:**
- Workflows → Security Scan (Commit & Daily)
- Look at the schedule runs
- GitHub may disable scheduled workflows if repo is inactive for 60 days

## Cost Considerations

**Vertex AI Pricing:**
- Each scan uses Claude Sonnet 4.5
- Cost depends on repository size and complexity
- Daily scans = ~30 scans/month
- Monitor usage in GCP Console → Vertex AI

**Recommendations:**
- Start with manual triggers to test
- Enable daily scans once confident
- Adjust schedule if costs are high (e.g., weekly: `0 9 * * 1`)

## Customization

### Change scan frequency

Edit `security-scan.yml`, line 12:
```yaml
- cron: '15 9 * * *'  # Daily at 9:15 AM UTC
```

Common patterns:
- `0 9 * * 1` - Weekly on Monday
- `0 9 1 * *` - Monthly on the 1st
- `0 9 * * 1-5` - Weekdays only

### Change severity threshold

Edit the prompt in `security-scan.yml` to focus on specific severities:
```
Focus only on Critical and High severity issues.
```

### Add more security checks

Edit the scan prompt to include:
- Framework-specific vulnerabilities
- Compliance checks (GDPR, HIPAA, etc.)
- License scanning
- Dependency vulnerabilities

## Next Steps

1. ✅ Verify authentication works (Test 1)
2. ✅ Confirm vulnerability detection (Test 2)  
3. ✅ Review first security issue (Test 3)
4. Configure issue auto-assignment or notifications
5. Integrate with Slack/Discord for alerts
6. Set up automated fixes for common issues
