def load_word(path: str) -> list[list[int]]:
    with open(path, 'r') as f:
        lines = f.read().split('\n')
        word = [list(map(int, list(i))) for i in lines]
        return word
