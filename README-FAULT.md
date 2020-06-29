
# Robot-Shop

A `manual` fault injection approach to produce distributed traces.

## Fault Types

* WAEP: Wrong arithmetic expression in parameter of function call.

* WPFV: Wrong variable used in parameter of function call.

* WPFL: Wrong value used in parameter of function call.

* WRV: Wrong return value.

## Faults

TODO: What are the `best` faults to inject in fine-grained components? (Check those bellow)

### Path misconfiguration

A fault represented by a miss configured path from microservice A to B, where microservice A uses a wrong path.

```bash
# Fault-free
path = 'http://{abc}:{port}/resource'
call(path)

# Wrong path
path = 'http://{abd}:{port}/resource'
call(path)
```

### Request Retry

```bash
# Fault-free
1 (Web) --> 2 (Payment) --> 3 (Users)
                        --> 4 (Cart)

# Fault (Request Retry)
1 (Web) --> 2 (Payment) --> 3 (Users) 2x (1 fault & 1 OK?)
                        --> 4 (Cart)
```

### 

## Authors

```bash
apbento@dei.uc.pt
jaimec@dei.uc.pt
```
