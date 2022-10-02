from flask import request

# Number question for each page
QUESTIONS_PER_PAGE = 10

# Mehtod for number of question to be paginated at each page
def question_pagination(request,selection):
    page = request.args.get('page', 1, type=int)
    paginated_questions = [question.format() for question in selection]
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    current_paginate = paginated_questions[start:end]
    return current_paginate


# Method for the category page history
def category_history(request,page,current_paginate):
    if current_paginate < page:
        next_page = request.args.get('page', 1, type=int) + 1
        return str(request.url_root + 'questions?page=') + str(next_page)
    else:
        return str(request.url_root + 'questions?page=1')



