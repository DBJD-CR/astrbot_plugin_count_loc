import argparse
import re
from typing import Any


class CommandParser:
    """
    负责解析指令中带有的各项参数（如分支名、忽略项、平台标识、仓库路径等）。
    支持标准的命令行参数解析，例如：
    /代码统计 username/reponame --branch main --ignore node_modules,dist --gitlab
    同时也兼容更加简易或者手误的格式。
    """

    def __init__(self):
        # 匹配仓库路径的正则表达式，支持 username/reponame 的基本格式
        self.repo_pattern = re.compile(r"^([a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+)$")

    def parse_args(
        self, message_str: str
    ) -> tuple[str | None, dict[str, Any], str | None]:
        """
        解析用户发来的指令字符串。

        参数:
            message_str: 完整的用户输入消息，例如 "username/reponame -b main" 或 "代码统计 username/reponame"

        返回:
            repo_path: 解析出的仓库路径 (username/reponame)
            options: 包含 branch, ignored, platform 等参数的字典
            error_msg: 错误说明，如果解析正常则为 None
        """
        clean_text = message_str.strip()

        # 使用正则表达式配合单词边界，确保只有独立的指令前缀会被剥离
        # 例如不会把 "local test" 里的 "loc" 剥离掉喵
        prefixes = [
            r"/代码统计",
            r"代码统计",
            r"/loc",
            r"loc",
            r"/count_loc",
            r"count_loc",
        ]
        # 拼接成类似 ^(/(代码统计|loc|count_loc)|代码统计|loc|count_loc)\b 的正则表达式
        pattern_str = "^(" + "|".join(prefixes) + r")\b"
        clean_text = re.sub(pattern_str, "", clean_text, flags=re.IGNORECASE).strip()

        if not clean_text:
            return (
                None,
                {},
                (
                    "⚠️ 请提供要统计的仓库路径喵！\n"
                    "格式一：/代码统计 <用户名>/<仓库名>\n"
                    "格式二：/代码统计 <用户名>/<仓库名> --branch <分支名> --ignore <忽略文件或文件夹,以逗号分隔>\n"
                    "参数说明：\n"
                    "• --branch / -b : 指定分支（默认 master/main）\n"
                    "• --ignore / -i : 忽略的文件/目录，逗号分隔\n"
                    "• --gitlab / -g : 使用 GitLab 平台（默认 GitHub）"
                ),
            )

        # 我们先利用 argparse 的思想或简易拆分来解析命令行参数
        # 提取仓库路径：通常是第一个不带 '-' 的位置参数，或是符合 username/reponame 格式的词
        words = clean_text.split()

        repo_path = None
        remaining_args = []

        # 仅通过一次遍历，完成已知/未知参数的分类清洗
        for word in words:
            if (
                not repo_path
                and not word.startswith("-")
                and self.repo_pattern.match(word)
            ):
                repo_path = word
            else:
                remaining_args.append(word)

        # 如果没有找到完美的 username/reponame，则回退兼容带斜杠的单词
        if not repo_path:
            for word in words:
                if not word.startswith("-") and "/" in word:
                    repo_path = word
                    break
            if repo_path:
                remaining_args = [w for w in words if w != repo_path]

        if not repo_path:
            return None, {}, "⚠️ 无法识别仓库路径，请确认是否为 用户名/仓库名 的格式喵！"

        # 设置参数解析器
        parser = argparse.ArgumentParser(
            description="Code LOC Counter Parser", exit_on_error=False
        )
        parser.add_argument("-b", "--branch", type=str, default=None)
        parser.add_argument("-i", "--ignore", type=str, default=None)
        parser.add_argument("-g", "--gitlab", action="store_true", default=False)

        try:
            parsed_args, unknown = parser.parse_known_args(remaining_args)
        except Exception as e:
            # 如果解析出错，可以回退为简单的正则或默认解析，不抛出异常崩溃
            return (
                repo_path,
                {"branch": None, "ignored": None, "platform": "github"},
                f"解析参数时遇到一点小插曲喵，已使用默认参数。({str(e)})",
            )

        # 整理输出结果，防范 --ignore 传入空字符串如 --ignore "" 时解析结果为空白假值
        ignored_val = None
        if parsed_args.ignore is not None:
            ignored_list = [
                x.strip() for x in parsed_args.ignore.split(",") if x.strip()
            ]
            # 只有当非空时才赋值，否则保留为 None 以确保类型一致
            if ignored_list:
                ignored_val = ignored_list

        options = {
            "branch": parsed_args.branch,
            "ignored": ignored_val,
            "platform": "gitlab" if parsed_args.gitlab else "github",
        }

        return repo_path, options, None
