"""
Agent Router for dcai-demo-platform.
Parses @mention and keywords from chat messages to route to the correct Agent service.
"""
import re
from dataclasses import dataclass
from typing import Optional

MENTION_RE = re.compile(r'@([\w][\w\-]*)(?::([\w][\w\-]*))?')

@dataclass
class RouteResult:
    agent_name: str
    tool_name: str
    tool_input: dict
    action: str                      # "open_iframe" | "stream_agent"
    iframe_url: Optional[str] = None
    stream_url: Optional[str] = None
    hint: str = ''                   # user-facing hint message


# Registry: add new agents here only — no other code changes needed
AGENT_REGISTRY = {
    'DataFlow-Agent': {
        'aliases': ['DataFlow', 'dataflow', 'df'],
        'tool': 'open_dataflow_canvas',
        'keywords': ['pipeline', '算子', 'operator', '数据处理', 'dataflow',
                     '工作流', 'workflow', '节点', 'node', '数据流'],
        'action': 'open_iframe',
        'iframe_url': '/dataflow/canvas',
        'hint': '正在为您打开 DataFlow Pipeline 构建器...',
    },
    'LoopAI-Agent': {
        'aliases': ['LoopAI', 'loopai', 'loop'],
        'tool': 'run_loopai_agent',
        'keywords': ['训练', 'train', '数据集', 'dataset', '自动优化',
                     '模型评估', 'fine-tune', '微调', 'loopai', 'finetune'],
        'action': 'stream_agent',
        'iframe_url': '/apps/OpenDCAI/Dataflow-LoopAI',
        'stream_url': '/api/v2/loopai/starter/agent/message/stream',
        'hint': '正在启动 LoopAI 智能循环 Agent...',
    },
    'DFAgent': {
        'aliases': ['DFAgent', 'dfagent'],
        'tool': 'open_dfagent',
        'keywords': ['算子推荐', 'pipeline推荐', 'pipeline recommendation', 'prompt优化',
                     '数据采集', 'operator qa', 'operator', 'web collection'],
        'action': 'open_iframe',
        'iframe_url': '/apps/OpenDCAI/DataFlow-Agent',
        'hint': '正在打开 DataFlow-Agent 工作台...',
    },
    'PackageEditor-Agent': {
        'aliases': ['PackageEditor', 'package-editor', 'pkg'],
        'tool': 'open_package_editor',
        'keywords': ['写算子', 'operator package', 'package editor', '算子开发', 'operator write'],
        'action': 'open_iframe',
        'iframe_url': '/apps/OpenDCAI/PackageEditor-Agent',
        'hint': '正在打开算子包编辑工作台...',
    },
}


class AgentRouter:
    def route(self, message: str) -> Optional[RouteResult]:
        result = self._by_mention(message)
        if result:
            return result
        return self._by_keywords(message)

    def _by_mention(self, message: str) -> Optional[RouteResult]:
        for mention, submodule in MENTION_RE.findall(message):
            mention_key = mention.lower()
            for name, cfg in AGENT_REGISTRY.items():
                aliases = [alias.lower() for alias in cfg.get('aliases', [])]
                if mention_key == name.lower() or mention_key in aliases:
                    clean = MENTION_RE.sub('', message).strip()
                    return self._build(name, cfg, clean, submodule=submodule)
        return None

    def _by_keywords(self, message: str) -> Optional[RouteResult]:
        normalized = message.lower()
        scores = {
            name: sum(1 for kw in cfg['keywords'] if kw.lower() in normalized)
            for name, cfg in AGENT_REGISTRY.items()
        }
        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return None
        return self._build(best, AGENT_REGISTRY[best], message)

    def _build(self, name: str, cfg: dict, message: str, submodule: str = '') -> RouteResult:
        tool_input = self._extract_input(cfg['tool'], message, submodule=submodule)
        iframe_url = cfg.get('iframe_url')
        if submodule and name == 'DFAgent':
            iframe_url = f"{iframe_url}?tab={self._normalize_submodule(submodule)}"
        if name == 'PackageEditor-Agent':
            iframe_url = f"/apps/OpenDCAI/PackageEditor-Agent?package={tool_input['package_id']}"
        return RouteResult(
            agent_name=name,
            tool_name=cfg['tool'],
            tool_input=tool_input,
            action=cfg['action'],
            iframe_url=iframe_url,
            stream_url=cfg.get('stream_url'),
            hint=cfg.get('hint', ''),
        )

    def _normalize_submodule(self, submodule: str) -> str:
        return submodule.strip().replace('-', '_').lower()

    def _extract_input(self, tool: str, message: str, submodule: str = '') -> dict:
        normalized = message.lower()
        if tool == 'open_dataflow_canvas':
            intent = 'create_pipeline'
            if any(w in normalized for w in ['编辑', '修改', 'edit']):
                intent = 'edit_pipeline'
            elif any(w in normalized for w in ['查看', '列表', 'list', '算子库']):
                intent = 'view_operators'
            return {'intent': intent, 'hint': message[:200]}
        if tool == 'run_loopai_agent':
            return {'task_description': message}
        if tool == 'open_dfagent':
            return {
                'task_description': message,
                'tab': self._normalize_submodule(submodule) if submodule else '',
            }
        if tool == 'open_package_editor':
            package_id = self._guess_package_id(message)
            return {
                'package_id': package_id,
                'task_description': message,
            }
        return {'message': message}

    def _guess_package_id(self, message: str) -> str:
        normalized = message.lower()
        try:
            from df.services import catalog
        except Exception:
            return 'core_text'

        for package in catalog.list_packages():
            package_id = package['id']
            package_name = package.get('name', '')
            if package_id.lower() in normalized or package_name.lower() in normalized:
                return package_id
        return 'core_text'
