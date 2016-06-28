# WSL bash.exe patcher
Patch WSL's bash.exe to execute arbitrary Linux executables from the WSL filesystem

# Usage
Supply the tool with the path to the original bash.exe (`C:\Windows\System32\bash.exe` by default) and give it the absolute path to a Linux ELF executable (e.g. `/bin/zsh`). You may optionally specify a name for the generated wrapper binary (e.g. `--output zsh.exe`).

The tool will then replace the call to `/bin/bash` with your custom binary and write a new exe file to the location you specified (default is `launcher.exe`) which you can run from Windows.

Full, working example:
```
$ wsl-bashexe-patcher.py /mnt/c/Windows/System32/bash.exe /bin/zsh --output zsh.exe
```

# Limitations
* The path to the Linux executable may not exceed 16 characters
* The script may or may not work with future versions of Windows 10 and bash.exe
* If you execute this script from within a windows command prompt you may not be able to open the default `bash.exe` (not sure why, maybe Windows File Protection has something to do with this). Just copy bash.exe from its default location (`C:\Windows\System32\bash.exe`) to somewhere else and use that path instead
