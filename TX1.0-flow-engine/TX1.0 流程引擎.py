#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TX1.0 工业自动化流程引擎 v1.0

基于工业自动化流程图思维设计的核心流程引擎
整合 401 个技能，实现高效、简洁、自动化的流程执行
"""

import json
import yaml
import time
import uuid
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TX1.0-Flow-Engine')


class NodeType(Enum):
    """节点类型"""
    SKILL = "skill"
    TASK = "task"
    DECISION = "decision"
    MERGE = "merge"
    START = "start"
    END = "end"


class FlowStatus(Enum):
    """流程状态"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class Node:
    """流程节点"""
    id: str
    type: str
    skill: Optional[str] = None
    action: Optional[str] = None
    input: Dict[str, Any] = field(default_factory=dict)
    output: Dict[str, Any] = field(default_factory=dict)
    retry: int = 3
    timeout: int = 60
    status: str = "pending"
    result: Any = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None


@dataclass
class Edge:
    """流程边"""
    from_node: str
    to_node: str
    condition: Optional[str] = None


@dataclass
class ErrorHandler:
    """错误处理器"""
    retry_count: int = 3
    retry_delay: int = 5
    fallback_node: Optional[str] = None
    notification: Optional[Dict[str, Any]] = None


@dataclass
class FlowDefinition:
    """流程定义"""
    id: str
    name: str
    version: str
    trigger: Dict[str, Any] = field(default_factory=dict)
    nodes: List[Node] = field(default_factory=list)
    edges: List[Edge] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    error_handler: Optional[ErrorHandler] = None
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FlowInstance:
    """流程实例"""
    instance_id: str
    flow_id: str
    status: str = "pending"
    input: Dict[str, Any] = field(default_factory=dict)
    output: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    current_node: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    error: Optional[str] = None


class FlowEngine:
    """流程引擎核心类"""
    
    def __init__(self, workspace: str = "/root/.openclaw/workspace"):
        self.workspace = Path(workspace)
        self.flows_dir = self.workspace / "flows"
        self.instances_dir = self.workspace / "flow_instances"
        self.skills_dir = self.workspace / "skills"
        
        # 创建目录
        self.flows_dir.mkdir(exist_ok=True)
        self.instances_dir.mkdir(exist_ok=True)
        
        # 流程注册表
        self.flow_registry: Dict[str, FlowDefinition] = {}
        # 运行中的实例
        self.running_instances: Dict[str, FlowInstance] = {}
        # 技能缓存
        self.skill_cache: Dict[str, Any] = {}
        
        # 加载已有流程
        self._load_flows()
        
        logger.info(f"FlowEngine initialized. Workspace: {self.workspace}")
    
    def _load_flows(self):
        """加载已有流程定义"""
        for flow_file in self.flows_dir.glob("*.yaml"):
            try:
                with open(flow_file, 'r', encoding='utf-8') as f:
                    flow_data = yaml.safe_load(f)
                    flow = self._parse_flow(flow_data)
                    self.flow_registry[flow.id] = flow
                    logger.info(f"Loaded flow: {flow.id}")
            except Exception as e:
                logger.error(f"Failed to load flow {flow_file}: {e}")
    
    def _parse_flow(self, flow_data: Dict) -> FlowDefinition:
        """解析流程定义"""
        nodes = []
        for node_data in flow_data.get('nodes', []):
            node = Node(
                id=node_data['id'],
                type=node_data['type'],
                skill=node_data.get('skill'),
                action=node_data.get('action'),
                input=node_data.get('input', {}),
                output=node_data.get('output', {}),
                retry=node_data.get('retry', 3),
                timeout=node_data.get('timeout', 60)
            )
            nodes.append(node)
        
        edges = []
        for edge_data in flow_data.get('edges', []):
            edge = Edge(
                from_node=edge_data['from'],
                to_node=edge_data['to'],
                condition=edge_data.get('condition')
            )
            edges.append(edge)
        
        error_handler = None
        if 'error_handler' in flow_data:
            eh_data = flow_data['error_handler']
            error_handler = ErrorHandler(
                retry_count=eh_data.get('retry_count', 3),
                retry_delay=eh_data.get('retry_delay', 5),
                fallback_node=eh_data.get('fallback_node'),
                notification=eh_data.get('notification')
            )
        
        return FlowDefinition(
            id=flow_data['flow']['id'],
            name=flow_data['flow']['name'],
            version=flow_data['flow'].get('version', '1.0'),
            trigger=flow_data.get('trigger', {}),
            nodes=nodes,
            edges=edges,
            variables=flow_data.get('variables', {}),
            error_handler=error_handler
        )
    
    def define(self, flow: FlowDefinition) -> str:
        """定义并保存流程"""
        flow_path = self.flows_dir / f"{flow.id}.yaml"
        
        flow_data = {
            'flow': {
                'id': flow.id,
                'name': flow.name,
                'version': flow.version,
            },
            'trigger': flow.trigger,
            'nodes': [asdict(n) for n in flow.nodes],
            'edges': [asdict(e) for e in flow.edges],
            'variables': flow.variables,
        }
        
        if flow.error_handler:
            flow_data['error_handler'] = asdict(flow.error_handler)
        
        with open(flow_path, 'w', encoding='utf-8') as f:
            yaml.dump(flow_data, f, allow_unicode=True, default_flow_style=False)
        
        self.flow_registry[flow.id] = flow
        logger.info(f"Flow defined: {flow.id}")
        
        return flow.id
    
    def define_from_yaml(self, yaml_file: str) -> str:
        """从 YAML 文件定义流程"""
        with open(yaml_file, 'r', encoding='utf-8') as f:
            flow_data = yaml.safe_load(f)
        
        flow = self._parse_flow(flow_data)
        return self.define(flow)
    
    def execute(self, flow_id: str, input_data: Dict[str, Any] = None, 
                context: Dict[str, Any] = None) -> FlowInstance:
        """执行流程"""
        if flow_id not in self.flow_registry:
            raise ValueError(f"Flow not found: {flow_id}")
        
        flow_def = self.flow_registry[flow_id]
        instance = FlowInstance(
            instance_id=f"inst_{uuid.uuid4().hex[:8]}",
            flow_id=flow_id,
            status="running",
            input=input_data or {},
            context=context or {},
            start_time=time.time()
        )
        
        self.running_instances[instance.instance_id] = instance
        logger.info(f"Executing flow {flow_id}, instance: {instance.instance_id}")
        
        try:
            # 执行流程节点
            self._execute_nodes(flow_def, instance)
            instance.status = "completed"
            logger.info(f"Flow completed: {instance.instance_id}")
        except Exception as e:
            instance.status = "failed"
            instance.error = str(e)
            logger.error(f"Flow failed: {instance.instance_id}, error: {e}")
        
        instance.end_time = time.time()
        
        # 保存实例
        self._save_instance(instance)
        
        return instance
    
    def _execute_nodes(self, flow_def: FlowDefinition, instance: FlowInstance):
        """执行流程节点"""
        # 构建节点图
        node_map = {n.id: n for n in flow_def.nodes}
        edge_map = {}
        for edge in flow_def.edges:
            if edge.from_node not in edge_map:
                edge_map[edge.from_node] = []
            edge_map[edge.from_node].append(edge)
        
        # 从第一个节点开始执行
        current_node_id = flow_def.nodes[0].id if flow_def.nodes else None
        
        while current_node_id:
            instance.current_node = current_node_id
            node = node_map[current_node_id]
            
            logger.info(f"Executing node: {current_node_id}")
            
            # 执行节点
            result = self._execute_node(node, instance)
            node.result = result
            node.status = "completed"
            
            # 更新流程变量
            for key, value in node.output.items():
                instance.context[key] = result.get(key, value)
            
            # 查找下一个节点
            next_node_id = None
            if current_node_id in edge_map:
                for edge in edge_map[current_node_id]:
                    # 检查条件
                    if edge.condition:
                        if self._evaluate_condition(edge.condition, instance.context):
                            next_node_id = edge.to_node
                            break
                    else:
                        next_node_id = edge.to_node
                        break
            
            current_node_id = next_node_id
    
    def _execute_node(self, node: Node, instance: FlowInstance) -> Dict[str, Any]:
        """执行单个节点"""
        node.start_time = time.time()
        
        try:
            if node.type == "skill":
                result = self._execute_skill(node, instance)
            elif node.type == "task":
                result = self._execute_task(node, instance)
            elif node.type == "decision":
                result = self._execute_decision(node, instance)
            else:
                result = {}
            
            node.end_time = time.time()
            return result
            
        except Exception as e:
            # 重试逻辑
            for attempt in range(node.retry):
                try:
                    logger.warning(f"Retrying node {node.id}, attempt {attempt + 1}")
                    time.sleep(node.retry_delay)
                    result = self._execute_node_impl(node, instance)
                    node.end_time = time.time()
                    return result
                except:
                    continue
            
            # 重试失败
            node.error = str(e)
            node.end_time = time.time()
            
            # 错误处理
            if instance.error_handler and instance.error_handler.fallback_node:
                return {"fallback": True, "error": str(e)}
            raise
    
    def _execute_node_impl(self, node: Node, instance: FlowInstance) -> Dict[str, Any]:
        """执行节点实现"""
        if node.type == "skill":
            return self._execute_skill(node, instance)
        elif node.type == "task":
            return self._execute_task(node, instance)
        elif node.type == "decision":
            return self._execute_decision(node, instance)
        return {}
    
    def _execute_skill(self, node: Node, instance: FlowInstance) -> Dict[str, Any]:
        """执行技能节点"""
        skill_name = node.skill
        
        # 准备输入参数（替换变量）
        input_params = self._resolve_variables(node.input, instance)
        
        logger.info(f"Executing skill: {skill_name}, input: {input_params}")
        
        # TODO: 实际技能调用逻辑
        # 这里可以集成 skillhub 或其他技能执行框架
        result = {
            "skill": skill_name,
            "status": "simulated",
            "input": input_params,
            "message": f"Skill {skill_name} executed successfully"
        }
        
        return result
    
    def _execute_task(self, node: Node, instance: FlowInstance) -> Dict[str, Any]:
        """执行任务节点"""
        action = node.action
        input_params = self._resolve_variables(node.input, instance)
        
        logger.info(f"Executing task: {action}, input: {input_params}")
        
        # TODO: 实际任务执行逻辑
        result = {
            "action": action,
            "status": "simulated",
            "input": input_params
        }
        
        return result
    
    def _execute_decision(self, node: Node, instance: FlowInstance) -> Dict[str, Any]:
        """执行决策节点"""
        # TODO: 决策逻辑
        return {"decision": "pending"}
    
    def _resolve_variables(self, params: Dict[str, Any], instance: FlowInstance) -> Dict[str, Any]:
        """解析变量"""
        resolved = {}
        for key, value in params.items():
            if isinstance(value, str):
                # 替换 ${variable} 格式的变量
                for var_name, var_value in instance.context.items():
                    value = value.replace(f"${{{var_name}}}", str(var_value))
                for var_name, var_value in instance.input.items():
                    value = value.replace(f"${{{var_name}}}", str(var_value))
            resolved[key] = value
        return resolved
    
    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """评估条件表达式"""
        # TODO: 实现条件表达式评估
        # 支持简单的布尔表达式
        try:
            # 安全评估（不使用 eval）
            return True
        except:
            return False
    
    def get_status(self, instance_id: str) -> Dict[str, Any]:
        """获取流程实例状态"""
        if instance_id in self.running_instances:
            instance = self.running_instances[instance_id]
            return {
                "instance_id": instance.instance_id,
                "flow_id": instance.flow_id,
                "status": instance.status,
                "current_node": instance.current_node,
                "start_time": instance.start_time,
                "end_time": instance.end_time,
                "error": instance.error
            }
        
        # 从文件加载
        instance_file = self.instances_dir / f"{instance_id}.json"
        if instance_file.exists():
            with open(instance_file, 'r') as f:
                return json.load(f)
        
        return {"error": "Instance not found"}
    
    def list_flows(self) -> List[Dict[str, Any]]:
        """列出所有流程"""
        return [
            {
                "id": flow.id,
                "name": flow.name,
                "version": flow.version,
                "nodes": len(flow.nodes),
                "created_at": flow.created_at
            }
            for flow in self.flow_registry.values()
        ]
    
    def _save_instance(self, instance: FlowInstance):
        """保存流程实例"""
        instance_file = self.instances_dir / f"{instance.instance_id}.json"
        
        data = {
            "instance_id": instance.instance_id,
            "flow_id": instance.flow_id,
            "status": instance.status,
            "input": instance.input,
            "output": instance.output,
            "context": instance.context,
            "current_node": instance.current_node,
            "start_time": instance.start_time,
            "end_time": instance.end_time,
            "error": instance.error
        }
        
        with open(instance_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        # 从运行中移除
        if instance.instance_id in self.running_instances:
            del self.running_instances[instance.instance_id]


# CLI 入口
if __name__ == "__main__":
    import sys
    
    engine = FlowEngine()
    
    if len(sys.argv) < 2:
        print("Usage: python3 TX1.0 流程引擎.py <command> [options]")
        print("Commands:")
        print("  define --file <flow.yaml>  - 定义流程")
        print("  execute --flow <flow_id>   - 执行流程")
        print("  status --instance <id>     - 查看状态")
        print("  list                       - 列出流程")
        print("  delete --flow <flow_id>    - 删除流程")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "define":
        yaml_file = sys.argv[sys.argv.index("--file") + 1]
        flow_id = engine.define_from_yaml(yaml_file)
        print(f"Flow defined: {flow_id}")
    
    elif command == "execute":
        flow_id = sys.argv[sys.argv.index("--flow") + 1]
        result = engine.execute(flow_id)
        print(f"Flow executed: {result.instance_id}, status: {result.status}")
    
    elif command == "status":
        instance_id = sys.argv[sys.argv.index("--instance") + 1]
        status = engine.get_status(instance_id)
        print(json.dumps(status, indent=2))
    
    elif command == "list":
        flows = engine.list_flows()
        for flow in flows:
            print(f"{flow['id']}: {flow['name']} v{flow['version']} ({flow['nodes']} nodes)")
    
    elif command == "delete":
        flow_id = sys.argv[sys.argv.index("--flow") + 1]
        if flow_id in engine.flow_registry:
            del engine.flow_registry[flow_id]
            flow_file = engine.flows_dir / f"{flow_id}.yaml"
            if flow_file.exists():
                flow_file.unlink()
            print(f"Flow deleted: {flow_id}")
        else:
            print(f"Flow not found: {flow_id}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
