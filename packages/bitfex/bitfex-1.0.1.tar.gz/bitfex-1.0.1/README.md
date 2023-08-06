# BitFex-API.py

BitFex.trade trading API python library.

## Installation

```
pip install bitfex
```

## Usage Examples

```python
from bitfex_api import Api

client = Api(token='4320dbf5-3df1-483d-a155-1fc860c4a14d')

client.user().response
# ApiResponse(
#   success=True,
#   response={'username': 'client', 'balances': {'BTC': 0.985e-05, 'RUR': 0.0, ..., 'DOGE': 0.0}},
#   error=None
# )

client.orders_my()
# ApiResponse(
#   success=True,
#   response={'orders': [
#     {'id': 1, 'pair': 'KWH_ETH', 'amount': 10000.0, 'price': 1.2e-07, 'operation': 'sell', 'completed': False, 'updated': 1563824693000, 'user_id': 'xx12'},
#     ...
#   ]}
# )

client.orders('BTC_RUR')
# ApiResponse(
#   success=True,
#   response={'orders': [
#     {'id': 11256624, 'pair': 'BTC_RUR', 'amount': 2.597e-05, 'price': 640988.03, 'operation': 'buy', 'completed': True, 'updated': 1563995215000, 'user_id': 'YZ'},
#     ...
#   ]}
# )

client.create_order(pair='BTC_RUR', operation='buy', amount=0.01, price=600000.0)
# ApiResponse(success = True) # fully completed
# ApiResponse(success = True, response = {'order_id': 1}) # not fully completed

client.cancel_order(order_id=1)
# ApiResponse(success = True)
```

## License

MIT