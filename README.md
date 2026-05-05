Smart Kitchen Inventory & Predictive Replenishment System
1. Overview

This system is designed to eliminate human error in kitchen management by automating the inventory tracking and ordering process. By utilizing real-time weight data and historical consumption patterns, the system ensures that a kitchen never runs out of essential ingredients while simultaneously minimizing food waste.
2. The Core Concept: "The Predictive Brain"

The system operates on a feedback loop. It doesn't just look at what is missing; it learns from the past to predict the future. It treats the kitchen as a dynamic environment where variables (like customer volume or supplier speed) are constantly changing.
Key Components:

    Mass-Based Tracking: Ingredients are placed on specialized scales. The system receives a constant stream of weight data, identifying exactly how much of a specific product (e.g., Salmon, Rice, Avocado) is left in real-time.

    Dynamic Coefficient Logic: Instead of a static "reorder point," the system uses a variable coefficient.

        If the kitchen ends the week with too much leftover (Waste), the coefficient decreases.

        If the kitchen runs out before the next delivery (Shortage), the coefficient increases.

    Latency Compensation: The system factors in "Lead Time"—the delay between placing an order and the physical arrival of the goods. It triggers orders early enough to cover the consumption expected during that delivery window.

3. Optimization Goal

The primary objective of the algorithm is a Minimal Residual Average. Over a three-month rolling window, the system adjusts its ordering patterns until the amount of remaining stock (at the moment of the next delivery) is as close to the safety buffer as possible, without ever hitting zero.
4. Operational Flow

    Sensing: Scales transmit current ingredient weights in a simplified data format.

    Processing: The "Brain" compares current weight against predicted needs for the next delivery cycle.

    Refining: The system checks the "Waste Log." If items were discarded, the ordering logic is penalized to prevent over-ordering in the future.

    Execution: When the "Safety Threshold" is breached (considering delivery latency), the system autonomously generates a replenishment request to the supply center.


Install:
for the db initialization, run models.py after activating the virtual env (later to be dockerized).