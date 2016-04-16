from textblob import TextBlob

def convertingPluralTosingular(line):
    """singularizes the words in the given line

    str -> list"""
    review= TextBlob(line)
    token=  review.split()
    token= token.singularize()
    return token
