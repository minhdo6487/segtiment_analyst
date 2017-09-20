# -*- coding: utf-8 -*-
import os
import sys
import yaml
from segtiment_analyst import Splitter, POSTagger
"""
Global
positive_dir
negative_dir
inc_dir
dec_dir
inv_dec
"""
path_yaml = '/home/minhdo/segtiment_analyst/data_segtiment/'
positive_dir = 'positive.yaml'
negative_dir = 'negative.yaml'
inc_dir = 'inc.yaml'
dec_dir = 'dec.yaml'
inv_dir = 'inv.yaml'

class DictionaryTagger(object):
    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

class measure_score:
    @classmethod
    def value_of(cls, sentiment):
        if sentiment == 'positive': return 1
        if sentiment == 'negative': return -1
        return 0

    # @classmethod
    # def sentiment_score(cls, review):    
    #     return sum ([ measure_score.value_of(tag) for sentence in dict_tagged_sentences for token in sentence for tag in token[2]])

    @classmethod
    def sentiment_score(cls, review):
        return sum([measure_score.sentence_score(sentence, None, 0.0) for sentence in review])

    @classmethod
    def sentence_score(cls, sentence_tokens, previous_token, acum_score):    
        if not sentence_tokens:
            return acum_score
        else:
            current_token = sentence_tokens[0]
            tags = current_token[2]
            token_score = sum([measure_score.value_of(tag) for tag in tags])


            if previous_token is not None:
                previous_tags = previous_token[2]
                if 'inc' in previous_tags:
                    token_score *= 2.0
                elif 'dec' in previous_tags:
                    token_score /= 2.0
                elif 'inv' in previous_tags:
                    token_score *= -1.0
            return measure_score.sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)



if __name__ == "__main__":
    # text = """
    #         What can I say about this place. 
    #         The staff of the restaurant is nice and the eggplant is not bad. 
    #         Apart from that, very uninspired food, lack of atmosphere and too expensive. 
    #         I am a staunch vegetarian and was sorely dissapointed with the veggie options on the menu. 
    #         Will be the last time I visit, I recommend others to avoid.
    #         """

    text = """
            this is dog expensive
            """
    # list_text = [
    #     "I like dog",
    #     "But I not love cat, too"
    # ]

    splitter = Splitter()
    postagger = POSTagger()


    splitted_sentences = splitter.split(text.decode('utf-8'))
    # splitted_sentences = splitter.split(list_text[1].decode('utf-8'))

    print splitted_sentences
    
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

    print(dict_tagged_sentences)

    score = measure_score.sentiment_score(dict_tagged_sentences)
    if score > 0:
        print ( "senctence: {} --- score: {} => pos".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )
    elif score < 0:
        print ( "senctence: {} --- score: {} => neg".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )    
    else:
        print ( "senctence: {} --- score: {} => neutral".format(text , measure_score.sentiment_score(dict_tagged_sentences))  )    