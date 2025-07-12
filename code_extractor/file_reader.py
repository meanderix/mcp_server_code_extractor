"""Unified file reading with VCS support."""

from pathlib import Path
from typing import Optional, Union

from .vcs.factory import detect_vcs_provider


def get_file_content(file_path: Union[str, Path], revision: Optional[str] = None) -> str:
    """
    Get file content from filesystem or VCS revision.
    
    Args:
        file_path: Path to file (string or Path object)
        revision: Optional VCS revision (commit, branch, tag, etc.)
    
    Returns:
        File content as string
    """
    path_obj = Path(file_path) if isinstance(file_path, str) else file_path
    
    if revision is None:
        # Filesystem read (backward compatible)
        return path_obj.read_text(encoding='utf-8')
    
    # VCS read using detected provider
    vcs_provider = detect_vcs_provider(path_obj)
    if not vcs_provider:
        raise ValueError(f"No VCS found for {path_obj}")
    
    return vcs_provider.get_file_content(path_obj, revision)