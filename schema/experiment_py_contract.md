# Kontrakt: experiment.py

Każdy plik `experiment.py` musi spełniać poniższe wymagania.

## 1. GeneratedOutputManager

Każdy eksperyment musi zawierać dokładnie jedną linię:

    out = GeneratedOutputManager(__file__)

## 2. match DRAFT

Musi istnieć dokładnie jeden blok `match DRAFT:` z trzema case'ami:

    match DRAFT:
        case DraftLevel.DRAFT_FINAL_VERSION:
            
        case DraftLevel.DRAFT_FOR_HUMAN_TO_VIEW_LATEX:
            
        case DraftLevel.DRAFT_TO_FIX_EXPERIMENT_OR_SEE_IF_IT_COMPILES:
            

Zasady:
- Każdy case ustawia TYLKO zmienne numeryczne N=100 lub Ns=[1,2,3]
- Wszystkie trzy case'y muszą ustawiać TEN SAM zestaw zmiennych.

## 3. tqdm 

Jeśli eksperyment używa progress baru:
- Import: tylko `import tqdm`
- dokładnie jedno `tqdm.tqdm(...)`
- Wymagane argumenty: `desc=`, `colour=`, `unit=`.
- `desc` musi być opisowy i specyficzny dla danego eksperymentu.
- `colour` — hardcoded kolor, NIE losowany.
- `unit` — co reprezentuje jedna iteracja (np. "sketch", "rep").

## 4. get_caption / get_test_caption

Każdy eksperyment musi posiadać funkcję `get_caption` i `get_test_caption`.
Przykładowo:

    def get_caption(m: int, n_reps: int) -> str:
        return rf"""Some caption with $m = {m}$ and {n_reps} trials."""

    def get_test_caption() -> str:
        return get_caption(m=100, n_reps=50)

Zasady:
- `get_caption` przyjmuje parametry potrzebne do zbudowania captiona (nie hardcoduje zmiennych).
- `get_test_caption()` wywołuje `get_caption` z przykładowymi parametrami.
- Caption max 300 znaków
- Caption nie może zawierać `---`.
- Jeśli eksperyment nie potrzebuje captiona: `return r"""NO CAPTION NEEDED"""`

## 5. if __name__ == "__main__"

Każdy eksperyment musi mieć na końcu:

    if __name__ == "__main__":
        main()

## 6. Frontmatter YAML

Początek pliku musi zawierać frontmatter Yaml wedlug schema z `experiment_py_frontmatter_yaml_schema.json`

## 7. DataModel i save_dataclass (gdy istnieje create_figure.py)

Jeśli w katalogu eksperymentu istnieje `create_figure.py`, to `experiment.py` musi:
- Importować: `from data_for_figure_dataclass import DataModel`
- Użyć: `out.save_dataclass(..., DataModel)`

## 8. Output functions

`experiment.py` must NOT use any of: `savefig`, `save_tex`, `save_tex_figure`.

`create_figure.py` must use at least one of: `savefig`, `save_tex`, `save_tex_figure`.

