from django.shortcuts import  redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
import json


class FuzzySearch(View):
    call_type = ''

    def get(self, request):
        if self.call_type == 'autocomplete':
            query = request.GET.get('term', '')
            results = sorting(search(query.lower()), query.lower())
            search_result = json.dumps(results)
            type = 'application/json'
            return HttpResponse(search_result, type)
        elif self.call_type == 'searchaction':
            query = request.GET.get('word')
            if query:
                searchResult = sorting(search(query.lower()), query.lower())
                if len(searchResult) == 0:
                    return JsonResponse({'result': "No Data Found For the Search.", 'found': False})
                else:
                    return JsonResponse({'result': searchResult, 'found': True})
            else:
                return JsonResponse({'result': "No Data Found For the Search.", 'found': False})


def searchAction(request):
    if request.method == 'GET':
        word = request.GET.get('word')
        print(word)
        if word:
            searchResult = sorting(search(word.lower()), word.lower())
            if len(searchResult) == 0:
                return JsonResponse({'Search_Result': "Word not found."})
            else:
                return JsonResponse({'Search_Result': searchResult})
        else:
            return redirect('/')


word_count = {}
words = []
with open('word_search.tsv') as file:
    for row in file:
        word, frequency = row.split('\t')
        word_count[word] = int(frequency.strip())
        words.append(word)


def search(word_letter):
    results = []
    for word in words:
        if word_letter in word:
            results.append(word)
    return results


def sorting(results, input_word):
    try:
        result_dict = {}
        for result in results[:25]:
            print(result, 'result', result.find(input_word), result.find(input_word))
            try:
                try:
                    result_dict[result.find(input_word)] = return_sorted_list(result_dict[result.find(input_word)])
                except:
                    result_dict[result.find(input_word)] = {}
                result_dict[result.find(input_word)][len(result)] = return_sorted_list(
                    result_dict[result.find(input_word)][len(result)])
            except Exception as e:
                result_dict[result.find(input_word)][len(result)] = {}
                print(e, 'warning')
            result_dict[result.find(input_word)][len(result)][word_count[result]] = result
            result_dict[result.find(input_word)][len(result)] = return_sorted_list(
                result_dict[result.find(input_word)][len(result)])
        print(return_sorted_list(result_dict), '====================================================')
        search_list_results = list(get_word_list(return_sorted_list(result_dict)))
        print(list(get_word_list(return_sorted_list(result_dict))), '----------------------------------------')
        return search_list_results
    except Exception as e:
        print(e, 'érror')


def return_sorted_list(result_dict):
    try:
        return dict(sorted(result_dict.items()))
    except:
        return {}


def get_word_list(d):
    for v in d.values():
        if isinstance(v, dict):
            yield from get_word_list(v)
        else:
            yield v
