import pyrtl

def datapath(zero, lt, opcode):
    # opcode: 00 = blt, 01 = bge, 10 = beq, 11 = bne
    branch = pyrtl.mux(opcode, lt, ~lt, zero, ~zero)
    return branch

if __name__ == "__main__":
    zero = pyrtl.Input(1, "zero")
    lt = pyrtl.Input(1, "lt")
    opcode = pyrtl.Input(2, "opcode")

    branch_out = datapath(zero, lt, opcode)

    branch = pyrtl.Output(1, "branch")
    branch <<= branch_out

    sim = pyrtl.Simulation()

    # Example test case below, this should PASS
    try:
        sim.step({"zero" : 0, "lt" : 1, "opcode": 0})
        assert sim.inspect("branch") == 1
        print("Test PASS")
    except:
        print("Test FAIL")

    # Exhaustive tests: every opcode with every zero/lt combination.
    expected = {
        0: lambda z, l: l,        # blt: branch if lt
        1: lambda z, l: 1 - l,    # bge: branch if NOT lt
        2: lambda z, l: z,        # beq: branch if zero
        3: lambda z, l: 1 - z,    # bne: branch if NOT zero
    }
    names = {0: "blt", 1: "bge", 2: "beq", 3: "bne"}

    for op in range(4):
        for z in (0, 1):
            for l in (0, 1):
                sim.step({"zero": z, "lt": l, "opcode": op})
                got = sim.inspect("branch")
                want = expected[op](z, l)
                assert got == want, f"{names[op]} zero={z} lt={l}: got {got}, expected {want}"

    print("All tests passed!")
