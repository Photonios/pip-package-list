import enum


class PackageListFileType(enum.Enum):
    REQUIREMENTS_TXT = "requirements.txt"
    SETUP_PY = "setup.py"


def identify_package_list_file_type(file_path: str) -> PackageListFileType:
    if file_path.endswith("setup.py"):
        return PackageListFileType.SETUP_PY

    return PackageListFileType.REQUIREMENTS_TXT
