# deadman-state-machine

Deadman State Machine can be used to manage state workflows in an alerting system.

It implements the State design pattern:

https://sourcemaking.com/design_patterns/state


State machine:

```
       start
          |   --------
          |   |      |
          v   v      | last_ping < timeout
       ----------    |
   --->| Active |-----
   |   ----------
   |      |
   |      | last_ping > timeout
   |      |
   |      v
   |   ----------
   |   | Dead   |
   |   ----------
   |      |
   |      | last_ping < timeout
   |      |
   |      v
   |   -----------------
   ----| Ressurrection |
       -----------------
```

Launch unit tests:

```
python3 -m unittest
```


To install this package using pip, add the following line in your `requirements.txt` file:

```
-e git+https://github.com/rsicart/deadman-state-machine.git@master#egg=deadman_state_machine
```

Replace master by a tag or commit if needed.

