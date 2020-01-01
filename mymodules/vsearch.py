def search4vowels(phrase: str) -> set:
    """returns the set of vowels found in 'phrase'."""
    return set('aeiou').intersection(set(phrase))

def search4letters(phrase: str, letters: str='aeiou') -> set:
    """returns the set of 'leters' found in 'phrase'."""
    return set(letters).intersection(set(phrase))
