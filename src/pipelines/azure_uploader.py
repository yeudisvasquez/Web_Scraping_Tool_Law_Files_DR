import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv


def upload_to_adls():

    load_dotenv()

    download_root = os.getenv("path_download_dir")
    azcopy_path = os.getenv("AZCOPY_PATH")
    container_url = os.getenv("AZURE_CONTAINER_URL")

    if not download_root:
        raise ValueError("path_download_dir missing in .env")

    if not azcopy_path:
        raise ValueError("AZCOPY_PATH missing in .env")

    if not container_url:
        raise ValueError("AZURE_CONTAINER_URL missing in .env")

    source = Path(download_root)

    if not source.exists():
        raise FileNotFoundError(source)

    print("=" * 70)
    print("Uploading files to Azure Data Lake...")
    print("=" * 70)

    command = (
    f'"{azcopy_path}" '
    f'copy "{source}" "{container_url}" --recursive=true'
    )

    print("\nExecuting:")
    print(command)

    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
    
    print(result.stdout)   # AzCopy normal output
    print(result.stderr)   # AzCopy warnings/errors

    if result.returncode != 0:
        raise RuntimeError("AzCopy failed.")

    print("\nUpload completed successfully.")

    ## Delete local files after confirmation
    '''input(
        "\nIs all the data loaded to ADL?\n"
        "Press ENTER to permanently delete the local files..."
    )

    print("\nDeleting local files...\n")

    for item in source.iterdir():

        try:

            if item.is_file():
                item.unlink()

            elif item.is_dir():
                shutil.rmtree(item)

        except Exception as e:
            print(f"Unable to delete {item}: {e}")

    print("Local cleanup completed.")
    '''

if __name__ == "__main__":
    upload_to_adls()