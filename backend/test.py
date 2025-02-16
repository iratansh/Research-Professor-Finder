from backend.query_search import ProfessorSearch

if __name__ == "__main__":
    search = ProfessorSearch()
    ret = search.search(["computer", "science"])
    print(ret)

    