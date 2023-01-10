import argparse
import csv
import glob
import os
import statistics
import tarfile
from datetime import date, datetime
from zipfile import ZipFile
from sys import platform as operatingsystem_codename
import atexit
import requests
import matplotlib.pyplot as plt
import psutil
import subprocess
from pathlib import Path
import json
import hashlib


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
]


def column(table, index):
    """Return the column of the table with the given index."""
    col = []
    for row in table:
        try:
            col.append(row[index])
        except Exception:  # noqa: PIE786
            continue
    return col


def exit_handler():
    print("Terminating grasfully!")
    sync_mods("", True)
    # I should also clean up potential other files
    # such as the lock file (factorio/.lock on linux)
    # also factorio.zip and maps.zip can be left over in rare cases and fail the reinstall.


def sync_mods(map: str, disable_all: bool = False):
    fmm_name = {"linux": "fmm_linux", "win32": "fmm_win32.exe", "cygwin": "fmm_win32.exe"}[
        operatingsystem_codename
    ]
    if not disable_all:
        set_mod_command = os.path.join("fmm", fmm_name) + f' --game-dir factorio sf "{map}"'
    else:
        set_mod_command = os.path.join("fmm", fmm_name) + " --game-dir factorio disable"
    # print(">>>> sync_mods()\t", set_mod_command)
    print(os.popen(set_mod_command).read())


def install_maps(link):
    """download maps from the walterpi server"""
    file = requests.get(link)
    with open("maps.zip", "xb") as mapsfile:
        mapsfile.write(file.content)
    with ZipFile("maps.zip", "r") as zip:
        zip.extractall("saves")
    os.remove("maps.zip")


def install_factorio(
    link="https://factorio.com/get-download/stable/headless/linux64",
):
    """Download and extract the latest version of Factorio."""
    file = requests.get(link)
    with open("factorio.zip", "xb") as zipfile:
        zipfile.write(file.content)
    with tarfile.open("factorio.zip", "r:xz") as tar:
        tar.extractall("")
    os.remove("factorio.zip")


def run_benchmark(
    map_,
    folder,
    ticks,
    runs,
    md5,
    save=True,
    disable_mods=True,
    factorio_bin=None,
    high_priority=None,
):
    """Run a benchmark on the given map with the specified number of ticks and
    runs."""
    if factorio_bin is None:
        factorio_bin = os.path.join("factorio", "bin", "x64", "factorio")
    # setting mods
    if not disable_mods:
        sync_mods(map_)

    print("Running benchmark...")
    os.dup(1)
    command = (
        f"{factorio_bin} "
        f'--benchmark "{map_}" '
        f"--benchmark-ticks {ticks} "
        f"--benchmark-runs {runs} "
        "--benchmark-verbose all "
        "--benchmark-sanitize"
    )
    # print(command)

    if high_priority is True:
        priority = {
            "linux": -20,
            "win32": psutil.HIGH_PRIORITY_CLASS,
            "cygwin": psutil.HIGH_PRIORITY_CLASS,
        }[operatingsystem_codename]
        process = psutil.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.nice(priority)
        factorio_log, err = map(
            lambda a: a.decode("utf-8").replace("\r", ""), process.communicate()
        )
    else:
        factorio_log = os.popen(command).read()
        err = ""

    if "Performed" not in factorio_log:
        print("Benchmark failed")
        print(factorio_log)
        print(err)
    else:
        # print(factorio_log)
        ups = int(
            1000
            * ticks
            / float(
                [line.split()[-2] for line in factorio_log.split("\n") if "Performed" in line][0]
            )
        )
        print(f"Map benchmarked at {ups} UPS")
        print()
        if save:
            filtered_output = [
                line for line in factorio_log.split("\n") if "ed" in line or "t" in line
            ]
            with open(os.path.join(folder, "saves", md5 + ".log"), "x") as f:
                f.write("\n".join(filtered_output))


def get_md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def benchmark_folder(
    ticks,
    runs,
    disable_mods,
    skipticks,
    consistency,
    map_regex="*",
    factorio_bin=None,
    folder=None,
    filenames=None,
    high_priority=None,
):
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
    )
    print("Finished warming up, starting the actual benchmark...")

    print()
    print("==================")
    print("benchmark maps")
    print("==================\r\n")
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
        )

    print("==================")
    old_subfolder_name = ""
    # print(
    #     sorted(
    #         glob.glob(
    #             os.path.join(
    #                 folder,
    #                 "saves",
    #                 map_regex,
    #             ),
    #             recursive=True,
    #         )
    #     )
    # )
    outfile = [outheader]
    errfile = [outheader]
    # get file names from hash
    files = list()
    for file in glob.glob(os.path.join(folder, "saves", "*.log")):
        full_file_name = md5_to_name[os.path.basename(file).replace(".log", "")]
        file_name = os.path.basename(full_file_name).split(".")[0]
        files.append({"file_name": file_name, "file": file, "full_file_name": full_file_name})

    # processing benchmark results
    for file in sorted(files, key=lambda f: f["file_name"]):
        with open(file["file"], "r", newline="") as cfile:
            cfilestr = list(csv.reader(cfile, dialect="excel"))
            inlist = []
            errinlist = []
            for i in cfilestr[0 : len(cfilestr)]:
                try:
                    if int(i[0][1:]) % ticks < skipticks:
                        # figure out how to actually skip these ticks.
                        continue
                    inlist.append([t / 1000000 for t in list(map(int, i[1:-1]))])
                    if i[0] != "t0":
                        errinlist.append(list(map(int, i[1:-1])))
                except Exception:  # noqa: PIE786
                    pass
                    # print("can't convert to int")

            full_file_name = file["full_file_name"]
            file_name = file["file_name"]
            outrow = [file_name]
            outrowerr = [file_name + "_stdev"]
            for rowi in range(32):
                outrow.append(statistics.mean(column(inlist, rowi)))
                outrowerr.append(statistics.stdev(column(errinlist, rowi)))
            outrow.append(full_file_name)
            outrowerr.append(full_file_name)
            outrow.append(name_to_md5[full_file_name])
            outrowerr.append(name_to_md5[full_file_name])

            outfile.append(outrow)
            errfile.append(outrowerr)

            if consistency is not None:
                # do the consistency plot
                plot_ups_consistency(
                    folder=folder,
                    subfolder=old_subfolder_name,
                    data=column(inlist, consistency_index - 1),
                    ticks=ticks,
                    skipticks=skipticks,
                    name="consistency_" + file_name + "_" + consistency,
                )

    print("saving out.json")
    outfile_1 = dict()
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

    print("saving stdev.csv")
    errout_path = os.path.join(folder, "stdev.csv")
    with open(errout_path, "w+", newline="") as erroutfile:
        erroutfile.write(str(errfile))

    print("\r\nthe benchmark is finished")
    print("==================")

    return folder


def plot_ups_consistency(folder, subfolder, data, ticks, skipticks, name="default"):
    subfolder_path = os.path.join(folder, "graphs", subfolder)

    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    darray = []
    med = []
    maxi = []
    mini = []

    t = list(range(skipticks, ticks))
    for i in range(int(len(data) / (ticks - skipticks))):
        darray.append(data[(ticks - skipticks) * i : (ticks - skipticks) * (i + 1)])
    for i in range(len(darray[0])):
        # first discard the highest value as that can frequently be an outlier.
        c = sorted(column(darray, i))[:-1]
        med.append(statistics.median(c))
        maxi.append(max(c))
        mini.append(min(c))

    for i in range(int(len(data) / (ticks - skipticks))):
        plt.plot(
            t,
            data[(ticks - skipticks) * i : (ticks - skipticks) * (i + 1)],
            "k",
            alpha=0.2,
            linewidth=0.6,
        )
    plt.plot(t, med, "r", label="median", linewidth=0.6)
    plt.title(label=name)
    plt.xlabel(xlabel="tick")
    plt.ylabel(ylabel="tick time [ms]")
    plt.legend()
    plt.tight_layout()
    # Use os.path.join to build the file path for the output image
    out_path = os.path.join(subfolder_path, f"{name}_all.png")
    # plt.show()
    plt.savefig(out_path, dpi=800)
    plt.clf()
    plt.close()

    plt.plot(t, maxi, label="maximum", linewidth=0.3)
    plt.plot(t, mini, label="minimum", linewidth=0.3)
    plt.plot(t, med, "r", label="median", linewidth=0.6)
    plt.title(label=name)
    plt.xlabel(xlabel="tick")
    plt.ylabel(ylabel="tick time [ms]")
    plt.legend()
    plt.tight_layout()
    # Use os.path.join to build the file path for the output image
    out_path = os.path.join(subfolder_path, f"{name}_min_max_med.png")
    # plt.show()
    plt.savefig(out_path, dpi=800)
    plt.clf()
    plt.close()


def plot_benchmark_results(folder, out_folder=None, cols=None):
    """Generate plots of benchmark results."""

    columns = (
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


def create_mods_dir():
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


def init_parser():
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
        help=(
            "Regular expression to match map names to benchmark. "
            "The regex either needs to be escaped by quotes or every special "
            "character needs to be escaped. use ** if you want to match "
            "everything. * can only be used if a specific folder is specified.",
        ),
    )
    parser.add_argument(
        "-c",
        "--consistency",
        nargs="?",
        const="wholeUpdate",
        help=(
            "generates a update time consistency plot for the given metric. It "
            "has to be a metric accessible by --benchmark-verbose. the default "
            "value is 'wholeUpdate'. the first 10 ticks are skipped.(this can "
            "be set by setting '--skipticks'.",
        ),
    )
    parser.add_argument(
        "-s",
        "--skipticks",
        type=int,
        default="20",
        help=(
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
        help=(
            "the number of times each map is repeated. default five. should be "
            "higher if `--consistency` is set.",
        ),
    )
    parser.add_argument(
        "--version_link",
        type=str,
        help=(
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
        help="Increases the priority for the 'factorio' process.",
    )
    parser.add_argument(
        "-p",
        "--plot_results",
        action="store_true",
        default=False,
        help="Plot benchmark results.",
    )
    return parser


######################################
#
# main
if __name__ == "__main__":
    atexit.register(exit_handler)
    args = init_parser().parse_args()
    consistency_index: int = 0

    if args.consistency is not None:
        try:
            consistency_index = outheader.index(args.consistency)
        except ValueError as e:
            print("the chosen consistency variable doesn't exist:", e)
            exit(0)

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
        args.ticks,
        args.repetitions,
        args.disable_mods,
        args.skipticks,
        args.consistency,
        map_regex=args.regex,
        high_priority=args.high_priority,
        # filenames=saves,
    )

    if args.plot_results:
        plot_benchmark_results(folder)
