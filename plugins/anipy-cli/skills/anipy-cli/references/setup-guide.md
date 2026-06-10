# anipy-cli Setup Guide — Windows

## Complete Dependency Installation Flow

This guide documents the exact commands for installing each dependency in the chain. All installations require user confirmation via `AskUserQuestion` before proceeding.

**Timeouts:** Use 300s for all installation commands (they download from the internet and can be slow). If an install command times out, check if the tool was partially installed before retrying — for scoop packages, run `scoop uninstall <pkg>` before re-running `scoop install <pkg>`.

## 1. uv (Python Package Manager)

### Check
```bash
uv --version
```

### Install

Try PowerShell 7 first (more reliable on Windows 11):
```bash
pwsh.exe -NoProfile -Command "irm https://astral.sh/uv/install.ps1 | iex"
```

If `pwsh.exe` not available, try standard PowerShell:
```bash
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
```

If PowerShell security module is broken (`Microsoft.PowerShell.Security` error), `pwsh.exe` is the only reliable path. Guide user to install PowerShell 7 via Microsoft Store if neither works.

### Verify
```bash
uv --version
```

If not found on PATH, check the expected install location directly:
```bash
~/.local/bin/uv --version
```

If the binary exists but is not on PATH, inform the user to restart their terminal.

## 2. anipy-cli

### Check
```bash
anipy-cli --version
```

### Install
```bash
uv tool install anipy-cli
```

This installs anipy-cli globally with all Python dependencies isolated. The binary goes to `~/.local/bin/` which uv adds to PATH.

### Verify
```bash
anipy-cli --version
```

If not found on PATH, check the expected install location directly:
```bash
~/.local/bin/anipy-cli --version
```

Expected output is a version string like `3.8.8` (any 3.x release works with this skill). If the binary exists but is not on PATH, inform the user to restart their terminal or add `~/.local/bin` to their PATH.

### Upgrade
```bash
uv tool upgrade anipy-cli
```

### Uninstall
```bash
uv tool uninstall anipy-cli
```

## 3. Scoop (Windows Package Manager)

Only needed if installing mpv. Skip if user already has a video player.

### Check
```bash
pwsh.exe -NoProfile -Command "scoop --version"
```

Or check if scoop directory exists:
```bash
ls ~/scoop/shims/scoop.ps1
```

### Install
```bash
pwsh.exe -NoProfile -Command "irm get.scoop.sh | iex"
```

**Important**: `powershell.exe` often fails with security module errors on Windows 11. Always prefer `pwsh.exe`.

### Post-Install PATH Issue

After installing scoop, the current bash session does NOT have scoop on PATH. Always use full paths:
```bash
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 <command>"
```

## 4. mpv (Video Player)

### Check
```bash
where.exe mpv 2>/dev/null
```

Or check scoop installation:
```bash
ls ~/scoop/apps/mpv/current/mpv.exe 2>/dev/null
```

### Install via Scoop

mpv is in the `extras` bucket:
```bash
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 bucket add extras; & $env:USERPROFILE\scoop\shims\scoop.ps1 install mpv"
```

This also installs 7zip as a dependency.

### Verify
After terminal restart:
```bash
mpv --version
```

### mpv Config Location (Scoop)
```
C:\Users\<username>\scoop\apps\mpv\current\portable_config\
```

## 5. VLC (Alternative Video Player)

### Check
```bash
where.exe vlc 2>/dev/null
# Also check common install paths:
ls "/c/Program Files/VideoLAN/VLC/vlc.exe" 2>/dev/null
ls "/c/Program Files (x86)/VideoLAN/VLC/vlc.exe" 2>/dev/null
```

### Install

VLC is typically installed manually from https://www.videolan.org/ or via:
```bash
winget install VideoLAN.VLC
```

VLC is often already installed on Windows machines.

## 6. anipy-cli Configuration

### Get Config Path
```bash
anipy-cli --config-path
```

Default: `C:\Users\<username>\AppData\Local\anipy-cli\config.yaml`

### Initial Config

On first run, anipy-cli generates a default config. Key fields to verify/update:

```yaml
# Set to detected player
player_path: mpv                    # if mpv on PATH
# or
player_path: C:\Program Files\VideoLAN\VLC\vlc.exe  # full path for VLC

# Download location (optional)
download_folder_path: C:\Users\<username>\Downloads\anime

# Provider
providers:
  default:
    - allanime
```

### Update player_path

Read the config, find the `player_path` line after the comment block (not the example lines), and update it using the Edit tool. Be careful: there may be multiple occurrences of `player_path` in comments — only change the actual config value.

## Updating Dependencies

### Update anipy-cli
```bash
uv tool upgrade anipy-cli
```

### Update mpv (via scoop)
```bash
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 update mpv"
```

### Update scoop itself
```bash
pwsh.exe -NoProfile -Command "& $env:USERPROFILE\scoop\shims\scoop.ps1 update"
```
