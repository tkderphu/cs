# Note about distributed transaction saga pattern

A `Saga` breaks one business action into a sequence of `local transactions` across services.

Each step has:
- a forward action(do)
- a compensation(undo/mitigate if a later step fails)

Two ways to coordinate:
- Orchestration(central controller drives steps): Simpler to reason about, greate for complex flows
- Choreography(pure events; each service reacts): fewer moving parts, but can get spaghetti if the flow grows
