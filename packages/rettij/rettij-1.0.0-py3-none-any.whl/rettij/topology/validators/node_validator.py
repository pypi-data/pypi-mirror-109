import re
from typing import Dict, List

from rettij.topology.validators.abstract_validator import AbstractValidator
from rettij.exceptions.topology_exception import TopologyException
from rettij.topology.network_components.node import Node


class NodeValidator(AbstractValidator):
    """
    Validator class for the nodes in the topology.
    """

    def __init__(self, topology: Dict, topology_file_path: str) -> None:
        """
        Initialize a NodeValidator object for the supplied topology.

        :param topology: The topology to validate.
        :param topology_file_path: Path to the topology file.
        """
        super().__init__(topology, topology_file_path)

        # stores the declared nodes and maps them to the line numbers that they are defined in
        self.declared_nodes: Dict[str, List[int]] = {}
        self._store_declared_nodes()

    def validate(self) -> None:
        """
        Validate the nodes in the topology.

        Checks for:
        - Node name length
        - Node name pattern correctness
        - Duplicate node names
        - Duplicate interface names in a node

        :raises: TopologyException
        """
        self._check_node_id_length()
        self._check_node_name_validity()
        self._check_for_duplicate_node_ids()
        self._check_for_duplicate_interface_names()

    def _store_declared_nodes(self) -> None:
        """
        Parse data and store the declared nodes and the lines they are declared in the declared_nodes dictionary.

        :raises: TopologyException
        """
        if self.topology.get("nodes"):
            for node in self.topology.get("nodes", []):
                node_id: str = node.get("id")
                line: int = node.get("__line__")
                if node_id not in self.declared_nodes:
                    self.declared_nodes[node_id] = [line]
                else:
                    self.declared_nodes[node_id].append(line)
        else:
            raise TopologyException(
                TopologyException.NODE_VALIDATION_FAILED, self.topology_file_path, message="No nodes declared."
            )

    def _check_node_id_length(self) -> None:
        """
        Check if a node exceeds the maximum node-id length.

        :raises: TopologyException
        """
        for node_id, line in self.declared_nodes.items():
            if len(node_id) > Node.get_name_max_length():
                raise TopologyException(
                    TopologyException.NODE_VALIDATION_FAILED,
                    self.topology_file_path,
                    message=f"Node id '{node_id}' exceeds maximum id length of {Node.get_name_max_length()}. See line {line} in {self.topology_file_path}.",
                )

    def _check_node_name_validity(self) -> None:
        """
        Check if a node exceeds the maximum node-id length.

        :raises: TopologyException
        """
        # Pattern background: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#dns-label-names
        # Some resource types require their names to follow the DNS label standard as defined in RFC 1123. This means the name must:
        #     contain at most 63 characters
        #     contain only lowercase alphanumeric characters or '-'
        #     start with an alphanumeric character
        #     end with an alphanumeric character
        pattern_str: str = r"^[a-z0-9]([-a-z0-9]{0,61}[a-z0-9])?$"

        # Create and compile the pattern once since it is a computation heavy process.
        pattern: re.Pattern = re.compile(pattern_str)

        for node_id, line in self.declared_nodes.items():
            if not re.match(pattern, node_id):
                raise TopologyException(
                    TopologyException.NODE_VALIDATION_FAILED,
                    self.topology_file_path,
                    message=f"Node id '{node_id}' is not a valid DNS Label Name (must consist of lower case alphanumeric characters and '-', and must start and end with an alphanumeric character). See line {line} in {self.topology_file_path}.",
                )

    def _check_for_duplicate_node_ids(self) -> None:
        """
        Ensure that node ids are unique.

        :raises: TopologyException
        """
        for node_name, lines in self.declared_nodes.items():
            if len(lines) > 1:
                raise TopologyException(
                    TopologyException.NODE_VALIDATION_FAILED,
                    self.topology_file_path,
                    message=f"Node {node_name} is declared {len(lines)} times. See lines {str(lines)} in {self.topology_file_path}.",
                )

    def _check_for_duplicate_interface_names(self) -> None:
        """
        Ensure that interface names on each node are unique.

        :raises: TopologyException
        """
        for node in self.topology.get("nodes", []):
            current_node_id: str = node.get("id")
            used_interface_names: List[str] = []
            if node.get("interfaces"):
                for interface in node.get("interfaces"):
                    interface_name: str = interface.get("id")
                    line: int = interface.get("__line__")
                    if interface_name not in used_interface_names:
                        used_interface_names.append(interface_name)
                    else:
                        raise TopologyException(
                            TopologyException.NODE_VALIDATION_FAILED,
                            self.topology_file_path,
                            message=f"Interface {interface_name} of node {current_node_id} is declared multiple times. See line {line} in {self.topology_file_path}.",
                        )
