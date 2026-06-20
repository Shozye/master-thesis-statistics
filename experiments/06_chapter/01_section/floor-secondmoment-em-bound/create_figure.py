from data_for_figure_dataclass import DataModel
from generated_output_manager import GeneratedOutputManager

FIGURE_KEY = "floor-secondmoment-em-bound"


def get_caption() -> str:
    return r"""NO CAPTION NEEDED"""


def get_test_caption() -> str:
    return get_caption()


def main() -> None:
    out = GeneratedOutputManager(__file__)
    data = out.load_dataclass(DataModel)
    out.save_text(data.bound_tex, FIGURE_KEY + ".tex")


if __name__ == "__main__":
    main()
