import sqlite3
import numpy as np
import pandas as pd

def verify_answer(answer_index, answer_name = None):
    if ('submission_data' not in globals() or 'checker_str' not in globals()):
        print('Login required')
        print('Please make sure you have run the first cell above')
        return

    if ('email' not in submission_data):
        print('Login required')
        print('Please submit your email')
        return

    if (answer_name not in globals()):
        print('The answer is not defined. Make sure you have run the cell first.')
        return
    answer = globals()[answer_name]
    if (not isinstance(answer, (str))):
        print("Your answer should be a string. Please define it as a string")
        return

    print("Your answer is:")
    print(answer)

    question = assignment.questions[answer_index]
    solution = question['solution']
    result_type = question['resultType']
    question_id = question['_id']
    result = check(answer, solution, result_type, connection=conn)

    try:
        ans = submission_data['answers'][answer_index]
        ans['answer'] = answer
        submission_data['currentScore'] -= question['score']*ans['clientCheck']
        ans['clientCheck'] = int(result)
        submission_data['currentScore'] += question['score']*ans['clientCheck']
        _ = Submission.create(db, submission_data)
    except:
        print('')
    finally:
        score = submission_data['currentScore']
        print(f'Your current score: {score}/{total_score}')
        
# def check(submission, solution, assignment_type, **kargs):
#     if (assignment_type == 'SQL'):
#         conn = kargs['connection']
#         df_sub = pd.read_sql_query(submission, conn)
#         df_sol = pd.read_sql_query(solution, conn)
#         try:
#             assert df_sol.equals(df_sub)
#             print('You passed! Good job!')
#             return True
#         except:
#             print('Your solution is not correct, try again')
#             return False

#     if (assignment_type == 'Function'):
#         test_cases = kargs['test_cases']
        
#         try:
#             score = 0
#             exec(submission)
#             exec(solution)
#             func_name = submission.split('(')[0][4:]
#             func_name_sol = solution.split('(')[0][4:]
#             for test_case in test_cases:
#                 result = locals()[func_name_sol](*test_case)
#                 if (result == locals()[func_name](*test_case)):
#                     score += 1
#             print(f'You have passed {score}/{len(test_cases)} test cases')
#             return score
#         except:
#             print('Your solution is not correct, try again')
#             return 0

#     if (assignment_type == "Expression"):
#         try:
#             result = eval(solution)
#             result_sub = eval(submission)
#             if (isinstance(result, (int, str, float, bool))):
#                 assert result == result_sub
#             if (isinstance(result, (pd.DataFrame, pd.Series))):
#                 assert result.equals(result_sub)
#             if (isinstance(result, (np.ndarray))):
#                 assert np.array_equal(result, result_sub)
#             print('You passed! Good job!')
#             return True
#         except:
#             print('Your solution is not correct, try again')
#             return False
