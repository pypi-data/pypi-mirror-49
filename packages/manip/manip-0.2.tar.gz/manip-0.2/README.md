# File manipulation

## Explanation:

<p>The idea is to transform a function that transform one text into another text and call it transforming the desired files with that function.</p>
<p>This is not a package made thinking about being used in a project, rather it's a package made to make a programmer's life easier.</p>

## INSTRUCTIONS:
<p>Decorator that transforms an <b>[str] = function( [str]:text, *args, **kwargs )</b> into an function that apllies itself into a folder.</p>
<p>The default values for the new function can be set at the decorator.</p>
<div class='params'>
<label><b>at</b> - regex to search target files</label>
<label><b>path</b> - folder with files to change (start folder on recursive mode)</label>
<label><b>recursive</b> - makes the function call itself on all folders inside the start folder</label>
<label><b>ignore</b> - ignore changes on file if function returns any error and continues to the next file</label>
<label><b>test</b> - creates a new file with the changes for test (NOT recommended with: recursive = True)</label>
<label><b>prefix/posfix</b> - strings added before and after test files</label>
<label><b>log</b> - shows on console steps</label>
</div>

<p>Default values on decorator are set to avoid writting over important files with broken functions.</p>

### !! ATENTION !!
<p>MAKE SURE TO ALWAYS TEST YOUR FUNCTIONS BEFORE APPLYING ANY TRUE CHANGES.</p>

### Simple functions:

<p>Imagine you want to comment all prints in your project:</p>

~~~
from manip import manip

@manip()
def comment_print(text):
    return text.replace('print(', '# print(')
~~~

<p>Now we can call the function on a folder like:</p>

~~~
comment_print(path='./target')
comment_print(path='./target', test=False) # to save changes on original files
~~~

<p>If you wanna just call a single line function on the command line you can import manipulate:</p>

~~~
from manip import manipulate

manipulate(lambda text: text.replace('print(', '# print('), path='./target', test=False)
~~~

<p>up to change whole files with json data, maybe:</p>

~~~
from manip import manip
import json

@manip(at='.json$')
def join_props(text, prop1='key', prop2='value', new_prop='new'):
    obj = json.loads(text)
    obj[new_prop] = (prop1, prop2)
    
    del(obj[prop1])
    del(obj[prop2])

    return json.dumps(obj)
~~~

### More info:

[GitHub](https://github.com/Flipecs/file_manip)

<style>
p {
    font-size: 19px;
}

.params {
    display: flex;
    flex-direction: column;
    margin-left: 3%;
    font-size: 17px;

    margin-bottom: 15px;
}
</style>