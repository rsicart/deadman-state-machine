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
