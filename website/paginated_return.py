def paginated_return(result_list, page: int):
    li = {
        result_list.pages
    }
    for i in range(1, 6):
        if result_list.pages >= i:
            li.add(i)
    for extra in (result_list.pages - 2, result_list.pages - 1):
        if extra > 0:
            li.add(extra)
    li.add(page)
    if page > 1:
        li.add(page - 1)
    if page < result_list.pages:
        li.add(page + 1)
    li = list(li)
    li.sort()
    new_li = []
    prev = 0
    for i in li:
        if i != (prev + 1):
            new_li.append("..")
        new_li.append(i)
        prev = i
    return new_li