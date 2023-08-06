# distxml
Convert labeled data to xml at scale.

## Installation

Run the following command:
```python
pip install distxml
```

## Usage

Import the the package and create an instance of `XMLConverter` with
your desired outer xml tag.
```
from distxml.xml_converter import XMLConverter

xml_con = XMLConverter("Hello")
```
You now have an `XMLConverter` object, and if you print it
would write `<Hello />` to console. Now add data you want
within the `Hello` tags.
```
data = [
    {'start':'Good morning', 'finish':' Good night'},
    {'finish':' Good evening', 'start':'Good morning again'}
]

xml_con.queue(data)
```
Now this data is queued in the XMLConverter object, but if you print
`xml_con`, it will still write `<Hello />` to console.
To solve this, you must compile the data.
```
xml_con.compile("Greetings")
```
Now if you print, the console will read
```
<Hello><Greetings><start>Good morning</start><finish> Good night</finish></Greetings><Greetings><finish> Good evening</finish><start>Good morning again</start></Greetings></Hello>
```
Finally, to write to a file, just use
```
xml_con.write_to_file("filepath/file.xml")
```
And there you go, a new xml file!
