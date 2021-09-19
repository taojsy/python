"""
This file is template
Created by jutao on 2020/7/13
E-mail 

"""

from utils import CommonDict
from utils import raise_cBTSError

__all__ = ["template", ]


def template(host, count="3", **args):
	"""This keyword is template.
	*AUTHOR* xx.xxxx@nokia.com  
	
	| Input Parameters | Man. | Description |
	| host             | Yes | ping destination host ip address |
	| count            | No  | ping count |
	| **args           | No  | other ping parameters, should be "size", "tos", "interval", "interface", "ttl" |
	| Return value | object for ping result |    
	
	*RETURN VALUE*
	file content string
	
	Example
	| = | ping_from_VM | 10.1.1.1 | count=3  | size=1000 | count=5 | hop=5 |
	|  log | ${result.loss_rate} |   |   |   |
	|  should be equal | ${result.send_count} | 3 |  |  |
	"""