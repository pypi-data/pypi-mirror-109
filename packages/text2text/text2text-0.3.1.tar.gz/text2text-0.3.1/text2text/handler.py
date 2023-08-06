from text2text import (
    Answerer, 
    Counter,
    Measurer, 
    Questioner, 
    Searcher,
    Summarizer,
    Tfidfer,
    Tokenizer,
    Translator, 
    Variator,
    Vectorizer, 
)

class Handler(object):
  """
  Text Handler unified API for text transformers
  """

  EXPOSED_TRANSFORMERS = {
    "answer": Answerer,
    "count": Counter,
    "measure": Measurer,
    "question": Questioner,
    "search": Searcher,
    "summarize": Summarizer,
    "tfidf": Tfidfer,
    "tokenize": Tokenizer,
    "translate": Translator,
    "variate": Variator,
    "vectorize": Vectorizer,
  }

  def _transformer_handler(self, transformation, **kwargs):
    transformer = self.__class__.transformer_instances.get(transformation, self.__class__.EXPOSED_TRANSFORMERS[transformation](pretrained_translator=self.__class__.pretrained_translator))
    self.__class__.transformer_instances[transformation] = transformer
    return transformer.transform(input_lines=self.input_lines, src_lang=self.src_lang, **kwargs)
    
  def __init__(self, input_lines=[], src_lang='en', **kwargs):
    self.input_lines = input_lines
    self.src_lang = src_lang
    self.__class__.pretrained_translator = kwargs.get("pretrained_translator")
    for k in self.__class__.EXPOSED_TRANSFORMERS:
      handler = lambda x: lambda **kwargs: self._transformer_handler(transformation=x, **kwargs)
      handler = handler(k)
      setattr(self, k, handler)
    self.__class__.transformer_instances = {}