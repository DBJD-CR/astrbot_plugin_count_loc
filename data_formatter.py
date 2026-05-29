from datetime import datetime, timezone


class DataFormatter:
    """
    负责将 API 返回的原始数据转换为易于阅读的文本列表或统计摘要，并绘制占比条。
    采用“列表卡片化”排版，完美适配移动端非等宽字体与窄屏折行问题喵。
    """

    # 常用开发语言色彩条块映射定义喵 (根据语言属性映射适合的 Emoji 颜色方块)
    LANGUAGE_COLORS = {
        "Python": "🟦",  # 蓝色
        "JavaScript": "🟨",  # 黄色
        "TypeScript": "🟦",  # 蓝色
        "TypeScript Typings": "🟦",  # 蓝色
        "HTML": "🟥",  # 红色/橙红
        "CSS": "🟪",  # 紫色
        "Java": "🟫",  # 褐色
        "C": "⬜",  # 白色/灰色
        "C++": "🟦",  # 蓝色
        "C#": "🟩",  # 绿色
        "Go": "🟦",  # 蓝色
        "Rust": "🟫",  # 褐色
        "PHP": "🟪",  # 紫色
        "Ruby": "🟥",  # 红色
        "Swift": "🟧",  # 橙色
        "Kotlin": "🟪",  # 紫色
        "Shell": "🟩",  # 绿色
        "Markdown": "⬛",  # 黑色
        "YAML": "🟨",  # 黄色
        "JSON": "🟨",  # 黄色
        "Vue": "🟩",  # 绿色
        "JSX": "🟦",  # 蓝色
        "TSX": "🟦",  # 蓝色
        "Dart": "🟦",  # 蓝色
        "Flutter": "🟦",  # 蓝色
        "Objective-C": "🟦",  # 蓝色
        "Scala": "🟥",  # 红色
        "Haskell": "🟪",  # 紫色
        "Lua": "🟦",  # 蓝色
        "Perl": "🟦",  # 蓝色
        "R": "🟦",  # 蓝色
        "SQL": "🟫",  # 褐色
        "CMake": "⬛",  # 黑色
        "Makefile": "⬛",  # 黑色
        "Docker ignore": "⬛",  # 黑色
        "Dockerfile": "🐳",  # 蓝鲸/Docker专用
        "SVG": "🟨",  # 黄色
        "TOML": "🟫",  # 褐色
        "INI": "🟫",  # 褐色
        "XML": "🟧",  # 橙色
        "Sass": "🟪",  # 紫色
        "Less": "🟦",  # 蓝色
        "Stylus": "🟫",  # 褐色
        "Assembly": "🟥",  # 红色
        "Fortran": "🟪",  # 紫色
        "PowerShell": "🟦",  # 蓝色
        "Powershell": "🟦",  # 蓝色 (针对API返回名称的额外映射)
        "Batchfile": "🟩",  # 绿色
        "Batch": "🟩",  # 绿色 (针对API返回名称的额外映射)
        "Systemd": "🟫",  # 褐色
        "Other": "⬜",  # 其他/灰色
    }

    DEFAULT_COLOR = "⬜"  # 默认未识别颜色方块

    @classmethod
    def _generate_percentage_bar(
        cls, languages_info: list[tuple[str, float]], bar_length: int = 15
    ) -> str:
        """
        根据各语言所占比例动态生成文本形式的彩色渐变进度条喵。
        """
        if not languages_info:
            return ""

        bar_chars = []
        total_assigned = 0
        allocated = []

        for idx, (name, pct) in enumerate(languages_info):
            # 精确计算格数
            exact_chars = (pct / 100.0) * bar_length
            char_count = int(exact_chars)

            # 保存余数用于补充剩余的格子
            remainder = exact_chars - char_count
            allocated.append(
                {
                    "index": idx,
                    "name": name,
                    "count": char_count,
                    "remainder": remainder,
                    "pct": pct,
                }
            )
            total_assigned += char_count

        # 如果因为向下取整导致还有空闲格子，把空闲格子按余数从大到小分给各个语言
        free_slots = bar_length - total_assigned
        if free_slots > 0:
            # 过滤出占比大于 0 的，并按余数降序排列
            allocated.sort(key=lambda x: x["remainder"], reverse=True)
            for i in range(min(free_slots, len(allocated))):
                if allocated[i]["pct"] > 0:
                    allocated[i]["count"] += 1

            # 恢复原有排位顺序以保持占比降序一致
            allocated.sort(key=lambda x: x["index"])

        # 生成彩色组成条
        for item in allocated:
            color = cls.LANGUAGE_COLORS.get(item["name"], cls.DEFAULT_COLOR)
            bar_chars.append(color * item["count"])

        return "".join(bar_chars)

    @classmethod
    def format_loc_report(
        cls,
        data: list[dict[str, str | int]],
        repo_path: str,
        platform: str,
        branch: str | None = None,
        ignored: list[str] | str | None = None,
    ) -> str:
        """
        将代码行数统计数据格式化为精美的文本列表，完美适配手机等非等宽字体客户端喵。
        """
        if not data:
            return "没有获取到任何有效的代码统计数据喵。"

        # 区分 Total 与其他语言数据
        languages = []
        total_data = None

        for item in data:
            if item.get("language") == "Total":
                total_data = item
            else:
                languages.append(item)

        # 按代码行数降序排序
        languages.sort(key=lambda x: int(x.get("linesOfCode") or 0), reverse=True)

        total_loc = sum(int(lang.get("linesOfCode") or 0) for lang in languages)

        # 1. 计算前 5 大语言（及其他）占比信息喵
        top_languages = languages[:5]
        other_languages = languages[5:]

        lang_percentages = []

        # 处理前 5 大语言
        for lang in top_languages:
            loc = int(lang.get("linesOfCode") or 0)
            pct = (loc / total_loc * 100) if total_loc > 0 else 0.0
            lang_percentages.append((lang.get("language"), pct))

        # 处理其他语言的合并
        if other_languages:
            other_loc = sum(
                int(lang.get("linesOfCode") or 0) for lang in other_languages
            )
            other_pct = (other_loc / total_loc * 100) if total_loc > 0 else 0.0
            if other_pct > 0:
                lang_percentages.append(("Other", other_pct))

        # 生成彩色组成条
        color_bar = cls._generate_percentage_bar(lang_percentages, bar_length=15)

        # 构建头部信息
        title_platform = "GitHub" if platform.lower() == "github" else "GitLab"
        branch_str = branch if branch else "默认分支"

        # 转换 ignored 为展示字符串
        ignored_str = "无"
        if ignored:
            if isinstance(ignored, list):
                ignored_str = ", ".join(ignored)
            elif isinstance(ignored, str):
                ignored_str = ignored

        try:
            # 尝试获取带系统本地时区的时间
            now = datetime.now(timezone.utc).astimezone()
            time_str = now.strftime("%Y-%m-%d %H:%M:%S %Z")
        except Exception:
            try:
                # 备用：不通过 utc 转换，直接取当前时间
                now = datetime.now()
                time_str = now.strftime("%Y-%m-%d %H:%M:%S") + " (本地时间)"
            except Exception as e:
                time_str = f"获取失败 ({str(e)})"

        lines = []
        lines.append(f"📊 {title_platform} 仓库分析报告")
        lines.append(f"项目: {repo_path}")
        lines.append(f"查询分支: {branch_str}")
        lines.append(f"忽略文件/目录: {ignored_str}")
        lines.append(f"查询时间: {time_str}")
        lines.append("=" * 30)

        # 语言占比展示条
        if color_bar:
            lines.append("文件组成:")
            lines.append(f"{color_bar}\n")
            # 占比文字说明
            pct_desc = []
            for name, pct in lang_percentages:
                display_name = "其他" if name == "Other" else name
                icon = cls.LANGUAGE_COLORS.get(name, cls.DEFAULT_COLOR)
                pct_desc.append(f"{icon} {display_name} {pct:.1f}%")

            # 每行放 2 个占比图例，以防文字堆叠在手机上换行难看喵
            for i in range(0, len(pct_desc), 2):
                lines.append("   " + "   ".join(pct_desc[i : i + 2]))
            lines.append("=" * 30)

        # 语言明细列表 (替代旧版的表格渲染，采用高兼容性的列表结构)
        lines.append("📈 语言明细:")
        for lang in languages:
            name = lang.get("language", "Unknown")
            # 截断过长的语言名字
            if len(name) > 20:
                name = name[:17] + "..."

            files = int(lang.get("files") or 0)
            lines_code = int(lang.get("linesOfCode") or 0)
            comments = int(lang.get("comments") or 0)

            icon = cls.LANGUAGE_COLORS.get(name, cls.DEFAULT_COLOR)

            # 使用列表项格式，即便在非等宽字体或手机屏幕折行时也绝不会乱，超级整齐！
            lines.append(f" 🔹{icon} {name}:")
            lines.append(f"    ├─ 文件数量: {files:,} 个")
            lines.append(f"    ├─ 代码行数: {lines_code:,} 行")
            lines.append(f"    └─ 注释行数: {comments:,} 行")

        lines.append("=" * 30)

        # 追加汇总信息
        if total_data:
            tot_files = int(total_data.get("files") or 0)
            tot_lines = int(total_data.get("lines") or 0)
            tot_blanks = int(total_data.get("blanks") or 0)
            tot_comments = int(total_data.get("comments") or 0)
            tot_code = int(total_data.get("linesOfCode") or 0)

            # 用千位分隔符以及 emoji 图标进行美化展示
            lines.append(f"📁 总计文件数量 : {tot_files:,} 个")
            lines.append(f"💻 总计代码行数 : {tot_code:,} 行")
            lines.append(f"💬 总计注释行数 : {tot_comments:,} 行")
            lines.append(f"🫙 总计空白行数 : {tot_blanks:,} 行")
            lines.append(f"📈 总计物理行数 : {tot_lines:,} 行")

            # 计算代码注释率：使用“总计代码行数 (lines Of Code)”作为分母喵！
            # 这样可以精准反应代码的文档健康度，而不受非代码文件（如空白行等）的干扰喵
            if tot_code > 0:
                comment_ratio = (tot_comments / tot_code) * 100

                # 依据注释率高低判定健康度喵
                if comment_ratio > 20:
                    health_status = "🟢 极佳 (文档超详细喵！)"
                elif comment_ratio >= 10:
                    health_status = "🟡 良好 (注释合适喵)"
                elif comment_ratio >= 5:
                    health_status = "🟠 偏低 (阅读起来要耐心喵)"
                else:
                    health_status = "🔴 极低 (简直是无注释屎山喵！😱)"

                lines.append(
                    f"🩺 代码注释比例 : {comment_ratio:.1f}% ({health_status})"
                )

        else:
            lines.append("未获取到总计汇总数据喵。")

        return "\n".join(lines)
