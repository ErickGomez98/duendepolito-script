def getInputValue(text, inputName):
    initialIndex = text.find(f'name="{inputName}"')
    i = initialIndex
    firstIndex = 0
    while True:
        if(text[i] == '<'):
            firstIndex = i
            break
        i = i - 1
    lastIndex = 0

    i = initialIndex
    while True:
        if(text[i] == '>'):
            lastIndex = i
            break
        i = i + 1

    token_str = text[firstIndex:lastIndex]
    tmpIndex1 = token_str.find('value="')
    tmpLastIndex = 0
    j = tmpIndex1 + len('value="')
    while True:
        if(token_str[j] == '"'):
            tmpLastIndex = i
            break

        if(j >= len(token_str)):
            break
        j = j + 1

    final_str = token_str[tmpIndex1+len(
        'value="'):tmpLastIndex]
    final_str = final_str[:-1]
    return final_str


def getUrlValue(text, className):
    initialIndex = text.find(f'class="{className}"')
    i = initialIndex
    firstIndex = 0
    while True:
        if(text[i] == '<'):
            firstIndex = i
            break
        i = i - 1
    lastIndex = 0

    i = initialIndex
    while True:
        if(text[i] == '>'):
            lastIndex = i
            break
        i = i + 1

    token_str = text[firstIndex:lastIndex]
    tmpIndex1 = token_str.find('href="')
    tmpLastIndex = 0
    j = tmpIndex1 + len('href="')
    while True:
        if(token_str[j] == '"'):
            tmpLastIndex = i
            break

        if(j >= len(token_str)):
            break
        j = j + 1

    final_str = token_str[tmpIndex1+len(
        'href="'):tmpLastIndex]
    final_str = final_str[:-1]
    return final_str
