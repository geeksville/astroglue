import os
from pathlib import Path
from platformdirs import PlatformDirs

app_name = "starbash"
app_author = "geeksville"
dirs = PlatformDirs(app_name, app_author)
config_dir = Path(dirs.user_config_dir)
data_dir = Path(dirs.user_data_dir)

# These can be overridden for testing
_override_config_dir: Path | None = None
_override_data_dir: Path | None = None


def set_test_directories(
    config_dir_override: Path | None = None, data_dir_override: Path | None = None
) -> None:
    """Set override directories for testing. Used by test fixtures to isolate test data."""
    global _override_config_dir, _override_data_dir
    _override_config_dir = config_dir_override
    _override_data_dir = data_dir_override


def get_user_config_dir() -> Path:
    """Get the user config directory. Returns test override if set, otherwise the real user directory."""
    dir_to_use = (
        _override_config_dir if _override_config_dir is not None else config_dir
    )
    os.makedirs(dir_to_use, exist_ok=True)
    return dir_to_use


def get_user_data_dir() -> Path:
    """Get the user data directory. Returns test override if set, otherwise the real user directory."""
    dir_to_use = _override_data_dir if _override_data_dir is not None else data_dir
    os.makedirs(dir_to_use, exist_ok=True)
    return dir_to_use
