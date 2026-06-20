# Kontrakt: create_figure.py

Każdy plik `create_figure.py` musi spełniać poniższe wymagania.

## 1. GeneratedOutputManager

Musi zawierać dokładnie jedną linię:

    out = GeneratedOutputManager(__file__)

## 2. DataModel i load_dataclass

Musi importować DataModel i załadować dane:

    from data_for_figure_dataclass import DataModel

    data: DataModel = out.load_dataclass(DataModel)

## 3. Brak match DRAFT

`create_figure.py` NIE może zawierać bloku `match DRAFT:`.
Parametry jakościowe (repetitions, stream sizes) należą wyłącznie do `experiment.py`.

## 4. get_caption / get_test_caption

Musi posiadać funkcje `get_caption` i `get_test_caption` (te same zasady co w `experiment_py_contract.md`).

## 5. if __name__ == "__main__"

Musi mieć na końcu:

    if __name__ == "__main__":
        main()
