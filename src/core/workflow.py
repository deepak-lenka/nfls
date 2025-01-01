from typing import Dict, List, Callable
from datetime import datetime
import networkx as nx

class WorkflowNode:
    """Represents a node in the workflow DAG"""
    
    def __init__(self, name: str, task_func: Callable, dependencies: List[str] = None):
        self.name = name
        self.task_func = task_func
        self.dependencies = dependencies or []
        self.result = None
        self.status = 'pending'  # pending, running, completed, failed
        self.error = None
        self.start_time = None
        self.end_time = None
        
    def execute(self, input_data: Dict = None) -> Dict:
        """Execute the node's task"""
        try:
            self.status = 'running'
            self.start_time = datetime.now()
            
            # Execute task with input data
            self.result = self.task_func(input_data)
            
            self.status = 'completed'
            self.end_time = datetime.now()
            return self.result
            
        except Exception as e:
            self.status = 'failed'
            self.error = str(e)
            self.end_time = datetime.now()
            raise

class WorkflowDAG:
    """Manages the workflow DAG for NFL analysis"""
    
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes: Dict[str, WorkflowNode] = {}
        
    def add_node(self, name: str, task_func: Callable, dependencies: List[str] = None):
        """Add a node to the workflow"""
        if name in self.nodes:
            raise ValueError(f"Node {name} already exists")
            
        node = WorkflowNode(name, task_func, dependencies)
        self.nodes[name] = node
        
        # Add node to graph
        self.graph.add_node(name)
        
        # Add dependencies
        if dependencies:
            for dep in dependencies:
                if dep not in self.nodes:
                    raise ValueError(f"Dependency {dep} not found")
                self.graph.add_edge(dep, name)
                
        # Verify no cycles
        if not nx.is_directed_acyclic_graph(self.graph):
            self.graph.remove_node(name)
            del self.nodes[name]
            raise ValueError("Adding this node would create a cycle")
            
    def get_node_status(self, name: str) -> Dict:
        """Get status of a node"""
        node = self.nodes.get(name)
        if not node:
            raise ValueError(f"Node {name} not found")
            
        return {
            'name': node.name,
            'status': node.status,
            'error': node.error,
            'start_time': node.start_time,
            'end_time': node.end_time,
            'duration': (node.end_time - node.start_time).total_seconds() if node.end_time else None
        }
        
    def get_ready_nodes(self) -> List[str]:
        """Get nodes that are ready to execute"""
        ready_nodes = []
        
        for name, node in self.nodes.items():
            if node.status != 'pending':
                continue
                
            # Check if all dependencies are completed
            deps_completed = all(
                self.nodes[dep].status == 'completed'
                for dep in node.dependencies
            )
            
            if deps_completed:
                ready_nodes.append(name)
                
        return ready_nodes
        
    def execute_node(self, name: str, input_data: Dict = None) -> Dict:
        """Execute a specific node"""
        node = self.nodes.get(name)
        if not node:
            raise ValueError(f"Node {name} not found")
            
        # Verify dependencies are completed
        for dep in node.dependencies:
            dep_node = self.nodes[dep]
            if dep_node.status != 'completed':
                raise ValueError(f"Dependency {dep} not completed")
                
        # Execute node
        return node.execute(input_data)
        
    def execute_workflow(self, initial_data: Dict = None) -> Dict:
        """Execute the entire workflow"""
        # Verify DAG is valid
        if not nx.is_directed_acyclic_graph(self.graph):
            raise ValueError("Invalid DAG: contains cycles")
            
        # Get execution order
        execution_order = list(nx.topological_sort(self.graph))
        
        # Execute nodes in order
        results = {}
        current_data = initial_data or {}
        
        for node_name in execution_order:
            node = self.nodes[node_name]
            
            # Prepare input data
            node_input = {
                'workflow_data': current_data,
                'dependency_results': {
                    dep: self.nodes[dep].result
                    for dep in node.dependencies
                }
            }
            
            # Execute node
            node_result = self.execute_node(node_name, node_input)
            results[node_name] = node_result
            
            # Update current data
            if isinstance(node_result, dict):
                current_data.update(node_result)
                
        return results
        
    def get_workflow_status(self) -> Dict:
        """Get status of the entire workflow"""
        total_nodes = len(self.nodes)
        completed = sum(1 for node in self.nodes.values() if node.status == 'completed')
        failed = sum(1 for node in self.nodes.values() if node.status == 'failed')
        pending = sum(1 for node in self.nodes.values() if node.status == 'pending')
        running = sum(1 for node in self.nodes.values() if node.status == 'running')
        
        # Calculate start and end times
        start_times = [
            node.start_time for node in self.nodes.values()
            if node.start_time is not None
        ]
        end_times = [
            node.end_time for node in self.nodes.values()
            if node.end_time is not None
        ]
        
        workflow_start = min(start_times) if start_times else None
        workflow_end = max(end_times) if end_times else None
        
        return {
            'total_nodes': total_nodes,
            'completed': completed,
            'failed': failed,
            'pending': pending,
            'running': running,
            'start_time': workflow_start,
            'end_time': workflow_end,
            'duration': (workflow_end - workflow_start).total_seconds() if workflow_end else None,
            'status': 'completed' if completed == total_nodes else 'failed' if failed > 0 else 'running' if running > 0 else 'pending'
        }
