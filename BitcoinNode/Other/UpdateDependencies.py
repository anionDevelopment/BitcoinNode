import re
from pathlib import Path
import requests
from packaging.version import Version
from ScriptCollection.ScriptCollectionCore import ScriptCollectionCore
from ScriptCollection.TFCPS.TFCPS_Tools_General import TFCPS_Tools_General

# This must be the same host which CommonTasks.py downloads the releases from.
_AddressOfTheDownloads: str = "https://bitcoincore.org/bin"

_TimeoutInSeconds: int = 30


def get_latest_bitcoin_version() -> str:
    headers = {'Cache-Control': 'no-cache'}
    response = requests.get(_AddressOfTheDownloads, timeout=_TimeoutInSeconds, headers=headers)
    response.raise_for_status()
    link_regex = r"<a href=\"bitcoin\-core\-\d+\.\d+(\.\d+)?\/\">bitcoin\-core\-(\d+\.\d+(\.\d+)?)\/<\/a>"
    versions: list[str] = [linkmatch[1] for linkmatch in re.compile(link_regex).findall(response.text)]
    versions.sort(key=Version, reverse=True)
    for version in versions:
        if is_released(version):
            return version
    raise ValueError(f"No released Bitcoin-version was found on {_AddressOfTheDownloads}.")


def is_released(version: str) -> bool:
    """The folder of a version is created on the download-server before the version is released (it then only contains
    release-candidates). A version is released when its checksum-file is available."""
    response = requests.head(f"{_AddressOfTheDownloads}/bitcoin-core-{version}/SHA256SUMS", timeout=_TimeoutInSeconds)
    return response.status_code == 200


def update_dependencies():
    script_file = str(Path(__file__).absolute())
    sc = ScriptCollectionCore()
    TFCPS_Tools_General(sc).update_dependency_in_resources_folder(script_file, "Bitcoin", get_latest_bitcoin_version())


if __name__ == "__main__":
    update_dependencies()
