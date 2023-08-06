import pandas as pd
from samutils.util.fileutil import get_file_path_list_by_dir_path, get_file_name_from_path, get_csv_export_file_path

from samutils import import_dir_path


class PdUtil(object):
    class Compare(object):
        def __init__(self, base_dir_path: str = import_dir_path):
            super().__init__()
            self.stats_result = {}
            self.file_path_list = get_file_path_list_by_dir_path(base_dir_path)
            if not self.file_path_list or len(self.file_path_list) != 2:
                raise RuntimeError(f"请检查该目录下文件个数, 暂时仅支持两个文件相互比较")

        def __del__(self):
            print(self.stats_result)

        @staticmethod
        def get_join_on_column_list(df: pd.DataFrame, join_list: tuple):
            columns = df.columns.values.tolist()
            new_columns = []
            for join in join_list:
                new_columns.append(columns[join])
            return new_columns

        def compare(self, left_join_list: tuple = (0,), right_join_list: tuple = (0,)):
            left_file_name = get_file_name_from_path(self.file_path_list[0])
            left_df = pd.read_csv(self.file_path_list[0])
            self.stats_result[left_file_name] = left_df.shape[0]

            right_file_name = get_file_name_from_path(self.file_path_list[1])
            right_df = pd.read_csv(self.file_path_list[1])
            self.stats_result[right_file_name] = right_df.shape[0]

            common_df = pd.merge(
                left=left_df
                , right=right_df
                , how="inner"
                , on=None
                , left_on=self.get_join_on_column_list(left_df, left_join_list)
                , right_on=self.get_join_on_column_list(right_df, right_join_list)
            )

            left_common_df = common_df.drop(columns=right_df.columns.values.tolist(), inplace=False)
            left_common_df.to_csv(get_csv_export_file_path(f"common_{left_file_name}"), index=False)
            self.stats_result[f"common_{left_file_name}"] = left_common_df.shape[0]

            right_common_df = common_df.drop(columns=left_df.columns.values.tolist(), inplace=False)
            right_common_df.to_csv(get_csv_export_file_path(f"common_{right_file_name}"), index=False)
            self.stats_result[f"common_{right_file_name}"] = right_common_df.shape[0]

            only_left_df = pd.concat([left_common_df, left_df]).drop_duplicates(keep=False, inplace=False)
            only_left_df.to_csv(get_csv_export_file_path(f"only_{left_file_name}"), index=False)
            self.stats_result[f"only_{left_file_name}"] = only_left_df.shape[0]

            only_right_df = pd.concat([right_common_df, right_df]).drop_duplicates(keep=False, inplace=False)
            only_right_df.to_csv(get_csv_export_file_path(f"only_{right_file_name}"), index=False)
            self.stats_result[f"only_{right_file_name}"] = only_right_df.shape[0]


def compare():
    process = PdUtil.Compare()
    process.compare()


if __name__ == "__main__":
    compare()
