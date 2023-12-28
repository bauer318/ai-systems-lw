from qaSystem.tag_dictionary import TagDictionary


class Request:
    show: bool = False
    color: str = None
    type: str = None
    min_weight: float = None
    max_weight: float = None
    number: str = "One"
    tags: TagDictionary
    exist: bool = False
    extr: str = None
    and_log: bool = False
    or_log: bool = False

    def to_str(self):
        print(
            f'show: {self.show}\n'
            f'number: {self.number}\n'
            f'color: {self.color}\n'
            f'type: {self.type}\n'
            f'min weight: {self.min_weight}\n'
            f'max weight: {self.max_weight}\n'
            f'exist: {self.exist}\n'
            f'extr: {self.extr}\n'
            f'and_log: {self.and_log}\n'
            f'or_log: {self.or_log}\n'
            f'tags :{str(self.tags)}'
        )
