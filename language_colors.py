# 常用开发语言色彩条块映射定义 (根据语言属性映射适合的 Emoji 颜色方块)
# 采用独立的 python 常量模块以避免动态加载时发生路径寻址或读取 JSON 的 IO 问题，利于维护喵。
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
