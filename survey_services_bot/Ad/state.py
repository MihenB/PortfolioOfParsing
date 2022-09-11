import pickle
from typing import Generator


class CurrentCondition:
    def __init__(self):
        # Vars for current session
        self.current_header = None
        self.current_value = None
        self.is_header = None

        self.services_dict = self.get_service_dict()
        self.stream = self.stream_generator()

    @staticmethod
    def get_service_dict() -> dict:
        with open('service_dict.pkl', 'rb') as file:
            return pickle.load(file)

    def stream_generator(self) -> Generator:
        # Generator for travestying all values from initial dictionary
        for group_name in self.services_dict.keys():
            yield group_name, True
            for service_name in self.services_dict[group_name]:
                yield service_name, False

    def next_stream_elem(self) -> None:
        self.current_value, self.is_header = next(self.stream, (None, None))
        self.current_header = self.current_value if self.is_header else self.current_header

    def get_cur_val_and_head_mark(self) -> tuple[str, bool]:
        return self.current_value, self.is_header

    def get_cur_val(self):
        return self.current_value

    def get_cur_header(self):
        return self.current_header


def main():
    from pprint import pprint

    st = CurrentCondition()
    pprint(st.get_service_dict())


if __name__ == '__main__':
    main()
