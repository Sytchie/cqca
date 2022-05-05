from model.gates import Identity

def create_gate_list(n, coeff=1, gate=Identity):
    gates = []

    for i in range(n):
        gates.append(gate(coeff))

    return gates

def print_list(elements):
        res = ""
        
        for element in elements:
            res += str(element) + "\t"
        
        print(res[: -1])
