import pyrtl

if __name__ == "__main__":
    enable = pyrtl.Input(1, "enable")
    reset = pyrtl.Input(1, "reset")
    y = pyrtl.Register(2, "y")

    # reset = 1 -> 0 (enable ignored); else enable = 1 -> y + 1; else y unchanged
    y.next <<= pyrtl.select(reset, 0, pyrtl.select(enable, (y + 1)[:2], y))

    trace = pyrtl.SimulationTrace()
    sim = pyrtl.Simulation(tracer=trace)

    # (reset, enable) for each clock cycle
    steps = [
        (1, 0),                          # reset
        (0, 1), (0, 1), (0, 1), (0, 1),  # count up: 1, 2, 3, wraps to 0
        (0, 1),
        (0, 0), (0, 0),                  # enable off: y holds
        (1, 1),                          # reset wins even though enable = 1
        (0, 1), (0, 1),                  # count again from 0
        (0, 0),
    ]

    model = 0  # what y should be at the start of the next cycle
    for r, e in steps:
        sim.step({"reset": r, "enable": e})
        assert sim.inspect("y") == model, f"reset={r} enable={e}: y={sim.inspect('y')}, expected {model}"
        if r:
            model = 0
        elif e:
            model = (model + 1) % 4

    print("All tests passed!")
    trace.render_trace()
