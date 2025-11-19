"""
Setup Boilerplate

Utility to assist in setting up a new Python CLI Tools Boilerplate project.
"""
# MARK: Imports
import shutil
from pathlib import Path

# MARK: Constants
FILES_MODULE_DESC = [
    Path("BOILERPLATE_README.md").absolute(),
    Path("pyproject.toml").absolute()
]
FILES_PACKAGE_NAME_USER = [
    Path("BOILERPLATE_README.md").absolute(),
    Path("config.toml").absolute(),
    Path("clitoolsboilerplate/run.py").absolute()
]
FILES_PACKAGE_NAME_SYS = [
    Path("main.py").absolute(),
    Path("pyproject.toml").absolute(),
    Path("uv.lock").absolute()
]
FILES_DEV_ID = [
    Path("LICENSE.txt").absolute()
]
FILES_MODULE_DIR = Path("clitoolsboilerplate").absolute()

# MARK: Functions
def setup(
    packageNameRich: str,
    packageNameSys: str,
    moduleDesc: str,
    onlyVerify: bool = False
) -> None:
    """
    Set up the boilerplate project by guiding the user through necessary changes.

    packageNameRich: The user facing name of the package like `"My Cool Tool"`.
    packageNameSys: The system facing name of the package like `"mycooltool"`.
    moduleDesc: A brief, user facing description of the module's function.
    onlyVerify: If `True`, only verify that all boilerplate files are present then exit.
    """
    # TODO: The following:
    # * [x] Replace `[[MODULE_DESCRIPTION]]` with a description of your module's function.
    # * [x] Replace `[[PACKAGE_NAME_USER_FACING]]` in all files with the *user facing* name of your project.
    # * [x] Replace `[[DEVELOPER_IDENTIFIER]]` with your name or other developer identifier for licensing purposes.
    # * [x] Replace `clitoolsboilerplate` in `pyproject.toml` with the *system facing* name of the project.
    # * [x] Rename the `clitoolsboilerplate/` directory to the *system facing* name of the project.
    # * [ ] Remove the `README.md`.
    # * [ ] Rename the `BOILERPLATE_README.md` to `README.md`.
    # * [ ] Print the user should edit the `pyproject.toml` as needed.
    # * [ ] Print the user should remove the `setupBoilerplate.py` file.

    # Check all the inputs
    _checkString(packageNameRich)
    _checkString(packageNameSys)
    _checkString(moduleDesc)

    # Verify all files exist
    allFiles = (FILES_MODULE_DESC + FILES_PACKAGE_NAME_USER + FILES_PACKAGE_NAME_SYS + FILES_DEV_ID + [
        FILES_MODULE_DIR
    ])
    _checkFiles(allFiles)

    # Report
    print(f"All {len(allFiles)} boilerplate files to edit are present.")
    if onlyVerify:
        print("Verification complete. Exiting.")
        return

    # Replace module description
    for filePath in FILES_MODULE_DESC:
        _replaceInFile(filePath, "[[MODULE_DESCRIPTION]]", moduleDesc)

    # Report
    print("Module description replaced.")

    # Replace the user facing package name
    for filePath in FILES_PACKAGE_NAME_USER:
        _replaceInFile(filePath, "[[PACKAGE_NAME_USER_FACING]]", packageNameRich)

    # Replace the system facing package name
    for filePath in FILES_PACKAGE_NAME_SYS:
        _replaceInFile(filePath, "clitoolsboilerplate", packageNameSys)

    # Report
    print("Package names replaced.")

    # Rename the package directory
    newModuleDir = FILES_MODULE_DIR.parent / packageNameSys
    shutil.move(FILES_MODULE_DIR, newModuleDir)

    # Report
    print(f"Module directory renamed to: {newModuleDir.relative_to(Path.cwd())}")

    # TODO: The rest

def _checkFiles(filePaths: list[Path]):
    """
    Check that all files in `filePaths` exist.
    """
    missingFiles: list[Path] = []
    for filePath in filePaths:
        if not filePath.exists():
            missingFiles.append(filePath)

    if missingFiles:
        error = "\nBoilerplate files are missing:\n"
        for missingFile in missingFiles:
            error += f"\t* {missingFile}\n"
        raise FileNotFoundError(error)

def _checkString(s: str):
    """
    Check that the string `s` is not empty or whitespace only.
    """
    if not s or s.isspace():
        raise ValueError(f"Provided string '{s}' is empty or whitespace only.")

def _replaceInFile(filePath: Path, toReplace: str, replaceWith: str) -> None:
    """
    Replace all occurrences of `toReplace` with `replaceWith` in the file at `filePath`.
    """
    # Read file
    with open(filePath, "r", encoding="utf-8") as file:
        content = file.read()

    # Replace content
    content = content.replace(toReplace, replaceWith)

    # Write file
    with open(filePath, "w", encoding="utf-8") as file:
        file.write(content)

# MARK: Execution
if __name__ == "__main__":
    # CLI Imports
    import argparse

    # Setup setup CLI
    parser = argparse.ArgumentParser(
        description="Setup the Python CLI Tools Boilerplate project."
    )

    # Required arguments
    parser.add_argument(
        "packageNameRich",
        type=str,
        help="The user facing name of the package like 'My Cool Tool'."
    )
    parser.add_argument(
        "packageNameSys",
        type=str,
        help="The system facing name of the package like 'mycooltool'."
    )
    parser.add_argument(
        "moduleDesc",
        type=str,
        help="A description of the module's function."
    )

    # Optional arguments
    parser.add_argument(
        "-v", "--verify",
        action="store_true",
        help="Verify that all boilerplate files are present and then exit. No further steps will be performed."
    )

    # Parse arguments
    args = parser.parse_args()

    # Run setup
    setup(
        packageNameRich=args.packageNameRich,
        packageNameSys=args.packageNameSys,
        moduleDesc=args.moduleDesc,
        onlyVerify=args.verify
    )
