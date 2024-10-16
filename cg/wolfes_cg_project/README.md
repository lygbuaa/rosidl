## prerequisites
1. install empy with  `pip install empy`
2. install build with `python3 -m pip install build`

## build whl package
1. Compile into *.pyc   `python3 -m compileall .`
2. Build wheel package  `python3 -m build --wheel`

## install whl package
1. You can install wheel to it's default location, which is usually annoying. 
   Also you can install wheel package to specific directory, 
   such as "~/tmp/python3" on Linux, or "C:\\Users\\tmp" on Windows
        `pip install --target <install-directory> ***.whl`
   Be careful with the specific directory, since it's not the default location, 
   before `import wolfes_cg` in a script, append the directory with 
        `sys.path.append("<install-directory>")`

## run wolfes_cg
1. The entry script lies in "<install-directory>/wolfes_cg/bin" on Linux, or "<install-directory>\\wolfes_cg\\bin" on Windows, 
   On Linux the Shebang Lines will do it's work,
        `<install-directory>/wolfes_cg/bin/run_wolfes_cg.sh --input-params`
   However, on Windows Shebang Lines won't work, so call the entry with python3,
        `python3 <install-directory>\\wolfes_cg\\bin\\run_wolfes_cg.bat --input-params`
2. For convenience, add the binary path into environment variable. On Linux shell
        `export PATH=$PATH:<install-directory>/wolfes_cg/bin`
   On Windows powershell,
        `$env:PATH+=";<install-directory>\wolfes_cg\bin"`
