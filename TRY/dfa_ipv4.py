import sys

DIGITS = "0123456789"
DEAD = "DEAD"
TITIK = "."

def build_dfa():
    delta = {}
    states = {DEAD}

    for k in range(1, 5):
        S, Z, A, B, C, D, E = (f"{n}{k}" for n in "SZABCDE")
        states.update([S, Z, A, B, C, D, E])

        for ch in DIGITS:
            if ch == "0":
                delta[(S, ch)] = Z
            elif ch == "1":
                delta[(S, ch)] = A
            elif ch == "2":
                delta[(S, ch)] = B
            else:
                delta[(S, ch)] = C

        for ch in DIGITS:
            delta[(A, ch)] = D
            delta[(C, ch)] = Z
            delta[(D, ch)] = Z
            delta[(Z, ch)] = DEAD

            if ch in "01234":
                delta[(B, ch)] = D
            elif ch == "5":
                delta[(B, ch)] = E
            else:
                delta[(B, ch)] = Z

            delta[(E, ch)] = Z if ch in "012345" else DEAD

        if k < 4:
            nxt = f"S{k + 1}"
            for st in (A, B, C, D, E, Z):
                delta[(st, TITIK)] = nxt

    start = "S1"
    accept = {f"{n}4" for n in "ZABCDE"}
    alphabet = set(DIGITS) | {TITIK}
    return states, alphabet, delta, start, accept

STATES, ALPHABET, DELTA, START, ACCEPT = build_dfa()

def step(state, ch):
    return DELTA.get((state, ch), DEAD)

def run_dfa(text):
    state = START

    for i, ch in enumerate(text, start=1):
        state = step(state, ch)
        if state == DEAD:
            if ch not in ALPHABET:
                alasan = f"simbol '{ch}' di posisi {i} tidak ada dalam alfabet DFA"
            else:
                alasan = f"karakter '{ch}' di posisi {i} melanggar aturan IPv4"
            return False, state, alasan

    if state in ACCEPT:
        return True, state, "string berakhir di final state"

    if text == "":
        alasan = "input kosong"
    else:
        alasan = f"string berakhir di state {state} (bukan final state): oktet belum lengkap"
    return False, state, alasan

def tampilkan_hasil(text):
    diterima, akhir, alasan = run_dfa(text)
    print(f"\nInput : '{text}'")
    print(f"State akhir : {akhir}")
    print(f"Status      : {'VALID (ACCEPT)' if diterima else 'TIDAK VALID (REJECT)'}")
    print(f"Keterangan  : {alasan}")

def cetak_tabel_transisi():
    urutan = []
    for k in range(1, 5):
        urutan += [f"{n}{k}" for n in "SZABCDE"]
    urutan.append(DEAD)

    simbol = list(DIGITS) + [TITIK]
    print("\nTabel Transisi DFA IPv4  (-> = start, * = final)")
    header = f"{'State':<8}" + "".join(f"{s:^6}" for s in simbol)
    print(header)
    print("-" * len(header))
    for st in urutan:
        tanda = ("->" if st == START else "  ") + ("*" if st in ACCEPT else " ")
        baris = f"{tanda}{st:<5}" + "".join(
            f"{step(st, s):^6}" for s in simbol
        )
        print(baris)

def main():
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            tampilkan_hasil(arg)
        return

    while True:
        try:
            teks = input("\nMasukkan IPv4 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSampai jumpa!")
            break

        perintah = teks.lower()
        if perintah in ("keluar", "exit", "quit", "q"):
            print("Sampai jumpa!")
            break
        elif perintah == "tabel":
            cetak_tabel_transisi()
        else:
            tampilkan_hasil(teks)

if __name__ == "__main__":
    main()