# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from chat_app import settings

from .models import Chat

from segtiment_analyst import Splitter, POSTagger
from dictionaty_tagger import DictionaryTagger, measure_score
import os


path_yaml = '/home/minhdo/segtiment_analyst/data_segtiment/'
positive_dir = 'positive.yaml'
negative_dir = 'negative.yaml'
inc_dir = 'inc.yaml'
dec_dir = 'dec.yaml'
inv_dir = 'inv.yaml'


def Login(request):
    next = request.GET.get('next', '/home/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Account is not active at the moment.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)
    return render(request, "alpha/login.html", {'next': next})

def Logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def Home(request):
    c = Chat.objects.all()
    return render(request, "alpha/home.html", {'home': 'active', 'chat': c})

def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        ################# start ###################
        """
        estimate chat segtiment
        """
        text = str(msg.encode('utf-8'))
        print (text)
        splitter = Splitter()
        postagger = POSTagger()

        splitted_sentences = splitter.split(text.decode('utf-8'))
        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)

        # print pos_tagged_sentences

        dicttagger = DictionaryTagger([
                                            os.path.join(path_yaml, positive_dir),
                                            os.path.join(path_yaml, negative_dir),
                                            os.path.join(path_yaml, inc_dir),
                                            os.path.join(path_yaml, dec_dir),
                                            os.path.join(path_yaml, inv_dir),

                                        ]
                                    )

        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        score = measure_score.sentiment_score(dict_tagged_sentences)
        if score > 0:
            sentence_type = "it's positive sentence"
            print ( "what you says is : {} \n    => it's positive sentence".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )
        elif score < 0:
            sentence_type = "it's negative sentence"
            print ( "what you says is : {} \n    => it's negative sentence".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )    
        else:
            sentence_type = "it's neutral sentence"
            print ( "what you says is : {} \n    => it's neutral sentence".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )    
        ################# end ###################

        c = Chat(user=request.user, message=msg, sentence_type = sentence_type)
        if msg != '':
            c.save()
        return JsonResponse({ 'msg': msg, 'user': c.user.username, 'sentence_type':sentence_type })
    else:
        return HttpResponse('Request must be POST.')

def Messages(request):
    c = Chat.objects.all()
    return render(request, 'alpha/messages.html', {'chat': c})