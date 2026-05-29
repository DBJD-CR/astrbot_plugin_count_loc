import astrbot.api.message_components as Comp
from astrbot.api import logger
from astrbot.api.event import AstrMessageEvent, filter
from astrbot.api.star import Context, Star

from .command_parser import CommandParser
from .data_formatter import DataFormatter

# 导入我们的自定义多模块组件喵
from .repo_client import RepoClient


class CountLocPlugin(Star):
    """
    AstrBot 代码行数统计分析插件。
    可以一键分析 GitHub 或 GitLab 上的公开仓库代码，支持分支选择和忽略项过滤喵！
    """

    def __init__(self, context: Context):
        super().__init__(context)
        self.repo_client = RepoClient()
        self.command_parser = CommandParser()

    async def initialize(self):
        """异步初始化方法"""
        logger.info("[代码统计] 插件成功初始化喵！")

    # 注册“代码统计”指令，并提供别名：codeloc, 测代码, 统计代码, loc
    @filter.command("代码统计", alias={"codeloc", "测代码", "统计代码", "loc"})
    async def code_statistics(self, event: AstrMessageEvent):
        """分析指定 GitHub/GitLab 仓库的代码行数、文件数和注释喵。

        用法:
        /代码统计 <用户名>/<仓库名> [选项]

        选项:
        -b, --branch <分支名>   指定分支（默认 master/main）
        -i, --ignore <忽略项>   忽略的文件或文件夹，逗号分隔
        -g, --gitlab           使用 GitLab 平台（默认 GitHub）
        """
        message_str = event.message_str.strip()

        # 1. 使用 CommandParser 解析用户输入
        repo_path, options, error_msg = self.command_parser.parse_args(message_str)

        if error_msg:
            # 如果有解析错误（例如用户直接打了 "/代码统计"），回复帮助提示
            yield event.plain_result(error_msg)
            return

        # 2. 友好地提示用户正在查询中
        platform_name = "GitLab" if options.get("platform") == "gitlab" else "GitHub"
        branch_info = (
            f"，分支: {options.get('branch')}" if options.get("branch") else ""
        )
        yield event.plain_result(
            f"🔍 正在为您努力测算 {platform_name} 仓库 {repo_path} {branch_info} 的代码行数，请稍候喵..."
        )

        # 3. 发送请求获取数据
        result = await self.repo_client.get_repo_loc(
            repo_path=repo_path,
            platform=options.get("platform", "github"),
            branch=options.get("branch"),
            ignored=options.get("ignored"),
        )

        # 4. 根据请求结果判断与处理
        if isinstance(result, str):
            # 返回字符串代表 API 报错或者抓取失败
            yield event.plain_result(f"❌ [代码统计] 统计失败了喵。\n原因: {result}")
            return

        # 5. 格式化统计结果
        report_text = DataFormatter.format_loc_report(
            data=result,
            repo_path=repo_path,
            platform=options.get("platform", "github"),
            branch=options.get("branch"),
        )

        # 6. 使用群合并转发消息（转发节点）回复（若平台和协议端支持），保证群聊版面整洁！
        try:
            self_id = int(event.get_self_id())
        except Exception:
            self_id = 0

        try:
            # 构造群合并转发节点 Node
            node = Comp.Node(
                uin=self_id, name="代码统计", content=[Comp.Plain(report_text)]
            )
            # 发送消息链
            yield event.chain_result([node])
        except Exception as e:
            logger.warning(
                f"[代码统计] 使用转发节点发送失败，回退为普通纯文本消息发送喵。({str(e)})"
            )
            yield event.plain_result(report_text)

    async def terminate(self):
        """销毁方法"""
        await self.repo_client.close()
        logger.info("[代码统计] 插件已被安全停用喵。")
