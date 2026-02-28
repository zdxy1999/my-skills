---
name: sync-my-skills
description: Synchronizes personal skills from GitHub repository to local skill directories. Pulls latest skills from zdxy1999/my-skills repo and intelligently syncs to target directories (overwrites existing skills, preserves local-only skills). Use when user wants to sync skills, update skills from GitHub, or copy skills from repo.
---

# Sync My Skills

Syncs personal skills from GitHub repository to local skill directories with intelligent merge behavior.

## When to use

Use when:
- User wants to sync skills from GitHub repository
- User mentions "sync skills", "update skills from repo", "pull latest skills"
- User wants to copy skills from one directory to another
- User needs to update Claude Code or OpenClaw skills from a central repo

## Supported Target Directories

| Platform | Default Path | Example |
|----------|--------------|---------|
| Claude Code | `~/.claude/skills/` | Local macOS/Linux |
| OpenClaw (remote) | `/root/.openclaw/workspace/skills/` | Remote server |

## Workflow

### 1. Identify Source and Target

- **Source**: GitHub repository `https://github.com/zdxy1999/my-skills`
- **Target**: User-specified directory (default: `~/.claude/skills/`)

Ask user which target to sync if not specified:
- Local Claude Code skills (`~/.claude/skills/`)
- Remote OpenClaw skills (requires SSH access)
- Custom path

### 2. Handle GitHub Authentication (if needed)

Check if the repository requires authentication (private repo) and handle accordingly:

```bash
# Configuration
REPO_OWNER="zdxy1999"
REPO_NAME="my-skills"
HTTPS_URL="https://github.com/${REPO_OWNER}/${REPO_NAME}.git"
SSH_URL="git@github.com:${REPO_OWNER}/${REPO_NAME}.git"

# Function to check if repo requires authentication
check_repo_access() {
    local url="$1"
    git ls-remote --exit-code "$url" HEAD &>/dev/null
    return $?
}

# Check authentication requirements
echo "Checking repository access..."
if ! check_repo_access "$HTTPS_URL"; then
    echo "HTTPS access failed - checking authentication options..."

    # Try SSH access
    if check_repo_access "$SSH_URL"; then
        REPO_URL="$SSH_URL"
        echo "Using SSH URL for authentication"
    else
        # Both failed, ask user for credentials
        echo ""
        echo "Authentication required. Please choose a method:"
        echo "1. Enter GitHub Personal Access Token (PAT)"
        echo "2. Use Git credential helper"
        echo "3. Configure SSH key access"
        echo "4. Skip sync"
        echo ""
        read -p "Choose option [1-4]: " AUTH_CHOICE

        case "$AUTH_CHOICE" in
            1)
                # Use PAT
                read -p "Enter GitHub Personal Access Token: " -s TOKEN
                REPO_URL="https://${TOKEN}@github.com/${REPO_OWNER}/${REPO_NAME}.git"
                echo ""
                echo "Using PAT for authentication"
                ;;
            2)
                # Use credential helper
                git config --global credential.helper store
                echo "Git credential helper configured. You'll be prompted for credentials."
                REPO_URL="$HTTPS_URL"
                ;;
            3)
                # SSH key setup
                echo ""
                echo "To use SSH authentication, please:"
                echo "1. Generate SSH key: ssh-keygen -t ed25519 -C 'your_email@example.com'"
                echo "2. Add public key to GitHub: https://github.com/settings/keys"
                echo "3. Test connection: ssh -T git@github.com"
                echo ""
                read -p "Press Enter after setting up SSH key, or 's' to skip: " CONFIRM
                if [[ "$CONFIRM" != "s" ]]; then
                    REPO_URL="$SSH_URL"
                    if ! check_repo_access "$REPO_URL"; then
                        echo "SSH authentication still failed. Please verify your setup."
                        exit 1
                    fi
                else
                    exit 0
                fi
                ;;
            4)
                echo "Sync cancelled."
                exit 0
                ;;
            *)
                echo "Invalid option. Using HTTPS (may fail without credentials)"
                REPO_URL="$HTTPS_URL"
                ;;
        esac
    fi
else
    REPO_URL="$HTTPS_URL"
fi
```

### 3. Prepare Source Directory

Use a fixed temp directory to avoid variable passing issues:

```bash
# Fixed temp directory for consistent access
TEMP_REPO="/tmp/my-skills-sync-$$"

# Check if source already exists and is a git repo
if [ -d "$TEMP_REPO" ]; then
    if [ -d "$TEMP_REPO/.git" ]; then
        echo "Updating existing repo..."
        cd "$TEMP_REPO"
        git pull origin main
    else
        # Exists but not a git repo, remove and clone
        echo "Removing non-git directory and cloning..."
        rm -rf "$TEMP_REPO"
        git clone "$REPO_URL" "$TEMP_REPO"
    fi
else
    # Directory doesn't exist, clone fresh
    echo "Cloning repository..."
    git clone "$REPO_URL" "$TEMP_REPO"
fi

SOURCE_DIR="$TEMP_REPO"
```

### 4. Smart Sync Operation

**Key Rules:**
- ✅ Overwrite: Existing skill in target (same name) → replace with repo version
- ✅ Preserve: Local-only skill (not in repo) → keep unchanged
- ✅ Add: New skill in repo (not in target) → copy to target
- ❌ Delete: Never remove local skills even if removed from repo

```bash
SOURCE_DIR="$TEMP_REPO/my-skills"
TARGET_DIR="$TARGET_PATH"  # User-specified

# Copy each skill from source to target
for skill_dir in "$SOURCE_DIR"/*/; do
    skill_name=$(basename "$skill_dir")

    # Skip non-skill directories (.git, .claude, etc.)
    if [[ "$skill_name" == .* ]] || [[ "$skill_name" == "sync-my-skills" ]]; then
        continue
    fi

    # Remove existing skill if present (overwrite)
    if [ -d "$TARGET_DIR/$skill_name" ]; then
        rm -rf "$TARGET_DIR/$skill_name"
    fi

    # Copy skill from repo
    cp -r "$skill_dir" "$TARGET_DIR/$skill_name"
    echo "Synced: $skill_name"
done

# List preserved local-only skills
for skill_dir in "$TARGET_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    if [ ! -d "$SOURCE_DIR/$skill_name" ]; then
        echo "Preserved (local): $skill_name"
    fi
done
```

### 5. Cleanup

```bash
rm -rf "$TEMP_REPO"
```

## Usage Examples

### Sync to Local Claude Code
```
User: Sync my skills
Agent: Syncing skills from zdxy1999/my-skills to ~/.claude/skills/...
```

### Sync to Remote OpenClaw
```
User: Sync skills to remote openclaw
Agent: I'll sync skills to /root/clawdbot/skills. This requires SSH access.
[Proceeds with sync via ssh or rsync]
```

### Sync to Custom Path
```
User: Sync skills to /custom/path/to/skills
Agent: Syncing skills from zdxy1999/my-skills to /custom/path/to/skills...
```

## Error Handling

| Error | Solution |
|-------|----------|
| Target directory doesn't exist | Ask to create or provide different path |
| Git clone fails (authentication) | Check authentication section above, provide PAT or SSH key |
| Git clone fails (network) | Check network connection, verify repo URL |
| Permission denied | Check write permissions on target directory |
| SSH access failed (remote sync) | Verify SSH keys or ask for credentials |
| Invalid credentials | Prompt user to re-enter PAT or verify GitHub token permissions |
| Repository not found | Verify repository URL and access rights (public/private) |

## Notes

- The skill being synced (`sync-my-skills`) should be skipped during sync to avoid conflicts
- Git metadata (`.git/`) is never copied to target
- Hidden directories starting with `.` are skipped unless explicitly requested
- Always show summary of sync actions: synced, preserved, added
- For GitHub authentication:
  - **PAT (Personal Access Token)**: Recommended for HTTPS access. Requires `repo` scope permissions
  - **SSH Keys**: Requires SSH public key added to GitHub account settings
  - **Credential Helper**: Stores credentials locally (use with caution on shared systems)
- When using PAT in URL format, credentials may appear in process listings. Consider using `git credential-store` or environment variables for better security
- If using PAT, ensure it has the minimum required permissions (`public_repo` for public repos, `repo` for private)
