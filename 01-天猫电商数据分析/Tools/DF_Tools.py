import shutil

import pandas as pd
from tabulate import tabulate


class DFPrint:
    """DataFrame 高级表格工具类"""

    @classmethod
    def display(
            cls,
            df: pd.DataFrame,
            style: str = "psql",
            hide_index: bool = True,
            max_rows: int = 20,
            align: str = "center"
    ) -> None:
        """
        美化打印 DataFrame，支持居中对齐

        参数:
            style: 表格风格（"psql", "github", "html" 等）
            hide_index: 是否隐藏行索引
            max_rows: 最大显示行数（避免大数据卡顿）
            align: 对齐方式（"left", "center", "right"）
        """
        if len(df) > max_rows:
            df = df.head(max_rows)
            print(f"显示前 {max_rows} 行（共 {len(df)} 行）\n")

        # 根据 align 参数设置对齐方式
        stralign = align if align in ["left", "center", "right"] else "left"

        tbl = tabulate(
            df,
            headers="keys",
            tablefmt=style,
            showindex=not hide_index,
            stralign=stralign
        )

        # 如果是居中对齐，按行处理并居中输出
        if align == "center":
            terminal_width = shutil.get_terminal_size((80, 20)).columns
            for line in tbl.split('\n'):
                print(line.center(terminal_width))
        else:
            print(tbl)

    @classmethod
    def to_markdown(cls, df: pd.DataFrame) -> str:
        """转换为 Markdown 表格"""
        return tabulate(df, headers="keys", tablefmt="github", showindex=False)

    @classmethod
    def to_html(cls, df: pd.DataFrame) -> str:
        """转换为 HTML 表格"""
        return tabulate(df, headers="keys", tablefmt="html", showindex=False)

    @classmethod
    def my_print(cls, my_title: str) -> None:
        print("*" * 20 + my_title + "*" * 20)
