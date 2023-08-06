# PDF-creator
It`s a library create pdf files
## Installing:
pip install pdf_creator
## Guide:
```python
from pdf_creator.creator import pdf_creator
new = pdf_creator('papka/new.pdf') # create file on path 'papka/new.pdf'
new.text('guide', 100, 100) # write 'guide' on 100,100; size of page 594,842
data = [
    ['1', '2'],
    ['a', 'b']
]
new.table(data, 200, 200) # create table on 200,200
new.image('papka/img.png', 300, 300) # create image from 'papka/img.png' on 300,300
new.save() # save file
```
