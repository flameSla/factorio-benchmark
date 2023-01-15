#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Fri Jan 13 15:00:55 2023
#

import wx
import sqlite3
from datetime import datetime
import json
import os
import glob
import shutil
from contextlib import redirect_stdout, redirect_stderr
import benchmarker
import result_to_db

# begin wxGlade: dependencies
import wx.adv

# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    def OnClose(self, event):
        print("__del__")
        self.save_settings()
        self.Destroy()

    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((1200, 800))
        self.SetTitle("benchmark GUI")

        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Exit", "")
        self.Bind(wx.EVT_MENU, self.menu_EXIT, item)
        self.frame_menubar.Append(wxglade_tmp_menu, "File")
        wxglade_tmp_menu = wx.Menu()
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "About", "")
        self.Bind(wx.EVT_MENU, self.menu_ABOUT, item)
        self.frame_menubar.Append(wxglade_tmp_menu, "Help")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end

        self.Panel1 = wx.Notebook(self, wx.ID_ANY)

        self.Tests = wx.Panel(self.Panel1, wx.ID_ANY)
        self.Panel1.AddPage(self.Tests, "Tests")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_1 = wx.Panel(self.Tests, wx.ID_ANY)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)

        sizer_10 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_10, 1, wx.EXPAND, 0)

        label_7 = wx.StaticText(self.panel_1, wx.ID_ANY, "Factorio_bin")
        label_7.SetMinSize((75, 16))
        sizer_10.Add(label_7, 0, 0, 0)

        self.text_factorio_bin = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        self.text_factorio_bin.SetMinSize((400, -1))
        sizer_10.Add(self.text_factorio_bin, 0, 0, 0)

        self.button_set_the_path = wx.Button(self.panel_1, wx.ID_ANY, "Set the path")
        sizer_10.Add(self.button_set_the_path, 0, 0, 0)

        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_3, 1, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "Runs")
        label_1.SetMinSize((40, 16))
        sizer_3.Add(label_1, 0, 0, 0)

        self.spin_runs = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "3", min=0, max=999999)
        self.spin_runs.SetMinSize((60, 23))
        sizer_3.Add(self.spin_runs, 0, 0, 0)

        self.checkbox_disable_mods = wx.CheckBox(
            self.panel_1, wx.ID_ANY, "Disable mods", style=wx.ALIGN_RIGHT
        )
        self.checkbox_disable_mods.SetMinSize((100, -1))
        self.checkbox_disable_mods.SetValue(1)
        sizer_3.Add(self.checkbox_disable_mods, 0, 0, 0)

        self.checkbox_delete_temp_folder = wx.CheckBox(
            self.panel_1, wx.ID_ANY, "Delete Temp folder", style=wx.ALIGN_RIGHT
        )
        self.checkbox_delete_temp_folder.SetMinSize((120, -1))
        self.checkbox_delete_temp_folder.SetValue(1)
        sizer_3.Add(self.checkbox_delete_temp_folder, 0, 0, 0)

        sizer_3.Add((20, 20), 10, wx.EXPAND, 0)

        self.button_start_test = wx.Button(self.panel_1, wx.ID_ANY, "Start Test")
        sizer_3.Add(self.button_start_test, 0, wx.ALL, 0)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "Ticks")
        label_2.SetMinSize((40, 16))
        sizer_4.Add(label_2, 0, 0, 0)

        self.spin_ticks = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "100", min=0, max=999999)
        self.spin_ticks.SetMinSize((60, 23))
        sizer_4.Add(self.spin_ticks, 0, 0, 0)

        self.checkbox_high_priority = wx.CheckBox(
            self.panel_1, wx.ID_ANY, "High priority", style=wx.ALIGN_RIGHT
        )
        self.checkbox_high_priority.SetMinSize((100, -1))
        self.checkbox_high_priority.SetValue(1)
        sizer_4.Add(self.checkbox_high_priority, 0, 0, 0)

        sizer_4.Add((20, 20), 0, 0, 0)

        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_8, 1, wx.EXPAND, 0)

        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, "Cpus")
        label_5.SetMinSize((40, 16))
        sizer_8.Add(label_5, 0, 0, 0)

        self.text_ctrl_cpus = wx.TextCtrl(self.panel_1, wx.ID_ANY, "0")
        sizer_8.Add(self.text_ctrl_cpus, 3, wx.EXPAND, 0)

        sizer_8.Add((0, 0), 0, 0, 0)

        sizer_9 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_9, 1, wx.EXPAND, 0)

        label_6 = wx.StaticText(self.panel_1, wx.ID_ANY, "Skipticks")
        sizer_9.Add(label_6, 0, 0, 0)

        self.spin_skipticks = wx.SpinCtrl(self.panel_1, wx.ID_ANY, "20", min=0, max=999999)
        self.spin_skipticks.SetMinSize((60, 23))
        sizer_9.Add(self.spin_skipticks, 0, 0, 0)

        self.panel_2 = wx.Panel(self.Tests, wx.ID_ANY)
        self.panel_2.SetBackgroundColour(wx.Colour(192, 192, 192))
        sizer_1.Add(self.panel_2, 20, wx.EXPAND, 0)

        sizer_6 = wx.BoxSizer(wx.VERTICAL)

        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(sizer_7, 1, wx.EXPAND, 0)

        self.text_regex = wx.TextCtrl(self.panel_2, wx.ID_ANY, "**")
        sizer_7.Add(self.text_regex, 1, 0, 0)

        self.button_regex = wx.Button(self.panel_2, wx.ID_ANY, "Regex")
        sizer_7.Add(self.button_regex, 0, 0, 0)

        self.button_add_map = wx.Button(self.panel_2, wx.ID_ANY, "Add map")
        sizer_7.Add(self.button_add_map, 0, 0, 0)

        self.button_reset_maps = wx.Button(self.panel_2, wx.ID_ANY, "Reset maps")
        sizer_7.Add(self.button_reset_maps, 0, 0, 0)

        label_4 = wx.StaticText(self.panel_2, wx.ID_ANY, "Maps:")
        sizer_6.Add(label_4, 0, 0, 0)

        self.text_ctrl_maps = wx.TextCtrl(self.panel_2, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_6.Add(self.text_ctrl_maps, 10, wx.EXPAND, 0)

        self.panel_3 = wx.Panel(self.Tests, wx.ID_ANY)
        sizer_1.Add(self.panel_3, 20, wx.EXPAND, 0)

        sizer_5 = wx.BoxSizer(wx.VERTICAL)

        label_3 = wx.StaticText(self.panel_3, wx.ID_ANY, "Description")
        sizer_5.Add(label_3, 0, 0, 0)

        self.text_Description = wx.TextCtrl(
            self.panel_3, wx.ID_ANY, "", style=wx.TE_LEFT | wx.TE_MULTILINE
        )
        sizer_5.Add(self.text_Description, 15, wx.EXPAND, 0)

        self.text_ctrl_command_line = wx.TextCtrl(
            self.panel_3, wx.ID_ANY, "benchmarker.py", style=wx.TE_READONLY
        )
        sizer_5.Add(self.text_ctrl_command_line, 0, 0, 0)

        self.Results = wx.Panel(self.Panel1, wx.ID_ANY)
        self.Panel1.AddPage(self.Results, "Results")

        sizer_11 = wx.BoxSizer(wx.VERTICAL)

        self.panel_4 = wx.Panel(self.Results, wx.ID_ANY)
        sizer_11.Add(self.panel_4, 1, wx.EXPAND, 0)

        sizer_12 = wx.BoxSizer(wx.VERTICAL)

        self.button_tests_update = wx.Button(self.panel_4, wx.ID_ANY, "Update tests")
        sizer_12.Add(self.button_tests_update, 0, 0, 0)

        self.list_ctrl_tests = wx.ListCtrl(
            self.panel_4, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES
        )
        sizer_12.Add(self.list_ctrl_tests, 1, wx.EXPAND, 0)

        self.panel_5 = wx.Panel(self.Results, wx.ID_ANY)
        sizer_11.Add(self.panel_5, 1, wx.EXPAND, 0)

        sizer_13 = wx.BoxSizer(wx.VERTICAL)

        self.button_update_benchmark_results = wx.Button(
            self.panel_5, wx.ID_ANY, "Update benchmark results"
        )
        sizer_13.Add(self.button_update_benchmark_results, 0, 0, 0)

        self.list_ctrl_benchmark_results = wx.ListCtrl(
            self.panel_5, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES
        )
        # self.list_ctrl_benchmark_results.AppendColumn("A", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_13.Add(self.list_ctrl_benchmark_results, 10, wx.EXPAND, 0)

        self.panel_5.SetSizer(sizer_13)

        self.panel_4.SetSizer(sizer_12)

        self.Results.SetSizer(sizer_11)

        self.panel_3.SetSizer(sizer_5)

        self.panel_2.SetSizer(sizer_6)

        self.panel_1.SetSizer(sizer_2)

        self.Tests.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.button_set_the_path_OnButton, self.button_set_the_path)
        self.Bind(wx.EVT_BUTTON, self.button_start_test_OnButton, self.button_start_test)
        self.Bind(wx.EVT_BUTTON, self.button_regex_OnButton, self.button_regex)
        self.Bind(wx.EVT_BUTTON, self.button_add_map_OnButton, self.button_add_map)
        self.Bind(wx.EVT_BUTTON, self.button_reset_maps_OnButton, self.button_reset_maps)
        self.Bind(wx.EVT_BUTTON, self.button_tests_update_OnButton, self.button_tests_update)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_tests_SELECTED, self.list_ctrl_tests)
        self.Bind(
            wx.EVT_BUTTON,
            self.button_update_benchmark_results_OnButton,
            self.button_update_benchmark_results,
        )
        self.Bind(
            wx.EVT_LIST_ITEM_SELECTED,
            self.list_ctrl_benchmark_results_SELECTED,
            self.list_ctrl_benchmark_results,
        )
        # end wxGlade
        self.Bind(
            wx.EVT_LIST_COL_CLICK,
            self.list_ctrl_benchmark_results_COL_CLICK,
            self.list_ctrl_benchmark_results,
        )
        self.Bind(
            wx.EVT_LIST_COL_CLICK,
            self.list_ctrl_tests_COL_CLICK,
            self.list_ctrl_tests,
        )
        self.Bind(
            wx.EVT_CLOSE,
            self.OnClose,
            self,
        )

        self.column_widths = set()
        self.name_of_the_settings_file = "benchmark_GUI_settings.json"
        self.query_for_tests_results = "select * from tests"
        self.query_for_benchmark_results = "select * from view_benchmark_result"
        self.add_mapFileDialog_defaultDir = ""
        self.set_the_pathFileDialog_defaultDir = ""

        self.restore_settings()
        self.update_benchmark_results("", "")
        self.update_tests_results("", "")

    def restore_settings(self):
        if os.path.exists(self.name_of_the_settings_file):
            with open(self.name_of_the_settings_file, "r") as f:
                settings = json.loads(f.read())
                cols = ""
                for col in settings["list_ctrl_tests"]:
                    if settings["list_ctrl_tests"][col]:
                        cols += col + ","
                self.query_for_tests_results = "select {} from tests".format(cols[:-1])
                cols = ""
                for col in settings["list_ctrl_benchmark_results"]:
                    if settings["list_ctrl_benchmark_results"][col]:
                        cols += col + ","
                self.query_for_benchmark_results = "select {} from view_benchmark_result".format(
                    cols[:-1]
                )

                self.text_regex.Clear()
                self.text_regex.AppendText(settings["text_regex"])
                self.text_factorio_bin.Clear()
                self.text_factorio_bin.AppendText(settings["text_factorio_bin"])
                self.text_ctrl_cpus.Clear()
                self.text_ctrl_cpus.AppendText(settings["text_ctrl_cpus"])
                self.spin_runs.SetValue(int(settings["spin_runs"]))
                self.spin_ticks.SetValue(int(settings["spin_ticks"]))
                self.spin_skipticks.SetValue(int(settings["spin_skipticks"]))
                self.checkbox_disable_mods.SetValue(settings["checkbox_disable_mods"])
                self.checkbox_delete_temp_folder.SetValue(settings["checkbox_delete_temp_folder"])
                self.checkbox_high_priority.SetValue(settings["checkbox_high_priority"])
                self.add_mapFileDialog_defaultDir = settings["add_mapFileDialog_defaultDir"]
                self.set_the_pathFileDialog_defaultDir = settings["set_the_pathFileDialog_defaultDir"]

    def get_list_settings(self, list):
        result = dict()
        for col in range(list.GetColumnCount())[1:]:
            result[list.GetColumn(col).GetText()] = True
        return result

    def save_settings(self):
        settings = dict()
        settings["list_ctrl_tests"] = self.get_list_settings(self.list_ctrl_tests)
        settings["list_ctrl_benchmark_results"] = self.get_list_settings(
            self.list_ctrl_benchmark_results
        )

        settings["text_regex"] = self.text_regex.GetLineText(0)
        settings["text_factorio_bin"] = self.text_factorio_bin.GetLineText(0)
        settings["spin_runs"] = self.spin_runs.GetTextValue()
        settings["checkbox_disable_mods"] = self.checkbox_disable_mods.GetValue()
        settings["checkbox_delete_temp_folder"] = self.checkbox_delete_temp_folder.GetValue()
        settings["spin_ticks"] = self.spin_ticks.GetTextValue()
        settings["spin_skipticks"] = self.spin_skipticks.GetTextValue()
        settings["checkbox_high_priority"] = self.checkbox_high_priority.GetValue()
        settings["text_ctrl_cpus"] = self.text_ctrl_cpus.GetLineText(0)

        settings["add_mapFileDialog_defaultDir"] = self.add_mapFileDialog_defaultDir
        settings["set_the_pathFileDialog_defaultDir"] = self.set_the_pathFileDialog_defaultDir

        with open(self.name_of_the_settings_file, "w") as f:
            f.write(json.dumps(settings, indent=4))

    def menu_EXIT(self, event):  # wxGlade: MainFrame.<event_handler>
        self.Close()
        event.Skip()

    def menu_ABOUT(self, event):  # wxGlade: MainFrame.<event_handler>
        AboutDialog = MyAboutDialog(self, wx.ID_ANY, "")
        AboutDialog.ShowModal()
        del AboutDialog
        event.Skip()

    def button_set_the_path_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        set_the_path_FileDialog = wx.FileDialog(
            self,
            "Add map",
            defaultDir=self.set_the_pathFileDialog_defaultDir,
            defaultFile="factorio",
            wildcard="",
            style=wx.FD_OPEN,
        )
        if set_the_path_FileDialog.ShowModal() == wx.ID_OK:
            map = set_the_path_FileDialog.GetPath()
            self.text_factorio_bin.Clear()
            self.text_factorio_bin.AppendText(map)
            self.set_the_pathFileDialog_defaultDir = os.path.dirname(map)
        event.Skip()

    def button_start_test_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_start_test_OnButton' not implemented!")

        map_regex = self.text_regex.GetLineText(0)
        map_regex = map_regex if map_regex else None

        factorio_bin = self.text_factorio_bin.GetLineText(0)
        factorio_bin = factorio_bin if factorio_bin else None

        runs = int(self.spin_runs.GetTextValue())
        ticks = int(self.spin_ticks.GetTextValue())
        skipticks = int(self.spin_skipticks.GetTextValue())

        disable_mods = self.checkbox_disable_mods.GetValue()
        high_priority = self.checkbox_high_priority.GetValue()



        
        event.Skip()
        return

        # cpus = self.text_ctrl_cpus.GetLineText(0)
        cpu = 0

        # maps
        # self.text_ctrl_maps.AppendText(map + "\n")
        filenames = None


        # deleting the Temp folder
        folder = "Temp"
        try:
            shutil.rmtree(folder)
        except OSError:
            pass
        
        with redirect_stdout(self.text_Description), redirect_stderr(self.text_Description):
            folder = benchmarker.benchmark_folder(
                ticks=ticks,
                runs=runs,
                disable_mods=disable_mods,
                skipticks=skipticks,
                map_regex=map_regex,
                factorio_bin=factorio_bin,
                folder=folder,
                filenames=filenames,
                high_priority=high_priority,
                cpu=cpu,
            )
            result_to_db.result_to_db(folder)

        # settings["checkbox_delete_temp_folder"] = self.checkbox_delete_temp_folder.GetValue()



        event.Skip()

    def button_regex_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        self.text_ctrl_maps.Clear()
        filenames = glob.glob(os.path.join("saves", self.text_regex.GetLineText(0)), recursive=True)
        filenames = [f for f in filenames if os.path.isfile(f)]
        for name in filenames:
            self.text_ctrl_maps.AppendText(name + "\n")
        event.Skip()

    def button_add_map_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        add_mapFileDialog = wx.FileDialog(
            self,
            "Add map",
            defaultDir=self.add_mapFileDialog_defaultDir,
            defaultFile="",
            wildcard="Maps|*.zip",
            style=wx.FD_OPEN | wx.FD_MULTIPLE,
        )
        if add_mapFileDialog.ShowModal() == wx.ID_OK:
            maps = add_mapFileDialog.GetPaths()
            for map in maps:
                self.text_ctrl_maps.AppendText(map + "\n")
                self.add_mapFileDialog_defaultDir = os.path.dirname(map)
        event.Skip()

    def button_reset_maps_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        self.text_ctrl_maps.Clear()
        event.Skip()

    def update_tests_results(self, column_on_which_we_are_sorting, where):
        with sqlite3.connect("benchmark_result.db3") as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            query = self.query_for_tests_results
            if where:
                query += where
            if column_on_which_we_are_sorting:
                query += f" order by {column_on_which_we_are_sorting}"
            else:
                query += " order by id"
            cur.execute(query)
            self.set_data_to_list(self.list_ctrl_tests, cur)
            db.commit()

    def button_tests_update_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        self.update_tests_results("", "")
        event.Skip()

    def list_ctrl_tests_COL_CLICK(self, event):
        col = event.GetColumn()
        self.update_tests_results(self.list_ctrl_tests.GetColumn(col).GetText(), "")
        event.Skip()

    def list_ctrl_tests_SELECTED(self, event):  # wxGlade: MainFrame.<event_handler>
        list = self.list_ctrl_tests
        row = int(event.GetItem().GetText()) - 1
        cols = list.GetColumnCount()
        if row >= 0:
            for col in range(cols):
                text = list.GetItemText(row, col)
                if text[0] == "[":
                    where = " where id in ({})".format(text[1:-1])
                    self.update_benchmark_results("", where)
                    break
        event.Skip()

    def list_get_text_for_column(self, col_index, col):
        if col_index == 2:
            d = datetime.fromtimestamp(col)
            return d.isoformat(" ", "seconds")
        match col:
            case float() as col:
                return "{:.3f}".format(col)
            case str() as col:
                if col[:5] == "JSON:":
                    # description
                    return " ".join(line for line in json.loads(col[5:]))
                else:
                    return col
            case _:
                return str(col)

    def set_data_to_list(self, list, cur):
        list.DeleteAllItems()
        for n, row in enumerate(cur, start=0):
            if list not in self.column_widths:
                # we add columns only when the function is called for the first time
                if n == 0:
                    list.AppendColumn("", format=wx.LIST_FORMAT_LEFT, width=-1)
                    for col in row.keys():
                        list.AppendColumn(col, format=wx.LIST_FORMAT_LEFT, width=-1)

            item = wx.ListItem()
            item.SetId(n)
            item.SetText(str(n + 1))
            list.InsertItem(item)
            for col_index, col in enumerate(row, start=1):
                list.SetItem(
                    n,
                    col_index,
                    self.list_get_text_for_column(col_index, col),
                )

        if list not in self.column_widths:
            # the width of the columns is set only when the function is called for the first time
            for col in range(list.GetColumnCount()):
                list.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER)
                wh = list.GetColumnWidth(col)
                list.SetColumnWidth(col, wx.LIST_AUTOSIZE)
                wc = list.GetColumnWidth(col)
                if wh > wc:
                    list.SetColumnWidth(col, wx.LIST_AUTOSIZE_USEHEADER)
                self.column_widths.add(list)

    def update_benchmark_results(self, column_on_which_we_are_sorting, where):
        with sqlite3.connect("benchmark_result.db3") as db:
            db.row_factory = sqlite3.Row
            cur = db.cursor()
            query = self.query_for_benchmark_results
            if where:
                query += where
            if column_on_which_we_are_sorting:
                query += f" order by {column_on_which_we_are_sorting}"
            else:
                query += " order by id"
            cur.execute(query)
            self.set_data_to_list(self.list_ctrl_benchmark_results, cur)
            db.commit()

    def button_update_benchmark_results_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        self.update_benchmark_results("", "")
        event.Skip()

    def list_ctrl_benchmark_results_COL_CLICK(self, event):
        col = event.GetColumn()
        self.update_benchmark_results(self.list_ctrl_benchmark_results.GetColumn(col).GetText(), "")
        event.Skip()

    def list_ctrl_benchmark_results_SELECTED(self, event):  # wxGlade: MainFrame.<event_handler>
        list = self.list_ctrl_benchmark_results
        row = int(event.GetItem().GetText()) - 1
        cols = list.GetColumnCount()
        if row >= 0:
            path = ""
            md5 = ""
            for col in range(cols):
                if list.GetColumn(col).GetText() == "path":
                    path = list.GetItemText(row, col)
                if list.GetColumn(col).GetText() == "md5":
                    md5 = list.GetItemText(row, col)
            if path and md5:
                with sqlite3.connect("benchmark_result.db3") as db:
                    db.row_factory = sqlite3.Row
                    cur = db.cursor()
                    query = "select id_tests from view_test where path='{}' and md5='{}'".format(
                        path, md5
                    )
                    cur.execute(query)
                    ids = ""
                    for row in cur:
                        for i in row:
                            ids += str(i) + ","
                    db.commit()
                    self.update_tests_results("", " where id in ({})".format(ids[:-1]))

        event.Skip()


# end of class MainFrame


class MyAboutDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyAboutDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("About")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        sizer_1.Add(self.panel_1, 1, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)

        self.hyperlink_1 = wx.adv.HyperlinkCtrl(
            self.panel_1,
            wx.ID_ANY,
            "source code (GitHub)",
            "https://github.com/flameSla/factorio-benchmark/tree/benchmark_GUI",
        )
        sizer_3.Add(self.hyperlink_1, 0, 0, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, "2023 (c) flameSla")
        sizer_3.Add(label_1, 0, 0, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        sizer_2.AddButton(self.button_CANCEL)

        sizer_2.Realize()

        self.panel_1.SetSizer(sizer_3)

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetAffirmativeId(self.button_OK.GetId())
        self.SetEscapeId(self.button_CANCEL.GetId())

        self.Layout()
        self.Centre()
        # end wxGlade


# end of class MyAboutDialog


class BenchmarkGUI(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


# end of class BenchmarkGUI

if __name__ == "__main__":
    benchmark_GUI = BenchmarkGUI(0)
    benchmark_GUI.MainLoop()
