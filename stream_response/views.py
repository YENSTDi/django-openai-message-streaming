from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.views.decorators.csrf import csrf_exempt

import openai
import json


# Create your views here.
@csrf_exempt
def index(request:WSGIRequest):
    return render(request, "index.html")

@csrf_exempt
def stream_message(request:WSGIRequest):
    
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message")
        print(message)
        response = StreamingHttpResponse(openai_streaming(message), content_type="text/plain")
        return response
    else:
        return HttpResponse("Need post")

def openai_streaming(msg):
    openai.api_key = "your api key"

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{'role': 'system', 'content': msg}],
        stream=True
    )
    
    for event in completion:
        try:
            finish_reason = event['choices'][0]['finish_reason']
            if finish_reason=="stop":
                break
    
            event = json.dumps(event)
            event = json.loads(event)
            event_text = event['choices'][0]['delta']['content']  # extract the text
            # print(event_text)
            yield event_text
        except:
            pass
