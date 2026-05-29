import httpx

from astrbot.api import logger


class RepoClient:
    """
    负责与 CodeTabs API 通信获取代码行数统计数据。
    """

    BASE_URL = "https://api.codetabs.com/v1/loc"

    def __init__(self):
        # 官方文档限制 5 秒一次请求，因此超时时间需要设得合理一些
        self.timeout = 30.0
        # 开启 follow_redirects=True 以处理服务器重定向 (如 301 Moved Permanently)
        self.client = httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)

    async def close(self):
        """关闭客户端，释放连接池资源"""
        await self.client.aclose()

    async def get_repo_loc(
        self,
        repo_path: str,
        platform: str = "github",
        branch: str | None = None,
        ignored: list[str] | None = None,
    ) -> list[dict[str, str | int]] | str:
        """
        异步调用 CodeTabs API 获取仓库代码行数统计数据喵。

        参数:
            repo_path: 仓库路径，如 "username/reponame"
            platform: 平台，"github" 或 "gitlab"
            branch: 分支名称
            ignored: 忽略的文件/文件夹列表

        返回:
            List[Dict]: 语言统计数据列表，最后一项通常为 Total
            str: 错误信息
        """
        params = {}
        # 根据 API 文档，参数形式为: github=username/reponame 或 gitlab=username/reponame
        # 或者 source=username/reponame (github)
        # 支持区分大小写或者不同参数形式，我们选用文档里给定的 ?github= 或 ?gitlab=
        params[platform] = repo_path

        if branch:
            params["branch"] = branch

        if ignored:
            params["ignored"] = ",".join(ignored)

        logger.info(f"[代码统计] 正在请求 {platform} 仓库: {repo_path}, 参数: {params}")

        try:
            response = await self.client.get(self.BASE_URL, params=params)

            # 处理可能遇到的 429 速率限制错误
            if response.status_code == 429:
                logger.warning("[代码统计] 触发 API 速率限制 (429 Too Many Requests)")
                return "请求过于频繁，CodeTabs API 限制每 5 秒只能请求一次喵。请稍等片刻后再试吧！"

            # 处理其他 HTTP 错误
            response.raise_for_status()

            try:
                data = response.json()
            except ValueError:
                logger.error(f"[代码统计] 解析 JSON 失败，响应内容: {response.text}")
                return "API 响应解析失败，可能返回了非 JSON 数据喵！"

            if not isinstance(data, list):
                logger.error(f"[代码统计] 错误的 API 响应格式: {data}")
                return "API 响应格式异常，请稍后再试喵！"

            return data

        except httpx.HTTPStatusError as e:
            logger.error(
                f"[代码统计] HTTP 错误: {e.response.status_code} - {e.response.text}"
            )
            if e.response.status_code == 404:
                return "未找到该仓库，请检查用户名、仓库名或分支名是否正确，且仓库必须是公开的喵！"
            return f"请求失败，API 返回了状态码 {e.response.status_code} 喵。"
        except httpx.RequestError as e:
            logger.error(f"[代码统计] 网络请求异常: {str(e)}")
            return f"网络连接异常，无法访问 API 喵。错误详情: {str(e)}"
        except Exception as e:
            logger.error(f"[代码统计] 未知异常: {str(e)}")
            return f"发生未知错误喵: {str(e)}"
