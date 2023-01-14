import argparse
import csv
import glob
import json
import os
import statistics
import subprocess
import tarfile
from datetime import date, datetime
from zipfile import ZipFile
from sys import platform as operatingsystem_codename
import atexit
import requests
import matplotlib.pyplot as plt
import psutil
from pathlib import Path
import hashlib
import result_to_db
from typing import Any

outheader = [
    "name",
    "timestamp",
    "wholeUpdate",
    "latencyUpdate",
    "gameUpdate",
    "circuitNetworkUpdate",
    "transportLinesUpdate",
    "fluidsUpdate",
    "heatManagerUpdate",
    "entityUpdate",
    "particleUpdate",
    "mapGenerator",
    "mapGeneratorBasicTilesSupportCompute",
    "mapGeneratorBasicTilesSupportApply",
    "mapGeneratorCorrectedTilesPrepare",
    "mapGeneratorCorrectedTilesCompute",
    "mapGeneratorCorrectedTilesApply",
    "mapGeneratorVariations",
    "mapGeneratorEntitiesPrepare",
    "mapGeneratorEntitiesCompute",
    "mapGeneratorEntitiesApply",
    "crcComputation",
    "electricNetworkUpdate",
    "logisticManagerUpdate",
    "constructionManagerUpdate",
    "pathFinder",
    "trains",
    "trainPathFinder",
    "commander",
    "chartRefresh",
    "luaGarbageIncremental",
    "chartUpdate",
    "scriptUpdate",
    "path",
    "md5",
    "info",
]


def exit_handler() -> None:
    print("Terminating grasfully!")
    sync_mods("", True)
    # I should also clean up potential other files
    # such as the lock file (factorio/.lock on linux)
    # also factorio.zip and maps.zip can be left over in rare cases and fail the reinstall.


def get_factorio_version(factorio_bin: str, full: bool = False) -> str:
    """returns the version string of the installed factorio instance"""
    factorio_log_version = os.popen(f"{factorio_bin} --version").read()
    result = factorio_log_version.splitlines()[0].split()[1]
    if full:
        result += " " + factorio_log_version.splitlines()[0].split()[4][:-1]
        result += " " + factorio_log_version.splitlines()[0].split()[5][:-1]
    return result


def sync_mods(map: str, disable_all: bool = False) -> None:
    fmm_name = {"linux": "fmm_linux", "win32": "fmm_win32.exe", "cygwin": "fmm_win32.exe"}[
        operatingsystem_codename
    ]
    if not disable_all:
        set_mod_command = os.path.join("fmm", fmm_name) + f' --game-dir factorio sf "{map}"'
    else:
        set_mod_command = os.path.join("fmm", fmm_name) + " --game-dir factorio disable"
    # print(">>>> sync_mods()\t", set_mod_command)
    print(os.popen(set_mod_command).read())


def install_maps(link: str) -> None:
    """download maps from the walterpi server"""
    file = requests.get(link)
    with open("maps.zip", "xb") as mapsfile:
        mapsfile.write(file.content)
    with ZipFile("maps.zip", "r") as zip:
        zip.extractall("saves")
    os.remove("maps.zip")


def install_factorio(
    link: str = "https://factorio.com/get-download/stable/headless/linux64",
) -> None:
    """Download and extract the latest version of Factorio."""
    file = requests.get(link)
    with open("factorio.zip", "xb") as zipfile:
        zipfile.write(file.content)
    with tarfile.open("factorio.zip", "r:xz") as tar:
        tar.extractall("")
    os.remove("factorio.zip")


# for mypy
def remove_character_from_string(s: str, char: str = "\r") -> str:
    return s.replace(char, "")


def run_benchmark(
    map_: str,
    folder: str,
    ticks: int,
    runs: int,
    md5: str,
    save: bool = True,
    disable_mods: bool = True,
    factorio_bin: str | None = None,
    high_priority: bool | None = None,
    cpu: int | None = None,
) -> None:
    """Run a benchmark on the given map with the specified number of ticks and
    runs."""
    if factorio_bin is None:
        factorio_bin = os.path.join("factorio", "bin", "x64", "factorio")
    # setting mods
    if not disable_mods:
        sync_mods(map_)

    print("Running benchmark...")
    # Get Version
    version: str = get_factorio_version(factorio_bin, True)
    # psutil.Popen on Linux it doesn't work well with str()
    command: list[str] = [str(factorio_bin)]
    command.extend(["--benchmark", str(map_)])
    command.extend(["--benchmark-ticks", str(ticks)])
    command.extend(["--benchmark-runs", str(runs)])
    command.extend(["--benchmark-verbose", "all"])
    command.extend(["--benchmark-sanitize"])
    if high_priority is True:
        if cpu is None:
            cpu = 0
        priority = {
            "linux": -20,
            "win32": 128,  # psutil.HIGH_PRIORITY_CLASS AttributeError: module 'psutil' has no attribute 'HIGH_PRIORITY_CLASS'
            "cygwin": 128,  # psutil.HIGH_PRIORITY_CLASS AttributeError: module 'psutil' has no attribute 'HIGH_PRIORITY_CLASS'
        }[operatingsystem_codename]
        print("nice = ", priority)
        process = psutil.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.nice(priority)
        if cpu != 0:
            process.cpu_affinity(list(range(0, cpu)))
    else:
        process = psutil.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    factorio_log, err = map(
        lambda a: remove_character_from_string(a.decode("utf-8"), "\r"), process.communicate()
    )

    if "Performed" not in factorio_log:
        print("Benchmark failed")
        print(factorio_log)
        print(err)
    else:
        if save:
            # print(factorio_log)
            print(version)
            avgs = [
                float(line.split()[-2]) / ticks
                for line in factorio_log.split("\n")
                if "Performed" in line
            ]
            avg = statistics.mean(avgs)
            ups = 1000 / avg
            avgs_str: list[str] = [f"{i:.3f}" for i in avgs]
            print("Map benchmarked at:")
            print("avg = {:.3f} ms {}".format(avg, avgs_str))
            print("{:.3f} UPS".format(ups))
            print()
            # with open(os.path.join(folder, "saves", md5 + ".all"), "x") as f:
            #    print(factorio_log_version, file=f)
            out: dict[str, Any] = dict()
            out["version"] = version
            out["avg"] = avg
            out["ups"] = ups
            out["avgs"] = avgs_str
            out["cpu"] = cpu
            filtered_output = [str(json.dumps(out))]
            filtered_output.extend(
                [line for line in factorio_log.split("\n") if "ed" in line or "t" in line]
            )
            with open(os.path.join(folder, "saves", md5 + ".log"), "x") as f:
                f.write("\n".join(filtered_output))


def get_md5(fname: str) -> str:
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def get_list_of_files_with_md5(folder: str, md5_to_name: dict[str, str]) -> list[dict[str, str]]:
    files: list[dict[str, str]] = list()
    for file in glob.glob(os.path.join(folder, "saves", "*.log")):
        full_file_name = md5_to_name[os.path.basename(file).replace(".log", "")]
        file_name = os.path.basename(full_file_name).split(".")[0]
        files.append({"file_name": file_name, "file": file, "full_file_name": full_file_name})
    return files


def benchmark_folder(
    ticks: int,
    runs: int,
    disable_mods: bool,
    skipticks: int,
    map_regex: str = "*",
    factorio_bin: str | None = None,
    folder: str | None = None,
    filenames: list[str] | None = None,
    high_priority: bool | None = None,
    cpu: int | None = None,
) -> str:
    """Run benchmarks on all maps that match the given regular expression."""
    datetime_now = datetime.now()
    if folder is None:
        folder = f"benchmark_on_{date.today()}_{datetime_now.strftime('%H_%M_%S')}"
    os.makedirs(folder)
    os.makedirs(os.path.join(folder, "saves"))
    os.makedirs(os.path.join(folder, "graphs"))

    print("Warming up the system...")
    run_benchmark(
        os.path.join("saves", "factorio_maps", "big_bases", "flame10k.zip"),
        folder,
        ticks=100,
        runs=1,
        md5="",
        save=False,
        disable_mods=disable_mods,
        factorio_bin=factorio_bin,
        high_priority=high_priority,
        cpu=cpu,
    )
    print("Finished warming up, starting the actual benchmark...")

    print()
    print("==================")
    print("benchmark maps")
    print("==================")
    print()
    if filenames is None:
        filenames = glob.glob(os.path.join("saves", map_regex), recursive=True)

    # md5 calculation for files
    print("maps:")
    filenames = [f for f in filenames if os.path.isfile(f)]
    for filename in filenames:
        print(filename)
    print()
    md5_to_name = dict()
    name_to_md5 = dict()
    for filename in filenames:
        md5 = get_md5(filename)
        # print("{} - {}".format(md5, filename))
        if md5 not in md5_to_name:
            md5_to_name[md5] = filename
            name_to_md5[filename] = md5
        else:
            print(
                "'{}' - the file matches the file - '{}'\tthe benchmark will not be made".format(
                    filename, md5_to_name[md5]
                )
            )
    filenames = list(name_to_md5.keys())
    print()

    for filename in filenames:
        print(filename)
        run_benchmark(
            filename,
            folder,
            ticks=ticks,
            runs=runs,
            md5=name_to_md5[filename],
            save=True,
            disable_mods=disable_mods,
            factorio_bin=factorio_bin,
            high_priority=high_priority,
            cpu=cpu,
        )

    print("==================")
    outfile: list[list[Any]] = [outheader]
    # get file names from hash
    files = get_list_of_files_with_md5(folder, md5_to_name)

    # processing benchmark results
    for file in sorted(files, key=lambda f: f["file_name"]):
        with open(file["file"], "r") as f:
            for line in f.readlines():
                info = json.loads(line)
                break

        with open(file["file"], "r", newline="") as cfile:
            cfilestr = list(csv.reader(cfile, dialect="excel"))
            inlist: list[list[float]] = list()
            for i in cfilestr[0 : len(cfilestr)]:
                try:
                    if int(i[0][1:]) % ticks < skipticks:
                        # figure out how to actually skip these ticks.
                        continue
                    inlist.append([float(t / 1000000) for t in list(map(int, i[1:-1]))])
                except Exception:  # noqa: PIE786
                    pass
                    # print("can't convert to int")

            full_file_name = file["full_file_name"]
            file_name = file["file_name"]
            outrow: list[str | float] = [file_name]
            for rowi in range(32):
                outrow.append(statistics.mean([a[rowi] for a in inlist]))
            outrow.append(full_file_name)
            outrow.append(name_to_md5[full_file_name])
            outrow.append(info)

            outfile.append(outrow)

    print("saving out.json")
    outfile_1: dict[str, Any] = dict()
    dt = dict()
    dt["year"] = datetime_now.year
    dt["month"] = datetime_now.month
    dt["day"] = datetime_now.day
    dt["hour"] = datetime_now.hour
    dt["minute"] = datetime_now.minute
    dt["second"] = datetime_now.second
    dt["microsecond"] = datetime_now.microsecond
    outfile_1["datetime"] = dt
    outfile_1["ticks"] = ticks
    outfile_1["runs"] = runs
    outfile_1["disable_mods"] = disable_mods
    outfile_1["skipticks"] = skipticks
    outfile_1["map_regex"] = map_regex
    outfile_1["factorio_bin"] = factorio_bin
    outfile_1["folder"] = folder
    outfile_1["filenames"] = filenames
    # list -> dict
    outfile_1["benchmark_result"] = [
        dict(zip(outheader, data_for_map)) for data_for_map in outfile[1:]
    ]
    out_path = os.path.join(folder, "out.json")
    outfile_json = json.dumps(outfile_1, indent=4)
    with open(out_path, "w+") as outjson_file:
        outjson_file.write(outfile_json)

    print()
    print("the benchmark is finished")
    print("==================")

    return folder


def plot_benchmark_results(
    folder: str, out_folder: str | None = None, cols: tuple[str, ...] | None = None
) -> None:
    """Generate plots of benchmark results."""

    columns: tuple[str, ...] = (
        "wholeUpdate",
        "latencyUpdate",
        "gameUpdate",
        "circuitNetworkUpdate",
        "transportLinesUpdate",
        "fluidsUpdate",
        "heatManagerUpdate",
        "entityUpdate",
        "particleUpdate",
        "mapGenerator",
        "mapGeneratorBasicTilesSupportCompute",
        "mapGeneratorBasicTilesSupportApply",
        "mapGeneratorCorrectedTilesPrepare",
        "mapGeneratorCorrectedTilesCompute",
        "mapGeneratorCorrectedTilesApply",
        "mapGeneratorVariations",
        "mapGeneratorEntitiesPrepare",
        "mapGeneratorEntitiesCompute",
        "mapGeneratorEntitiesApply",
        "crcComputation",
        "electricNetworkUpdate",
        "logisticManagerUpdate",
        "constructionManagerUpdate",
        "pathFinder",
        "trains",
        "trainPathFinder",
        "commander",
        "chartRefresh",
        "luaGarbageIncremental",
        "chartUpdate",
        "scriptUpdate",
    )
    if cols is not None:
        if set(cols).issubset(columns):
            columns = cols
        else:
            print("Error")
            print("columns should be set from the list:")
            print(columns)
            print()
            return

    print("creating graphs")
    # read out.json
    with open(os.path.join(folder, "out.json"), "r") as f:
        benchmark_result = json.loads(f.read())["benchmark_result"]

    # Create the output subfolder if it does not exist
    if out_folder is None:
        out_folder = os.path.join(folder, "graphs")
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    maps = [a["name"] for a in benchmark_result]
    for col in columns:
        fig, ax = plt.subplots()
        update = [a[col] for a in benchmark_result]
        hbars = ax.barh(maps, update)
        ax.bar_label(
            hbars,
            labels=[f"{x:.3f}" for x in update],
            padding=3,
        )
        ax.margins(0.1, 0.05)
        ax.set_title(col)
        ax.set_xlabel("Mean frametime [ms/frame]")
        ax.set_ylabel("Map name")
        plt.tight_layout()
        # Use os.path.join to build the file path for the output image
        out_path = os.path.join(out_folder, f"{col}.png")
        plt.savefig(out_path)
        plt.clf()
        plt.close()


def create_mods_dir() -> None:
    os.makedirs(os.path.join("factorio", "mods"), exist_ok=True)
    mod_list_json_file = os.path.join("factorio", "mods", "mod-list.json")
    if not os.path.exists(mod_list_json_file):
        with open(mod_list_json_file, "x") as file:
            file.write('{"mods":[{"name":"base","enabled":true}]}')
    mod_settings_dat_file = os.path.join("factorio", "mods", "mod-settings.dat")
    if not os.path.exists(mod_settings_dat_file):
        # copy the file 'mod-settings.dat'
        source = Path(os.path.join("fmm", "mod-settings.dat"))
        destination = Path(mod_settings_dat_file)
        destination.write_bytes(source.read_bytes())


def init_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Benchmark Factorio maps. " 'The default configuration is `-r "**" -s 20 -t 1000 -e 5'
        )
    )
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Update Factorio to the latest version before running benchmarks.",
    )
    parser.add_argument(
        "-r",
        "--regex",
        default="**",
        help=str(
            "Regular expression to match map names to benchmark. "
            "The regex either needs to be escaped by quotes or every special "
            "character needs to be escaped. use ** if you want to match "
            "everything. * can only be used if a specific folder is specified.",
        ),
    )
    parser.add_argument(
        "-s",
        "--skipticks",
        type=int,
        default="20",
        help=str(
            "the amount of ticks that are ignored at the beginning of very "
            "benchmark. helps to get more consistent data, especially for "
            "consistency plots. change this to '0' if you want to use all the "
            "data",
        ),
    )
    parser.add_argument(
        "-t",
        "--ticks",
        type=int,
        default="1000",
        help="the default amount of ticks to run for. defaults to 1000",
    )
    parser.add_argument(
        "-e",
        "--repetitions",
        type=int,
        default="5",
        help=str(
            "the number of times each map is repeated. default five. should be "
            "higher if `--consistency` is set.",
        ),
    )
    parser.add_argument(
        "--version_link",
        type=str,
        help=str(
            "if you want to install a specific version of factorio. you have to "
            "provide the complete download link to the headless version. don't "
            "forget to update afterwards.",
        ),
    )
    parser.add_argument(
        "-m",
        "--install_maps",
        type=str,
        nargs="?",
        const="https://walterpi.hopto.org/s/g6BLGR6wa27cNRf/download",
        help="install maps",
    )
    parser.add_argument(
        "-dm",
        "--disable_mods",
        action="store_true",
        help="disables the usage of mod syncronisations. runs all benchmarks without enabling any mods",
    )
    parser.add_argument(
        "-hp",
        "--high_priority",
        action="store_true",
        default=False,
        help="Increases the priority for the 'factorio' process. On Linux requires 'sudo'",
    )
    parser.add_argument(
        "-p",
        "--plot_results",
        action="store_true",
        default=False,
        help="Plot benchmark results.",
    )
    parser.add_argument(
        "-rtb",
        "--results_to_db",
        action="store_true",
        default=False,
        help=str("Save the benchmark result in the database. Database name 'benchmark_result.db3'"),
    )
    return parser


######################################
#
# main
if __name__ == "__main__":
    atexit.register(exit_handler)
    args = init_parser().parse_args()

    if args.update:
        if args.version_link:
            install_factorio(args.version_link)
        else:
            install_factorio()

    if args.install_maps:
        install_maps(args.install_maps)

    create_mods_dir()
    if args.disable_mods:
        sync_mods(map="", disable_all=True)

    # saves = list()
    # saves.append(r"D:\Games\Factorio\saves\flame_Sla_10k.zip")
    # saves.append(r"saves\flame10k.zip")
    # saves.append(r"saves\factorio_maps\big_bases\flame10k.zip")
    # saves.append(r"saves\factorio_maps\big_bases\steve10krail(2x5k).zip")
    folder = benchmark_folder(
        ticks=args.ticks,
        runs=args.repetitions,
        disable_mods=args.disable_mods,
        skipticks=args.skipticks,
        map_regex=args.regex,
        factorio_bin=None,
        folder=None,
        filenames=None,
        high_priority=args.high_priority,
        cpu=None,
    )

    if args.plot_results:
        plot_benchmark_results(folder)

    if args.results_to_db:
        result_to_db.result_to_db(folder)
