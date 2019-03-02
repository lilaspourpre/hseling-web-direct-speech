from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django import forms

import requests

HSE_API_ROOT = "http://hse-api-web/"
RU_TO_EN_DICT = {"Всего авторских комментариев (слова автора)": "author_comment",
                 "В них собственно высказываний:": "said",
                 "Не сказано вслух:": "said_aloud_false",
                 "Сказано вслух:": "said_aloud_true",
                 "Из них прямая речь:": "said_type_direct",
                 "Косвенная речь:": "said_type_indirect",
                 "Всего случаев чужой речи в тексте:": "speech",
                 "Всего глаголов речи (не уникальных):": "speech_verb",
                 "Глаголов с пометкой 'волнение':": "speech_verb_emotion_emotional",
                 "Глаголов с пометкой 'перебивать':": "speech_verb_emotion_interrupt",
                 "Глаголов с пометкой 'громкий':": "speech_verb_emotion_loud",
                 "Нейтральных глаголов:": "speech_verb_emotion_neutral",
                 "Глаголов с пометкой 'возражать':": "speech_verb_emotion_no",
                 "Глаголов, вводящих вопрос:": "speech_verb_emotion_question",
                 "Глаголов с пометкой 'грубый':": "speech_verb_emotion_rude",
                 "Глаголов с пометкой 'грустный':": "speech_verb_emotion_sad",
                 "Глаголов с пометкой 'соглашаться':": "speech_verb_emotion_yes",
                 "Глаголов с семантикой 'действие':": "speech_verb_semantic_action",
                 "Глаголов с семантикой 'пение':": "speech_verb_semantic_song",
                 "Из них глаголов с семантикой 'речь':": "speech_verb_semantic_speech",
                 "Глаголов с семантикой 'мысль':": "speech_verb_semantic_thought"}

LIST_RU = ["Всего авторских комментариев (слова автора)",
           "В них собственно высказываний:",
           "Не сказано вслух:",
           "Сказано вслух:",
           "Из них прямая речь:",
           "Косвенная речь:",
           "Всего случаев чужой речи в тексте:",
           "Всего глаголов речи (не уникальных):",
           "Глаголов с пометкой 'волнение':",
           "Глаголов с пометкой 'перебивать':",
           "Глаголов с пометкой 'громкий':",
           "Нейтральных глаголов:",
           "Глаголов с пометкой 'возражать':",
           "Глаголов, вводящих вопрос:",
           "Глаголов с пометкой 'грубый':",
           "Глаголов с пометкой 'грустный':",
           "Глаголов с пометкой 'соглашаться':",
           "Глаголов с семантикой 'действие':",
           "Глаголов с семантикой 'пение':",
           "Из них глаголов с семантикой 'речь':",
           "Глаголов с семантикой 'мысль':"]


# Create your views here.
def web_index(request):
    return render(request, 'index.html',
                  context={})


def web_about(request):
    return render(request, 'about.html', context={})


def web_gold(request):
    return render(request, 'gold-corpus.html', context={})


def web_tag(request):
    return render(request, 'tag-your-text.html', context={})


def web_main(request):
    return render(request, 'main.html',
                  context={"status": request.GET.get('status')})


def web_status(request):
    task_id = request.GET.get('task_id')
    if task_id:
        url = HSE_API_ROOT + "status/" + task_id
        content = requests.get(url)
        result = content.json()
        if result.get('status') == 'SUCCESS':
            file_id = result.get('result', [""])[0]
            result["file_id"] = file_id
            return JsonResponse(result)
    return JsonResponse({"error": "No task id"})


def download_file(request):
    new_statistics = []
    file_id = request.GET.get('file_id')
    if file_id:
        statistics = requests.get(HSE_API_ROOT +
                                  'query/text.txt?type=statistics').json()
        for n in LIST_RU:
            try:
                new_statistics.append((n, statistics[RU_TO_EN_DICT[n]]))
            except KeyError as e:
                print(e, n)
    return render(request, 'main_download.html',
                  {'file_id': file_id, "statistics": new_statistics})


def download_processed(request):
    file_id = request.GET.get('file_id')
    file_ = requests.request("GET", HSE_API_ROOT + 'files/' + file_id)
    text = file_.content
    with open('test', 'w') as f:
        f.write(text.decode('utf-8'))
    response = HttpResponse(text, content_type="application/txt")
    response['Content-Disposition'] = 'attachment;filename={}'.format(file_id)
    return response


def download_gold(request):
    return render(request, 'gold-corpus.html', {})


def download_xml(request):
    type1 = requests.request("GET", HSE_API_ROOT + 'files/gold?type=xml')
    xml_text = type1.content
    response = HttpResponse(xml_text, content_type="application/xml")
    response['Content-Disposition'] = 'attachment;filename=gold.xml'
    return response


def download_txt(request):
    type1 = requests.request("GET", HSE_API_ROOT + 'files/gold?type=txt')
    txt_text = type1.content
    response = HttpResponse(txt_text, content_type="application/txt")
    response['Content-Disposition'] = 'attachment;filename=gold.txt'
    return response


def handle_uploaded_file(f):
    files = {'file': f}
    url = HSE_API_ROOT + "upload"
    content = requests.post(url, files=files)

    file_id = content.json().get("file_id")

    if file_id:
        file_id = file_id[7:]
        url = HSE_API_ROOT + "process/" + file_id
        content = requests.get(url)

    else:
        raise Exception(content.json())

    return content.json().get('task_id')


class UploadFileForm(forms.Form):
    file = forms.FileField()


def web_upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('p?task_id=' + task_id)
    else:
        form = UploadFileForm()
    return render(request, 'main.html', {'form': form})


def web_processing(request):
    return render(request, 'main.html')
