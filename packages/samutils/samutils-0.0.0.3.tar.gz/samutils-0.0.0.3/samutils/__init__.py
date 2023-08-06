import os

project_root_dir = os.path.dirname(os.path.abspath(__file__))


class Common:
    class Export:
        class Dir:
            export_csv_base_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}" \
                                   f"export{os.sep}dir{os.sep}export.csv"
            export_excel_base_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}" \
                                     f"export{os.sep}dir{os.sep}export.xlsx"
            export_dir_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}export{os.sep}dir"

        class Excel:
            export_excel_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}export" \
                                f"{os.sep}excel{os.sep}export.xlsx"
            export_excel_dir_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}export" \
                                    f"{os.sep}excel"

        class Csv:
            export_csv_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}export" \
                              f"{os.sep}csv{os.sep}export.csv"
            export_csv_dir_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}export" \
                                  f"{os.sep}csv"

    class Import:
        class Dir:
            import_dir_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}import" \
                              f"{os.sep}dir"

        class Excel:
            import_excel_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}import" \
                                f"{os.sep}excel{os.sep}import.xlsx"
            import_excel_dir_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}import" \
                                    f"{os.sep}excel"

        class Csv:
            import_csv_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}import" \
                              f"{os.sep}csv{os.sep}import.csv"
            import_csv_dir_path = f"{project_root_dir}{os.sep}data{os.sep}common{os.sep}import" \
                                  f"{os.sep}csv"


#################
###  文件目录  ###
#################
import_csv_path = Common.Import.Csv.import_csv_path
import_csv_dir_path = Common.Import.Csv.import_csv_dir_path
import_excel_path = Common.Import.Excel.import_excel_path
import_excel_dir_path = Common.Import.Excel.import_excel_dir_path
import_dir_path = Common.Import.Dir.import_dir_path

export_csv_path = Common.Export.Csv.export_csv_path
export_csv_dir_path = Common.Export.Csv.export_csv_dir_path
export_excel_path = Common.Export.Excel.export_excel_path
export_excel_dir_path = Common.Export.Excel.export_excel_dir_path
export_dir_path = Common.Export.Dir.export_dir_path
export_csv_base_path = Common.Export.Dir.export_csv_base_path
export_excel_base_path = Common.Export.Dir.export_excel_base_path

#################
###  日志目录 ###
#################

default_log_file_path = f"{project_root_dir}{os.sep}data{os.sep}log{os.sep}default{os.sep}default.log"
default_dir_file_path = f"{project_root_dir}{os.sep}data{os.sep}log{os.sep}default"

# 自动创建对应的文件夹
dir_path_list = [
    import_csv_dir_path
    , import_excel_dir_path
    , import_dir_path
    , export_csv_dir_path
    , export_excel_dir_path
    , export_dir_path
    , default_dir_file_path
]

for dir_path in dir_path_list:
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
