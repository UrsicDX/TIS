#!/usr/bin/python3

from pathlib import Path
import sys
from timeit import default_timer as timer
import json
from naloga1 import naloga1


def test_naloga1(case_dir, case_id):
    """
    Funkcija za preverjanje naloge 1.
    Primer uporabe kot uvožen modul:
    from test_naloga1 import test_naloga1
    test_naloga1('primeri', 1)
    """
    # Zahtevana natančnost izračunov
    tol = 1e-3
    # Zahtevana časovna omejitev (s)
    t_max = 30

    # Naložimo vhodne podatke in rešitev
    base_path = Path(__file__).parent
    file_path = base_path / case_dir / (str(case_id) + '.json')
    json_file = open(file_path, 'r', encoding='utf8')
    data = json.load(json_file, strict=False)

    # Poženemo rešitev domače naloge in izmerimo izvajalni čas
    start = timer()
    H = naloga1(data['besedilo'], data['p'])
    end = timer()
    t_elapsed = end - start

    # Ovrednotimo rešitev
    if H is None:
        H = float("nan")
    # Pretvorimo za vsak primer, npr. če je rešitev niz
    H = float(H)
    success = int(abs(H - data['H']) < tol)

    # Izpišemo rezultat
    print("-"*72)
    print(f"Rezultat za primer {case_id}: {success} točk")
    if success != 1:
        print(f" -> Izračunani H: {H:.4f}    ✗")
        print(f" -> Pravi H:      {float(data['H']):.4f} ✓")
    print(f"Čas izvajanja: {t_elapsed:.1f} s")
    if t_elapsed > t_max:
        print(
            f" -> Čas izvajanja je daljši od {t_max:.1f} sekund! Razmislite o optimizaciji kode.")


def main(case_dir="primeri", case_id=None, *other):
    """
    Datoteko test_naloga1.py lahko poženemo kot program s podanimi vhodnimi argumenti:
    Primeri uporabe:
        V mapi "primeri" poženemo 1. primer (1.json):
        python test_naloga1.py primeri 1

        V mapi "primeri" poženemo vse tri primere:
        python test_naloga1.py primeri

        V mapi s privzetim imenom "primeri" poženemo vse tri primere:
        python test_naloga1.py
    """

    # Preverimo morebitne odvečne argumente ukazne vrstice (pospravljeni so v other)
    if other:
        print(("Napačno število argumentov! Podali ste {} preveč.\n"
               "Zagon:  python test_naloga1.py [mapa_s_primeri] [stevilka_primera]\n"
               "Primer: python test_naloga1.py primeri 2").format(len(other)))
        exit()

    # Poženemo za vse primere;
    # v primeru določenega case_id, upoštevamo le-tega
    if not case_id:
        [test_naloga1(case_dir, case_id=i) for i in range(1, 20)]
    else:
        test_naloga1(case_dir, case_id)


if __name__ == "__main__":
    # Argumenti ukazne vrstice so v sys.argv
    main(*sys.argv[1:])
