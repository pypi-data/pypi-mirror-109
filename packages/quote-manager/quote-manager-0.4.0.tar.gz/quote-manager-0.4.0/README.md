# library.quote.manager

Helper nlp library for handling non ascii quotes.

## Usage

```python3

from quote_manager import Quotes

sentence = “That’s an ‘magic’ shoe.”

quotes_sentence = Quotes(sentence)

quotes_sentence.simplified
>> "That's an 'magic' shoe.'

# do stuff here...
transformed_sentence = transform(quotes_sentence.simplified)
# ex. grammar correction: "That's a 'magic' shoe.'

quotes_sentence.requote_modified_string(transformed_sentence)
>> “That’s a ‘magic’ shoe.”
```