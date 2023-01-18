This repository should serve the testing of different factorio optimisations problems.
The goal is, to be able to test different maps quickly and be able to compare the results over time.

# Install

1. Install Python 3.10
2. Install packages:
   * Windows: `python.exe -m pip install -r requirements.txt`
   * Linux: read the documentation for your Linux distribution. The list of required packages is in the file requirements.txt
3. `Linux`: 
just run `benchmarker.py -u -m` to install the latest version of factorio and download some sample maps. This will also directly run the programm a first time. 
it needs python3. therefore depending on your distro you might have to do `python3 benchmarker.py -u -m` or `python benchmarker.py -u -m`.
4. `Windows`:
   * with WSL2:
You are using Linux therefore just use the linux install: `python benchmarker.py -u -m`
   * without WSL2:
As there is no headless version available for windows, one has to install factorio by hand. to do this download the correct version from the website and unpack it into the main folder. so that `factorio/bin/x64/factorio` is the correct file. It would also be possible to add a link to a existing install into that possition but that isn't recommended due to mods.
After that run `python benchmarker.py -m` to download some sample maps and run it a first time.
5. `OSX`:
Same as Windows without WSL. You need to install factorio manually. As with windows `factorio/bin/x64/factorio` needs to be pointing to factorio. If the factorio install uses a different path, for example if you are on a ARM based mac, you might need to create a symlink to there.
After that run `python benchmarker.py -m` to download some sample maps and run it a first time.
if you have suggestions on how to improve the OSX situation please reach out.
6. Mod support. Mod support is provided by `fmm`, a tool built bui Raiguard. it should in theory be possible to configure it via a config file. but I can't figure out how. Therefore it currently just has the default configuration. This requires the `factorio/player-data.json` to contain the username and token string(`service-username` `service-token` in the file). These lines are required to be able to download mods from the factorio server. The are added to the `player-data.json` if you load the game and log in. 
   * For `windows` user: just start the factorio instance and log in. after that mod support works. 
   * For `linux` user: as you can't log into the headless version, it's easiest to just coply the `player-data,json` from a working install.
   * For `OSX` and other(BSD etc): As I haven't yet cross compiled fmm you have to do so yourself, and then put it in the fmm folder and then do the same as windows user. 
7. `(Windows)` building benchmark_GUI.exe
   * Install the PyInstaller package `python.exe -m pip install pyinstaller`
   * `pyinstaller --onefile --noupx benchmark_GUI.py`

## Usage

When running it for the first time, or when updating factorio use the -u mode to get the latest stable version `(Linux only)`.

If you only want to run part of the testsuite you can use the -r \<regex> option to only match certain files.

### Running benchmarks
(to-do)

### Options for the console script `benchmarker.py`:
```
  -h, --help            show this help message and exit
  -u, --update          Update Factorio to the latest version before running benchmarks (Linux only).
  -r REGEX, --regex REGEX
                        Regular expression to match map names to benchmark. The regex either needs to be escaped by quotes or every special character needs to be escaped. use ** if you want to match everything.
                        * can only be used if a specific folder is specified.
  -s SKIPTICKS, --skipticks SKIPTICKS
                        the amount of ticks that are ignored at the beginning of very benchmark. helps to get more consistent data, especially for consistency plots. change this to '0' if you want to use all
                        the data
  -t TICKS, --ticks TICKS
                        the default amount of ticks to run for. defaults to 1000
  -e REPETITIONS, --repetitions REPETITIONS
                        the number of times each map is repeated. default five. should be higher if `--consistency` is set.
  --version_link VERSION_LINK
                        if you want to install a specific version of factorio. you have to provide the complete download link to the headless version. don't forget to update afterwards (Linux only).
  -m [INSTALL_MAPS], --install_maps [INSTALL_MAPS]
                        install maps
  -dm, --disable_mods   disables the usage of mod syncronisations. runs all benchmarks without enabling any mods
  -hp, --high_priority  Increases the priority for the 'factorio' process. On Linux requires 'sudo'
  -p, --plot_results    Plot benchmark results.
  -rtb, --results_to_db
                        Save the benchmark result in the database. Database name 'benchmark_result.db3'
```

## Todo
