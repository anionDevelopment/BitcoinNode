import hashlib
import os
from pathlib import Path
import requests
from ScriptCollection.GeneralUtilities import GeneralUtilities
from ScriptCollection.TFCPS.Docker.TFCPS_CodeUnitSpecific_Docker import TFCPS_CodeUnitSpecific_Docker_Functions,TFCPS_CodeUnitSpecific_Docker_CLI

# bitcoincore.org is the host where the Bitcoin Core project publishes its releases including the checksum-files.
# bitcoin.org does not provide all releases (for example not the files of v28.1), so it is not used.
_AddressOfTheDownloads: str = "https://bitcoincore.org/bin"

_NameOfTheResourceFolder: str = "Bitcoin"

# Maps the architecture-name which docker uses for the build-argument "TARGETARCH" to the architecture-name which
# Bitcoin Core uses in the names of its release-files. The dockerfile selects the archive by the docker-name.
_Architectures: dict[str, str] = {
    "amd64": "x86_64",
    "arm64": "aarch64",
}

_TimeoutInSeconds: int = 120


def download_bitcoin(tf: TFCPS_CodeUnitSpecific_Docker_Functions) -> None:
    codeunit_folder: str = tf.get_codeunit_folder()
    version: str = tf.tfcps_Tools_General.get_dependency_version_in_resources_folder(os.path.join(codeunit_folder, "Other", "Resources"), _NameOfTheResourceFolder)
    resource_folder: str = os.path.join(codeunit_folder, "Other", "Resources", _NameOfTheResourceFolder)
    GeneralUtilities.ensure_directory_does_not_exist(resource_folder)
    GeneralUtilities.ensure_directory_exists(resource_folder)
    checksums: dict[str, str] = get_checksums(version)
    for docker_architecture, bitcoin_architecture in _Architectures.items():
        file_name: str = f"bitcoin-{version}-{bitcoin_architecture}-linux-gnu.tar.gz"
        GeneralUtilities.write_message_to_stdout(f"Download {file_name}...")
        target_file: str = os.path.join(resource_folder, f"Bitcoin_{docker_architecture}.tar.gz")
        download_file(f"{_AddressOfTheDownloads}/bitcoin-core-{version}/{file_name}", target_file)
        GeneralUtilities.assert_condition(file_name in checksums, f"The checksum-file of Bitcoin v{version} does not contain an entry for \"{file_name}\".")
        verify_checksum(target_file, checksums[file_name])


def get_checksums(version: str) -> dict[str, str]:
    """Returns the sha256-checksums of the release-files of the given version, indexed by the file-name."""
    response = requests.get(f"{_AddressOfTheDownloads}/bitcoin-core-{version}/SHA256SUMS", timeout=_TimeoutInSeconds)
    response.raise_for_status()
    result: dict[str, str] = {}
    for line in response.text.splitlines():
        if GeneralUtilities.string_has_content(line):
            checksum, file_name = line.split(maxsplit=1)
            result[file_name.strip()] = checksum.strip().lower()
    return result


def download_file(url: str, target_file: str) -> None:
    """Loads a file in chunks, so that the memory-usage does not depend on the size of the release."""
    with requests.get(url, stream=True, timeout=_TimeoutInSeconds) as response:
        response.raise_for_status()
        with open(target_file, "wb") as target:
            for chunk in response.iter_content(chunk_size=1024*1024):
                target.write(chunk)


def verify_checksum(file: str, expected_sha256: str) -> None:
    """Ensures that the downloaded file is the one the release describes. Without this check a truncated or an exchanged
    download would end up in the image and would only be noticed when the node does not start."""
    actual_sha256 = hashlib.sha256(Path(file).read_bytes()).hexdigest()
    GeneralUtilities.assert_condition(actual_sha256 == expected_sha256, f"The checksum of \"{file}\" is \"{actual_sha256}\" but \"{expected_sha256}\" was expected.")


def common_tasks():
    tf:TFCPS_CodeUnitSpecific_Docker_Functions=TFCPS_CodeUnitSpecific_Docker_CLI.parse(__file__)
    download_bitcoin(tf)
    tf.do_common_tasks(tf.get_version_of_project())#codeunit-version should always be the same as project-version
    bitcoin_version=tf.tfcps_Tools_General.get_dependency_version_in_resources_folder(os.path.join(tf.get_codeunit_folder(),"Other","Resources"),_NameOfTheResourceFolder)
    GeneralUtilities.replace_regex_each_line_of_file(os.path.join(tf.get_codeunit_folder(),"ReadMe.md"),"The currently used Bitcoin\\-version is .*\\.", f"The currently used Bitcoin-version is {bitcoin_version}.")


if __name__ == "__main__":
    common_tasks()
