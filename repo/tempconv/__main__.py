import sys
from tempconv.ops import c_to_f, f_to_c

if __name__ == "__main__":
    _, op, v = sys.argv
    fn = c_to_f if op == "c2f" else f_to_c
    print(int(fn(float(v))))
