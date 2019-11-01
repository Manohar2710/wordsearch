from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
import json

word_count = {}
words_list = []

with open('word_search.tsv') as file:
    for row in file:
        word, frequency = row.split('\t')
        word_count[word] = int(frequency.strip())
        words_list.append(word)   # appending all the words list form the tsv file to list named variable words


# this class is used to return responce for both autocomplete and search button event based on call type from the url
class FuzzySearch(View):
    call_type = ''

    def get(self, request):
        # if the get request equals type autocomplete it returns the list of searched words
        if self.call_type == 'autocomplete':
            query = request.GET.get('term', '')

            results = sorting_words_list(search(query.lower()), query.lower())  # returns list of 25 words filtered based on the user input
            search_result = json.dumps(results)
            type = 'application/json'
            return HttpResponse(search_result, type)

        elif self.call_type == 'searchaction':  # if the get request equals type searchaction it returns the list of searched words for the provded input
            query = request.GET.get('word')
            if query:
                searchResult = sorting_words_list(search(query.lower()), query.lower()) # returns list of 25 words filtered based on the user input
                if len(searchResult) == 0:
                    return JsonResponse({'result': "No Data Found For the Search.", 'found': False})
                else:
                    return JsonResponse({'result': searchResult, 'found': True})
            else:
                return JsonResponse({'result': "No Data Found For the Search.", 'found': False})


def search(input_word):
    results = []
    try:
        for word in words_list:
            if input_word in word:
                results.append(word) # appends all the possible combinations of words matching with user input
        return results
    except:
        return results


def sorting_words_list(results, input_word):
    try:
        result_dict = {}
        for result in results[:25]:
            # print(result, 'result', result.find(input_word), result.find(input_word))
            try:
                try:
                    result_dict[result.find(input_word)]= return_sorted_list(result_dict[result.find(input_word)]) # sorting based om length of words in ascending order)
                except:
                    result_dict[result.find(input_word)] = {}
                result_dict[result.find(input_word)][len(result)] = return_sorted_list(
                    result_dict[result.find(input_word)][len(result)]) # sorting for ranking up words smaller in length
            except Exception as e:
                result_dict[result.find(input_word)][len(result)] = {}
                print(e, 'warning')
            result_dict[result.find(input_word)][len(result)][word_count[result]] = result
            result_dict[result.find(input_word)][len(result)] = return_sorted_list(
                result_dict[result.find(input_word)][len(result)])    # sorting for ranking up words smaller in length
        print(return_sorted_list(result_dict))
        search_list_results = list(get_word_list(return_sorted_list(result_dict))) # sorting for match in the beginning of words (EX. env --> 1st == environment , 2nd == environmentalism.)
        return search_list_results
    except Exception as e:
        print(e, 'érror')
        return []


def return_sorted_list(result_dict):
    try:
        return dict(sorted(result_dict.items())) # return list of sorted key values pairs sorted by key
    except:
        return {}


def get_word_list(d):
    try:
        for v in d.values():
            if isinstance(v, dict):
                yield from get_word_list(v)
            else:
                yield v    # lists the sorted top 25 words using recursion
    except Exception as e:
        print(e)
