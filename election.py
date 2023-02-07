import time

# Enum pour définir l'état d'un nœud
class NodeState:
    IDLE = 0
    REQUEST = 1
    LEADER = 2

# Classe représentant un nœud
class Node:
    def __init__(self, id, network):
        self.id = id
        self.state = NodeState.IDLE
        self.network = network
        self.leader_id = None

    def start_election(self):
        # Envoie une demande de contrôle au coordinateur actuel
        self.state = NodeState.REQUEST
        self.network.send_request(self.id)

    def receive_request(self, sender_id):
        # Si le nœud reçoit une demande de contrôle
        if self.state == NodeState.IDLE:
            # Envoie une demande de contrôle avec un ID supérieur
            self.start_election()
        elif self.state == NodeState.REQUEST:
            # Mettre à jour la liste des demandeurs
            self.network.update_request_list(sender_id)

    def receive_leader(self, leader_id):
        # Mettre à jour le leader actuel
        self.leader_id = leader_id
        self.state = NodeState.IDLE
        
# Classe représentant le réseau de nœuds
class Network:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.nodes = [Node(i, self) for i in range(num_nodes)]
        self.request_list = []

    def send_request(self, sender_id):
        for node in self.nodes:
            if node.id != sender_id:
                node.receive_request(sender_id)

    def update_request_list(self, sender_id):
        self.request_list.append(sender_id)
        if len(self.request_list) == self.num_nodes - 1:
            # Tous les nœuds ont reçu la demande
            # Déterminer le nœud avec l'ID le plus élevé
            leader_id = max(self.request_list)
            for node in self.nodes:
                node.receive_leader(leader_id)

# Exemple d'utilisation
if __name__ == "__main__":
    network = Network(5)
    node = network.nodes[0]
    node.start_election()
    time.sleep(10) # Simulation d'un temps de convergence
    print("Le leader actuel est le nœud", node.leader_id)
