from Document.models import Documents

def get_recommendations(results_ind):
    '''
    This function is used to get recommendations based on the results of a search.
    The recommendations are based on the authors and genres of the documents in the results.

    Args
        - results_ind: list of integers, the indices of the documents in the results

    Returns
        - list of integers, the indices of the recommended documents
        - list of strings, the authors of the recommended documents
        - list of strings, the genres of the recommended documents
    '''

    all_docs = Documents.objects.all()
    authors = dict()
    genres = dict()
    possible_rec = []

    for i in all_docs:
        if i.id in results_ind:
            authors[i.author] = authors.get(i.author, 0) + 1
            for j in i.genres.split(", "):
                genres[j] = genres.get(j, 0) + 1
        else:
            possible_rec.append(i)

    authors_ = sorted(authors.items(), key=lambda x: x[1], reverse=True)
    authors = [i[0] for i in authors_ if i[1] >= 1][: 10 if len(authors) > 10 else len(authors)]

    genres_ = sorted(genres.items(), key=lambda x: x[1], reverse=True)
    genres = [i[0] for i in genres_ if i[1] >= 1][: len(authors) if len(genres) > len(authors) else len(genres)]

    rec = {}
    for i in possible_rec:
        if i.author in authors:
            #rec[i] is the count of the number of times the author appears in the results
            rec[i] = authors_[authors.index(i.author)][1]
        for j in i.genres.split(", "):
            if j in genres:
                rec[i] = rec.get(i, 0) + genres_[genres.index(j)][1]

    rec = sorted(rec.items(), key=lambda x: x[1], reverse=True)
    rec = [i[0] for i in rec]

    if len(rec) > 100:
        rec = rec[:100]

    return rec, authors, genres