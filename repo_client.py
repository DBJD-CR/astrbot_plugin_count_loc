import asyncio

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
        # 采用惰性加载模式，此处不再同步创建 AsyncClient
        self.client = None

    def _get_client(self) -> httpx.AsyncClient:
        """
        获取当前异步客户端实例。
        如果当前客户端实例尚未创建或已经被关闭，则进行惰性实例化。
        这可以保证 httpx.AsyncClient 与发起异步请求时的 event loop 绑定，而不是与实例化 RepoClient 时的 loop 绑定喵。
        """
        if self.client is None or getattr(self.client, "is_closed", True):
            self.client = httpx.AsyncClient(timeout=self.timeout, follow_redirects=True)
        return self.client

    async def close(self):
        """关闭客户端，释放连接池资源"""
        if self.client and not getattr(self.client, "is_closed", False):
            try:
                await self.client.aclose()
            except Exception as e:
                logger.error(f"[代码统计] 释放资源时发生异常喵: {str(e)}")

    async def get_repo_loc(
        self,
        repo_path: str,
        platform: str = "github",
        branch: str | None = None,
        ignored: list[str] | str | None = None,
    ) -> list[dict[str, str | int]] | str:
        """
        异步调用 CodeTabs API 获取仓库代码行数统计数据喵。

        参数:
            repo_path: 仓库路径，如 "username/reponame"
            platform: 平台，"github" 或 "gitlab"
            branch: 分支名称
            ignored: 忽略的文件/文件夹列表（支持列表或逗号分隔的字符串）

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
            # 归一化重构逻辑，避免 if-else 的结构性重复
            # 不论入参是单个 str（如 "a,b"）还是列表（如 ["a", "b"]），统一转为可迭代的列表提取清洗
            raw_items = ignored.split(",") if isinstance(ignored, str) else ignored
            ignored_list = [
                item.strip()
                for item in raw_items
                if isinstance(item, str) and item.strip()
            ]
            if ignored_list:
                params["ignored"] = ",".join(ignored_list)

        logger.info(f"[代码统计] 正在请求 {platform} 仓库: {repo_path}, 参数: {params}")

        # 使用惰性方法获取当前绑定的 httpx.AsyncClient 对象喵
        client = self._get_client()

        try:
            response = await client.get(self.BASE_URL, params=params)

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
        except asyncio.CancelledError:
            # 显式重新抛出 CancelledError 异常，避免在异步环境协程被取消时异常被静默吞没喵
            raise
        except Exception as e:
            logger.error(f"[代码统计] 未知异常: {str(e)}")
            return f"发生未知错误喵: {str(e)}"
