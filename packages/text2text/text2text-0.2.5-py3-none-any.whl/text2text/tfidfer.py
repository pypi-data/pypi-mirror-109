import numpy as np
from text2text import Counter

class Tfidfer(Counter):

  def _calculate_idf(self, token_counts):
    num_documents = len(token_counts)
    self.idf = {}
    for count in token_counts:
      counted = set()
      for tk in count:
        if tk not in self.idf:
          self.idf[tk] = 0
        if tk not in counted:
          self.idf[tk] += 1
          counted.add(tk)
    for tk in self.idf:
      self.idf[tk] = np.log(num_documents/(1+self.idf[tk]))+1

  def _normalize_counts(self, token_counts):
    for i in range(len(token_counts)):
      num_tokens = sum(token_counts[i].values())
      for tk in token_counts[i]:
        token_counts[i][tk] /= num_tokens

      magnitude = 0
      for tk in token_counts[i]:
        token_counts[i][tk] *= self.idf.get(tk,0)
        magnitude += token_counts[i][tk]**2

      magnitude **= 0.5 
      for tk in token_counts[i]:
        token_counts[i][tk] /= magnitude
    return token_counts

  def predict(self, input_lines, src_lang='en', output='tokens', **kwargs):
    token_counts = Counter.predict(self, input_lines, src_lang=src_lang, output=output, **kwargs)
    self._calculate_idf(token_counts)
    return self._normalize_counts(token_counts)