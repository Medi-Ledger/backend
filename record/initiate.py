import requests
from .models import Node

class InitiationManager:
    ORIGIN_NODE = "https://mediledger.onrender.com"

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.verbose = False
        self.retry_limit = 3

    def set_verbose(self, verbose=True):
        self.verbose = verbose

    def set_retry_limit(self, limit):
        self.retry_limit = limit

    def authenticate(self):
        if self.api_key:
            # Perform authentication logic here
            if self.verbose:
                print("Authentication successful.")
            return True
        else:
            if self.verbose:
                print("No API key provided. Authentication failed.")
            return False

    def get_nodes(self, address=ORIGIN_NODE):
        response = requests.get(f"{address}/new-node/")
        
        if response.status_code == 200:
            urls = response.json().get('urls', [])
    
            for url in urls:
                node = Node(address=url)
                node.save()
            return len(urls)
        else:
            print(f"Failed to fetch URLs. Status code: {response.status_code}")
            return None

    def get_next_nodes(self):
        nodes = Node.objects.all().values_list("address", flat=True)
        for address in nodes:
            self.get_nodes(address=address)

    def run_initiation_process(self):
        if self.authenticate():
            if self.verbose:
                print("Initiation process started.")
            for _ in range(self.retry_limit):
                self.get_next_nodes()
            if self.verbose:
                print("Initiation process completed.")
        else:
            if self.verbose:
                print("Initiation process aborted due to authentication failure.")




