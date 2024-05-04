import requests
from .models import Node
from .serializers import BlockSerializer

def propagate(block):
  block_data = BlockSerializer(instance=block).data
  nodes = Node.objects.all().values_list("address")
  for address in node:
    response = response.post(url=f'{address}recieve-block/', data=block_data)