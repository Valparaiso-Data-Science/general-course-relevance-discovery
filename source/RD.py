def findRelevant(classes):
    """
    @terry
    There are a good number of data science words that should be but are not in bok.txt.
    If you want to browse through the file and add words you think are data-y, please do so
    I know a lot of statistics words are not in there like goodness of fit
    
    You can also look into figuring out multiple versions and tenses of certain words
    whether you do that manually, or Karl mentioned that it's possible to do that using some python package
    
    Also you may want to make this function titled something like "find keywords" 
    and move the getting of the keywords from bok.txt to main
    """
    bagWords = open("../bok.txt").read().splitlines()
    result = {}

    for classID,desc in classes.items():
        for relevantTerm in bagWords:
            if relevantTerm in desc:
                desc = desc.replace(relevantTerm,"*" + relevantTerm + "*")
                result[classID] = desc
    return result
