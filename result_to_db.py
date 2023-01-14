import sqlite3
import os
import json
from datetime import datetime
from typing import Any


def create_db(db_name: str) -> None:
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

    CREATE VIEW tests_ids AS
    SELECT	tests.id as id_tests, tests.disable_mods,
        tests.skipticks, tests.map_regex, tests.description, json_each.value as ids
    FROM tests, json_each(tests.benchmark_result_id);

    CREATE VIEW view_benchmark_result AS
    select benchmark_result.id as id,time,path,runs,
        ticks,avg,ups,version,cpu,avgs,timestamp,wholeUpdate,
        latencyUpdate,gameUpdate,circuitNetworkUpdate,transportLinesUpdate,fluidsUpdate,
        heatManagerUpdate,entityUpdate,particleUpdate,mapGenerator,mapGeneratorBasicTilesSupportCompute,
        mapGeneratorBasicTilesSupportApply,mapGeneratorCorrectedTilesPrepare,mapGeneratorCorrectedTilesCompute,
        mapGeneratorCorrectedTilesApply,mapGeneratorVariations,mapGeneratorEntitiesPrepare,
        mapGeneratorEntitiesCompute,mapGeneratorEntitiesApply,crcComputation,electricNetworkUpdate,
        logisticManagerUpdate,constructionManagerUpdate,pathFinder,trains,trainPathFinder,commander,
        chartRefresh,luaGarbageIncremental,chartUpdate,scriptUpdate,md5
    from benchmark_result
    join maps on map=maps.id;

    CREATE VIEW view_test AS
    select * from view_benchmark_result
    join tests_ids on view_benchmark_result.id=tests_ids.ids;

    """
    )
    db.commit()
    cur.close()


def get_map_id(db_name: str, path: str, md5: str) -> Any:
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


def get_time(d: dict[str, int]) -> float:
    return datetime(
        d["year"], d["month"], d["day"], d["hour"], d["minute"], d["second"], d["microsecond"]
    ).timestamp()


def bd_append_benchmark_result(db_name: str, data: list[Any]) -> int:
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute("SELECT max(id) FROM benchmark_result")
    row = res.fetchall()
    con.commit()
    cur.close()
    if row[0][0] is None:
        new_id = 1
    else:
        new_id = row[0][0] + 1

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


def description_list_to_str(d: list[str]) -> str:
    return "JSON:" + str(json.dumps(d))


def description_str_to_list(s: str) -> list[str]:
    if s[:5] == "JSON:":
        return list(json.loads(s[5:]))
    else:
        return list()


def result_to_db(folder: str, db_name: str | None = None, description: str | None = None) -> None:
    if db_name is None:
        db_name = "benchmark_result.db3"

    # read out.json
    with open(os.path.join(folder, "out.json"), "r") as f:
        benchmark_result = json.loads(f.read())

    create_db(db_name)
    ids = list()
    for br in benchmark_result["benchmark_result"]:
        data: list[Any] = list()
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
        new_description = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            new_description.append(line)
        description = description_list_to_str(new_description)
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
