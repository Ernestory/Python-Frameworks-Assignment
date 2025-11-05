<#
Helper PowerShell script to initialize, commit and push this repository to GitHub.

Usage (recommended):
1. Create a Personal Access Token (PAT) on GitHub with 'repo' scope.
2. In PowerShell set the token in the environment for the session:
   $env:GITHUB_TOKEN = 'ghp_...your_token_here...'
3. Run this script from the project root:
   .\push_to_github.ps1 -RemoteUrl 'https://github.com/Ernestory/Python-Frameworks-Assignment.git' -Branch 'main'

Notes:
- This script will NOT store your token in the repo. It uses the environment variable if present to perform a non-interactive push.
- If no token is provided, git will prompt for credentials interactively.
- The script will add a remote named 'origin' if none exists, or update it if different.
#>

param(
    [string]$RemoteUrl = 'https://github.com/Ernestory/Python-Frameworks-Assignment.git',
    [string]$Branch = 'main',
    [string]$CommitMessage = 'chore: add project files'
)

function ExecGit {
    param([string]$args)
    Write-Host "> git $args"
    git $args
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error 'Git is not installed or not on PATH. Please install Git before running this script.'
    exit 2
}

$pwdRoot = Get-Location
Write-Host "Running in project folder: $pwdRoot"

if (-not (Test-Path .git)) {
    Write-Host 'No git repository found — initializing.'
    ExecGit 'init'
} else {
    Write-Host 'Git repository already initialized.'
}

# Configure remote
$existingRemote = (git remote get-url origin 2>$null) -join "`n"
if ($existingRemote) {
    if ($existingRemote -ne $RemoteUrl) {
        Write-Host "Updating existing remote 'origin' from $existingRemote to $RemoteUrl"
        ExecGit "remote set-url origin $RemoteUrl"
    } else {
        Write-Host "Remote 'origin' already set to $RemoteUrl"
    }
} else {
    Write-Host "Adding remote 'origin' -> $RemoteUrl"
    ExecGit "remote add origin $RemoteUrl"
}

# Stage changes and commit
ExecGit 'add -A'

# Only commit if there are changes to commit
$status = git status --porcelain
if (-not $status) {
    Write-Host 'No changes to commit.'
} else {
    ExecGit "commit -m '$CommitMessage'"
}

# Push: if GITHUB_TOKEN env var exists, build an authenticated URL to avoid interactive prompt
if ($env:GITHUB_TOKEN) {
    # Build a secure URL that uses the token. This will only be used for the push command and not saved.
    $authUrl = $RemoteUrl -replace 'https://', "https://$($env:GITHUB_TOKEN)@"
    Write-Host 'Pushing using token from $env:GITHUB_TOKEN (not persisted).'
    ExecGit "push $authUrl HEAD:$Branch --set-upstream"
} else {
    Write-Host 'No GITHUB_TOKEN env var found — attempting interactive push (you will be prompted for credentials).'
    ExecGit "branch -M $Branch"
    ExecGit "push -u origin $Branch"
}

Write-Host 'Push helper finished.'
