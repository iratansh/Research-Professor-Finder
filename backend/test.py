from query_search import ProfessorSearch
from query_IDsearch import ProfessorQuery

if __name__ == "__main__":
    search = ProfessorSearch()
    ret = search.search(["computer", "science"])
    print(ret)

    db = ProfessorQuery()
    professor = db.get_professor_by_id(300)
    print(professor)
    