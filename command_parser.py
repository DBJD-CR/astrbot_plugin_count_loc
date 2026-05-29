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
        # 放开正则限制，支持匹配以 / 分割的任意多级嵌套目录（如 GitLab 的 group/subgroup1/subgroup2/repo）
        self.repo_pattern = re.compile(r"^([a-zA-Z0-9._-]+(?:/[a-zA-Z0-9._-]+)+)$")

    @staticmethod
    def clean_repo_path(repo_path: str | None) -> str | None:
        """
        统一对带协议前缀（如 https:// 或 http:// 等）以及 .git 结尾的仓库路径进行清洗和提纯喵。
        """
        if not repo_path:
            return repo_path

        # 1. 过滤协议前缀与提取主体
        # 如果包含协议前缀，我们截取域名（如 github.com、gitlab.com）后的全部剩余多段路径，兼容 GitLab 的多层级嵌套子组喵！
        if "://" in repo_path:
            path_parts = repo_path.split("://")[-1].split("/")
            if len(path_parts) >= 3:
                repo_path = "/".join(path_parts[1:])

        # 2. 移除 .git 结尾
        if repo_path.endswith(".git"):
            repo_path = repo_path[:-4]

        return repo_path

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

        # 使用非捕获的分隔符判断，确保不管是中文字符还是英文字符，都能在指令前缀紧跟空格或直接结尾时被准确剥离喵
        prefixes = [
            r"/代码统计",
            r"代码统计",
            r"/loc",
            r"loc",
            r"/count_loc",
            r"count_loc",
        ]
        # 使用 (?:\s+|$) 作为分隔边界，它匹配“一个或多个空白字符”或“字符串结尾”，避免了 \b 无法有效在中文上触发匹配的局限
        pattern_str = "^(" + "|".join(prefixes) + r")(?:\s+|$)"
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
        # 提取仓库路径：通常是第一个不带 '-' 的位置参数，或是符合多段格式的词
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

        # 如果没有找到完美的多段路径，则回退兼容带斜杠的单词
        if not repo_path:
            for word in words:
                if not word.startswith("-") and "/" in word:
                    repo_path = word
                    break
            if repo_path:
                remaining_args = [w for w in words if w != repo_path]

        # 职责划分单一化，在解析到 repo_path 时，对其调用统一的静态清洗函数喵
        if repo_path:
            repo_path = self.clean_repo_path(repo_path)

        if not repo_path:
            return None, {}, "⚠️ 无法识别仓库路径，请确认是否为 用户名/仓库名 的格式喵！"

        # 设置参数解析器，显式指定 add_help=False 禁用默认帮助动作，防范 SystemExit 崩溃风险
        parser = argparse.ArgumentParser(
            description="Code LOC Counter Parser", exit_on_error=False, add_help=False
        )
        parser.add_argument("-b", "--branch", type=str, default=None)
        parser.add_argument("-i", "--ignore", type=str, default=None)
        parser.add_argument("-g", "--gitlab", action="store_true", default=False)

        try:
            parsed_args, unknown = parser.parse_known_args(remaining_args)
        except Exception as e:
            # 捕获异常，并对原生报错信息做友好翻译，以改善对非技术用户的体验喵
            err_str = str(e)
            user_friendly_msg = "⚠️ 参数解析遇到了点小麻烦，请检查选项格式是否正确喵。"
            if "expected one argument" in err_str:
                user_friendly_msg = "⚠️ 参数输入格式有误喵！例如指定分支的 -b 或 忽略项的 -i 后面必须带上对应的值参数哦。"
            elif "ignored" in err_str:
                user_friendly_msg = "⚠️ 选项参数有误，请确保使用了正确的参数（如 -b 分支 / -i 忽略 / -g 使用GitLab）。"

            return (
                repo_path,
                {"branch": None, "ignored": None, "platform": "github"},
                user_friendly_msg,
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
