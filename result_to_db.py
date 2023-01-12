import sqlite3
import os
import json
from datetime import datetime


def create_db(db_name):
    if os.path.exists(db_name):
        # print("db exists")
        return

    db = sqlite3.connect(db_name)
    cur = db.cursor()
    cur.executescript(
        """
    CREATE TABLE IF NOT EXISTS "maps" (
    "id" INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
    "path" TEXT  NULL,
    "md5" TEXT  NULL,
    UNIQUE("path", "md5")
    );

    CREATE TABLE IF NOT EXISTS "tests" (
    "id" INTEGER  NOT NULL PRIMARY KEY AUTOINCREMENT,
    "time" REAL NULL,
    "disable_mods" INTEGER NULL,
    "skipticks" INTEGER NULL,
    "map_regex" TEXT  NULL,
    "description" TEXT  NULL,
    "benchmark_result_id" TEXT  NULL
    );

    CREATE TABLE IF NOT EXISTS "benchmark_result" (
    "id" INTEGER  NOT NULL PRIMARY KEY,
    "time" REAL NULL,
    "map" INTEGER NOT NULL REFERENCES "maps" ("id"),
    "runs" INTEGER NULL,
    "ticks" INTEGER NULL,
    "avg" REAL NULL,
    "ups" REAL NULL,
    "version" TEXT NULL,
    "cpu" INTEGER NULL,
    "avgs" TEXT NULL,
    "timestamp" REAL NULL,
    "wholeUpdate" REAL NULL,
    "latencyUpdate" REAL NULL,
    "gameUpdate" REAL NULL,
    "circuitNetworkUpdate" REAL NULL,
    "transportLinesUpdate" REAL NULL,
    "fluidsUpdate" REAL NULL,
    "heatManagerUpdate" REAL NULL,
    "entityUpdate" REAL NULL,
    "particleUpdate" REAL NULL,
    "mapGenerator" REAL NULL,
    "mapGeneratorBasicTilesSupportCompute" REAL NULL,
    "mapGeneratorBasicTilesSupportApply" REAL NULL,
    "mapGeneratorCorrectedTilesPrepare" REAL NULL,
    "mapGeneratorCorrectedTilesCompute" REAL NULL,
    "mapGeneratorCorrectedTilesApply" REAL NULL,
    "mapGeneratorVariations" REAL NULL,
    "mapGeneratorEntitiesPrepare" REAL NULL,
    "mapGeneratorEntitiesCompute" REAL NULL,
    "mapGeneratorEntitiesApply" REAL NULL,
    "crcComputation" REAL NULL,
    "electricNetworkUpdate" REAL NULL,
    "logisticManagerUpdate" REAL NULL,
    "constructionManagerUpdate" REAL NULL,
    "pathFinder" REAL NULL,
    "trains" REAL NULL,
    "trainPathFinder" REAL NULL,
    "commander" REAL NULL,
    "chartRefresh" REAL NULL,
    "luaGarbageIncremental" REAL NULL,
    "chartUpdate" REAL NULL,
    "scriptUpdate" REAL NULL
    );

    """
    )
    db.commit()
    cur.close()


def get_map_id(db_name, path, md5):
    con = sqlite3.connect(db_name)
    while True:
        cur = con.cursor()
        res = cur.execute("SELECT id FROM maps WHERE path=? and md5=?", (path, md5))
        id = res.fetchall()
        con.commit()
        cur.close()
        if id:
            break
        else:
            cur = con.cursor()
            cur.execute("INSERT INTO maps(path, md5) VALUES (?, ?)", (path, md5))
            con.commit()
            cur.close()
    con.close()
    if len(id) > 1:
        raise Exception("len(id) > 1 -> " + str(type(id)) + "\t" + str(id))
    return id[0][0]


def get_time(d):
    return datetime(
        d["year"], d["month"], d["day"], d["hour"], d["minute"], d["second"], d["microsecond"]
    ).timestamp()


def bd_append_benchmark_result(db_name, data):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute("SELECT max(id) FROM benchmark_result")
    new_id = res.fetchall()
    con.commit()
    cur.close()
    if new_id[0][0] is None:
        new_id = 1
    else:
        new_id = new_id[0][0] + 1

    data.insert(0, new_id)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO benchmark_result VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        data,
    )
    con.commit()
    cur.close()
    con.close()

    return new_id


def description_list_to_str(d: list):
    return "JSON:" + str(json.dumps(d))


def description_str_to_list(s: str):
    if s[:5] == "JSON:":
        return json.loads(s[5:])
    else:
        return list()


def result_to_db(folder, db_name=None, description=None):
    if db_name is None:
        db_name = "benchmark_result.db3"

    # read out.json
    with open(os.path.join(folder, "out.json"), "r") as f:
        benchmark_result = json.loads(f.read())

    create_db(db_name)
    ids = list()
    for br in benchmark_result["benchmark_result"]:
        data = list()
        data.append(get_time(benchmark_result["datetime"]))
        data.append(get_map_id(db_name, br["path"], br["md5"]))
        data.append(benchmark_result["runs"])
        data.append(benchmark_result["ticks"])
        data.append(br["info"]["avg"])
        data.append(br["info"]["ups"])
        data.append(br["info"]["version"])
        data.append(br["info"]["cpu"])
        data.append(str(br["info"]["avgs"]))
        data.append(br["timestamp"])
        data.append(br["wholeUpdate"])
        data.append(br["latencyUpdate"])
        data.append(br["gameUpdate"])
        data.append(br["circuitNetworkUpdate"])
        data.append(br["transportLinesUpdate"])
        data.append(br["fluidsUpdate"])
        data.append(br["heatManagerUpdate"])
        data.append(br["entityUpdate"])
        data.append(br["particleUpdate"])
        data.append(br["mapGenerator"])
        data.append(br["mapGeneratorBasicTilesSupportCompute"])
        data.append(br["mapGeneratorBasicTilesSupportApply"])
        data.append(br["mapGeneratorCorrectedTilesPrepare"])
        data.append(br["mapGeneratorCorrectedTilesCompute"])
        data.append(br["mapGeneratorCorrectedTilesApply"])
        data.append(br["mapGeneratorVariations"])
        data.append(br["mapGeneratorEntitiesPrepare"])
        data.append(br["mapGeneratorEntitiesCompute"])
        data.append(br["mapGeneratorEntitiesApply"])
        data.append(br["crcComputation"])
        data.append(br["electricNetworkUpdate"])
        data.append(br["logisticManagerUpdate"])
        data.append(br["constructionManagerUpdate"])
        data.append(br["pathFinder"])
        data.append(br["trains"])
        data.append(br["trainPathFinder"])
        data.append(br["commander"])
        data.append(br["chartRefresh"])
        data.append(br["luaGarbageIncremental"])
        data.append(br["chartUpdate"])
        data.append(br["scriptUpdate"])
        ids.append(bd_append_benchmark_result(db_name, data))

    data = list()
    data.append(None)
    data.append(get_time(benchmark_result["datetime"]))
    data.append(benchmark_result["disable_mods"])
    data.append(benchmark_result["skipticks"])
    data.append(benchmark_result["map_regex"])
    if description is None:
        # entering a multiline comment
        print("Enter a description for the test. Ctrl-D or Ctrl-Z ( windows ) to save it.")
        description = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            description.append(line)
        description = description_list_to_str(description)
    data.append(description)
    data.append(str(ids))
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO tests VALUES (?,?,?,?,?,?,?)",
        data,
    )
    con.commit()
    cur.close()
    con.close()
