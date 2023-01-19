#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# generated by wxGlade 1.0.4 on Thu Jan 19 22:42:52 2023
#

import wx

# begin wxGlade: dependencies
import wx.adv
import wx.grid
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
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
        self.text_factorio_bin.SetMinSize((200, -1))
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

        self.checkbox_disable_mods = wx.CheckBox(self.panel_1, wx.ID_ANY, "Disable mods", style=wx.ALIGN_RIGHT)
        self.checkbox_disable_mods.SetMinSize((100, -1))
        self.checkbox_disable_mods.SetValue(1)
        sizer_3.Add(self.checkbox_disable_mods, 0, 0, 0)

        self.checkbox_delete_temp_folder = wx.CheckBox(self.panel_1, wx.ID_ANY, "Delete Temp folder", style=wx.ALIGN_RIGHT)
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

        self.checkbox_high_priority = wx.CheckBox(self.panel_1, wx.ID_ANY, "High priority", style=wx.ALIGN_RIGHT)
        self.checkbox_high_priority.SetMinSize((100, -1))
        self.checkbox_high_priority.SetValue(1)
        sizer_4.Add(self.checkbox_high_priority, 0, 0, 0)

        self.checkbox_high_plot_results = wx.CheckBox(self.panel_1, wx.ID_ANY, "Plot results", style=wx.ALIGN_RIGHT)
        self.checkbox_high_plot_results.SetMinSize((100, -1))
        sizer_4.Add(self.checkbox_high_plot_results, 0, 0, 0)

        sizer_4.Add((20, 20), 0, 0, 0)

        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(sizer_8, 1, wx.EXPAND, 0)

        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, "Cpus")
        label_5.SetMinSize((40, 16))
        sizer_8.Add(label_5, 0, 0, 0)

        self.text_ctrl_5 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "0")
        sizer_8.Add(self.text_ctrl_5, 3, wx.EXPAND, 0)

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

        sizer_20 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(sizer_20, 0, wx.EXPAND, 0)

        label_4 = wx.StaticText(self.panel_2, wx.ID_ANY, "Maps:")
        sizer_20.Add(label_4, 0, 0, 0)

        sizer_20.Add((20, 20), 10, wx.EXPAND, 0)

        self.button_edit_file_list = wx.Button(self.panel_2, wx.ID_ANY, "Edit the file list")
        sizer_20.Add(self.button_edit_file_list, 0, 0, 0)

        self.button_add_10_lines = wx.Button(self.panel_2, wx.ID_ANY, "Add 10 lines")
        sizer_20.Add(self.button_add_10_lines, 0, 0, 0)

        self.grid_maps = wx.grid.Grid(self.panel_2, wx.ID_ANY, size=(1, 1))
        self.grid_maps.CreateGrid(10, 2)
        self.grid_maps.SetColLabelValue(0, "Path")
        self.grid_maps.SetColSize(0, 1000)
        self.grid_maps.SetColLabelValue(1, "On?")
        self.grid_maps.SetColSize(1, 60)
        sizer_6.Add(self.grid_maps, 10, wx.EXPAND, 0)

        self.panel_3 = wx.Panel(self.Tests, wx.ID_ANY)
        sizer_1.Add(self.panel_3, 20, wx.EXPAND, 0)

        sizer_14 = wx.BoxSizer(wx.HORIZONTAL)

        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_14.Add(sizer_5, 1, wx.EXPAND, 0)

        label_3 = wx.StaticText(self.panel_3, wx.ID_ANY, "Description")
        sizer_5.Add(label_3, 0, 0, 0)

        self.text_Description = wx.TextCtrl(self.panel_3, wx.ID_ANY, "<>", style=wx.TE_LEFT | wx.TE_MULTILINE)
        sizer_5.Add(self.text_Description, 15, wx.EXPAND, 0)

        sizer_21 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(sizer_21, 0, wx.EXPAND, 0)

        self.button_create_test_run_script = wx.Button(self.panel_3, wx.ID_ANY, "Create a test run script")
        sizer_21.Add(self.button_create_test_run_script, 0, 0, 0)

        self.button_load_script = wx.Button(self.panel_3, wx.ID_ANY, "Load the script")
        sizer_21.Add(self.button_load_script, 0, 0, 0)

        sizer_15 = wx.BoxSizer(wx.VERTICAL)
        sizer_14.Add(sizer_15, 2, wx.EXPAND, 0)

        label_8 = wx.StaticText(self.panel_3, wx.ID_ANY, "Out")
        sizer_15.Add(label_8, 0, 0, 0)

        self.text_out = wx.TextCtrl(self.panel_3, wx.ID_ANY, "<>", style=wx.TE_LEFT | wx.TE_MULTILINE)
        sizer_15.Add(self.text_out, 15, wx.EXPAND, 0)

        self.Results = wx.Panel(self.Panel1, wx.ID_ANY)
        self.Panel1.AddPage(self.Results, "Results")

        sizer_11 = wx.BoxSizer(wx.VERTICAL)

        self.panel_4 = wx.Panel(self.Results, wx.ID_ANY)
        sizer_11.Add(self.panel_4, 1, wx.EXPAND, 0)

        sizer_12 = wx.BoxSizer(wx.VERTICAL)

        sizer_22 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_12.Add(sizer_22, 1, wx.EXPAND, 0)

        self.button_tests_update = wx.Button(self.panel_4, wx.ID_ANY, "Update tests")
        sizer_22.Add(self.button_tests_update, 0, 0, 0)

        sizer_22.Add((20, 20), 10, 0, 0)

        self.button_save_report = wx.Button(self.panel_4, wx.ID_ANY, "Save report")
        sizer_22.Add(self.button_save_report, 0, 0, 0)

        self.list_ctrl_tests = wx.ListCtrl(self.panel_4, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.list_ctrl_tests.AppendColumn("A", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("B", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("C", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("D", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("E", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("F", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("G", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("H", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("I", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("J", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("K", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("L", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("M", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("N", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("O", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("P", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("Q", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("R", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("S", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("T", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("U", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("V", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("W", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("X", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("Y", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("Z", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AA", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AC", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AD", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AE", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AF", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AG", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_tests.AppendColumn("AH", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_12.Add(self.list_ctrl_tests, 10, wx.EXPAND, 0)

        self.panel_5 = wx.Panel(self.Results, wx.ID_ANY)
        sizer_11.Add(self.panel_5, 1, wx.EXPAND, 0)

        sizer_13 = wx.BoxSizer(wx.VERTICAL)

        self.button_update_benchmark_results = wx.Button(self.panel_5, wx.ID_ANY, "Update benchmark results")
        sizer_13.Add(self.button_update_benchmark_results, 0, 0, 0)

        self.list_ctrl_benchmark_results = wx.ListCtrl(self.panel_5, wx.ID_ANY, style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES)
        self.list_ctrl_benchmark_results.AppendColumn("A", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("B", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("C", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("D", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("E", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("F", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("G", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("H", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("I", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("J", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("K", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("L", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("M", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("N", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("O", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("P", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("Q", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("R", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("S", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("T", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("U", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("V", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("W", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("X", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("Y", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("Z", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AA", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AB", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AC", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AD", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AE", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AF", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AG", format=wx.LIST_FORMAT_LEFT, width=-1)
        self.list_ctrl_benchmark_results.AppendColumn("AH", format=wx.LIST_FORMAT_LEFT, width=-1)
        sizer_13.Add(self.list_ctrl_benchmark_results, 10, wx.EXPAND, 0)

        self.text_ctrl_selected_row = wx.TextCtrl(self.panel_5, wx.ID_ANY, "")
        sizer_13.Add(self.text_ctrl_selected_row, 0, wx.EXPAND, 0)

        self.sql_query = wx.Panel(self.Panel1, wx.ID_ANY)
        self.Panel1.AddPage(self.sql_query, "new tab")

        sizer_16 = wx.BoxSizer(wx.VERTICAL)

        sizer_17 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_16.Add(sizer_17, 1, wx.EXPAND, 0)

        self.text_ctrl_tables = wx.TextCtrl(self.sql_query, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer_17.Add(self.text_ctrl_tables, 1, wx.EXPAND, 0)

        self.text_ctrl_views = wx.TextCtrl(self.sql_query, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer_17.Add(self.text_ctrl_views, 1, wx.EXPAND, 0)

        sizer_18 = wx.BoxSizer(wx.VERTICAL)
        sizer_16.Add(sizer_18, 1, wx.EXPAND, 0)

        self.text_ctrl_sql = wx.TextCtrl(self.sql_query, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_18.Add(self.text_ctrl_sql, 10, wx.EXPAND, 0)

        self.button_execute_sql_query = wx.Button(self.sql_query, wx.ID_ANY, "execute sql query")
        sizer_18.Add(self.button_execute_sql_query, 0, 0, 0)

        sizer_19 = wx.BoxSizer(wx.VERTICAL)
        sizer_16.Add(sizer_19, 1, wx.EXPAND, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.sql_query, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        sizer_19.Add(self.text_ctrl_1, 10, wx.EXPAND, 0)

        self.sql_query.SetSizer(sizer_16)

        self.panel_5.SetSizer(sizer_13)

        self.panel_4.SetSizer(sizer_12)

        self.Results.SetSizer(sizer_11)

        self.panel_3.SetSizer(sizer_14)

        self.panel_2.SetSizer(sizer_6)

        self.panel_1.SetSizer(sizer_2)

        self.Tests.SetSizer(sizer_1)

        self.Layout()

        self.Bind(wx.EVT_BUTTON, self.button_set_the_path_OnButton, self.button_set_the_path)
        self.Bind(wx.EVT_BUTTON, self.button_start_test_OnButton, self.button_start_test)
        self.Bind(wx.EVT_BUTTON, self.button_regex_OnButton, self.button_regex)
        self.Bind(wx.EVT_BUTTON, self.button_add_map_OnButton, self.button_add_map)
        self.Bind(wx.EVT_BUTTON, self.button_reset_maps_OnButton, self.button_reset_maps)
        self.Bind(wx.EVT_BUTTON, self.button_edit_file_list, self.button_edit_file_list)
        self.Bind(wx.EVT_BUTTON, self.button_create_test_run_script_OnButton, self.button_create_test_run_script)
        self.Bind(wx.EVT_BUTTON, self.button_tests_update_OnButton, self.button_tests_update)
        self.Bind(wx.EVT_BUTTON, self.button_save_report_OnButton, self.button_save_report)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_tests_SELECTED, self.list_ctrl_tests)
        self.Bind(wx.EVT_BUTTON, self.button_update_benchmark_results_OnButton, self.button_update_benchmark_results)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_ctrl_benchmark_results_SELECTED, self.list_ctrl_benchmark_results)
        self.Bind(wx.EVT_BUTTON, self.button_execute_sql_query_OnButton, self.button_execute_sql_query)
        # end wxGlade

    def menu_EXIT(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'menu_EXIT' not implemented!")
        event.Skip()

    def menu_ABOUT(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'menu_ABOUT' not implemented!")
        event.Skip()

    def button_set_the_path_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_set_the_path_OnButton' not implemented!")
        event.Skip()

    def button_start_test_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_start_test_OnButton' not implemented!")
        event.Skip()

    def button_regex_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_regex_OnButton' not implemented!")
        event.Skip()

    def button_add_map_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_add_map_OnButton' not implemented!")
        event.Skip()

    def button_reset_maps_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_reset_maps_OnButton' not implemented!")
        event.Skip()

    def button_edit_file_list(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_edit_file_list' not implemented!")
        event.Skip()

    def button_create_test_run_script_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_create_test_run_script_OnButton' not implemented!")
        event.Skip()

    def button_tests_update_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_tests_update_OnButton' not implemented!")
        event.Skip()

    def button_save_report_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_save_report_OnButton' not implemented!")
        event.Skip()

    def list_ctrl_tests_SELECTED(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'list_ctrl_tests_SELECTED' not implemented!")
        event.Skip()

    def button_update_benchmark_results_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_update_benchmark_results_OnButton' not implemented!")
        event.Skip()

    def list_ctrl_benchmark_results_SELECTED(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'list_ctrl_benchmark_results_SELECTED' not implemented!")
        event.Skip()

    def button_execute_sql_query_OnButton(self, event):  # wxGlade: MainFrame.<event_handler>
        print("Event handler 'button_execute_sql_query_OnButton' not implemented!")
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

        self.hyperlink_1 = wx.adv.HyperlinkCtrl(self.panel_1, wx.ID_ANY, "source code (GitHub)", "https://github.com/flameSla/factorio-benchmark/tree/modified_version")
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

class MyChangeDescription(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyChangeDescription.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((400, 300))
        self.SetTitle("Change the description")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.panel_1 = wx.Panel(self, wx.ID_ANY)
        sizer_1.Add(self.panel_1, 15, wx.EXPAND, 0)

        sizer_3 = wx.StaticBoxSizer(wx.StaticBox(self.panel_1, wx.ID_ANY, "Description"), wx.VERTICAL)

        self.text_ctrl_description = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        sizer_3.Add(self.text_ctrl_description, 15, wx.EXPAND, 0)

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

        self.SetAffirmativeId(self.button_OK.GetId())
        self.SetEscapeId(self.button_CANCEL.GetId())

        self.Layout()
        # end wxGlade

# end of class MyChangeDescription

class MyEditingMaps(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyEditingMaps.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle("Editing maps")

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl_maps = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_MULTILINE)
        self.text_ctrl_maps.SetMinSize((1100, 500))
        sizer_1.Add(self.text_ctrl_maps, 0, 0, 0)

        sizer_2 = wx.StdDialogButtonSizer()
        sizer_1.Add(sizer_2, 0, wx.ALIGN_RIGHT | wx.ALL, 4)

        self.button_OK = wx.Button(self, wx.ID_OK, "")
        self.button_OK.SetDefault()
        sizer_2.AddButton(self.button_OK)

        self.button_CANCEL = wx.Button(self, wx.ID_CANCEL, "")
        sizer_2.AddButton(self.button_CANCEL)

        sizer_2.Realize()

        self.SetSizer(sizer_1)
        sizer_1.Fit(self)

        self.SetAffirmativeId(self.button_OK.GetId())
        self.SetEscapeId(self.button_CANCEL.GetId())

        self.Layout()
        # end wxGlade

# end of class MyEditingMaps

class BenchmarkGUI(wx.App):
    def OnInit(self):
        self.frame = MainFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class BenchmarkGUI

if __name__ == "__main__":
    benchmark_GUI_form = BenchmarkGUI(0)
    benchmark_GUI_form.MainLoop()
