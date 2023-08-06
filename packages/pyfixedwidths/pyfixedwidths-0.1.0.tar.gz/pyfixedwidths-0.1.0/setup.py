# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyfixedwidths']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pyfixedwidths',
    'version': '0.1.0',
    'description': 'Easy way converting from text, list, or dict to text or list with fixed widths.',
    'long_description': 'pyfixedwidths\n==========================================================\nEasy way converting from text, list, or dict to text or list with fixed widths.\n\nThe Installation\n------------------\n>>> pip install pyfixedwidths\n\nExamples\n-----------\n>>> from pyfixedwidths import FixedWidthFormatter\n>>> text = (\n>>> "1,2,3,4\\n"\n>>> "11,,33,44\\n"\n>>> )\n>>> \n>>> listofdict = [\n>>>     dict(name="John Doe", age=20, hobby="swim"),\n>>>     dict(name="John Smith", age=100, job="teacher"),\n>>> ]\n>>> \n>>> array = [\n>>>     [1, None, 3, 4],\n>>>     [11, 22, None, 44],\n>>> ]\n>>> \n\n>>> fw = FixedWidthFormatter()\n>>> fw.from_text(text).to_text(padding=1)\n>>> #=>\n>>>     ("1  , 2 , 3  , 4 \\n"   \n>>>      "11 ,   , 33 , 44\\n")\n>>> \n>>> fw.from_text(text).to_array(padding=1)\n>>> #=>\n>>>     [["1  "," 2 "," 3  "," 4 "],\n>>>      ["11 ","   "," 33 "," 44"],]\n>>> \n\n>>> fw = FixedWidthFormatter()\n>>> fw.from_array(array).to_text(padding=0)\n>>> #=>\n>>>     ("1 ,None,3   ,4 \\n"\n>>>      "11,    ,None,44\\n")\n>>> \n>>> fw.from_array(array).to_array(padding=0)\n>>> #=>\n>>>     [["1 ","None","3   ","4 "],\n>>>      ["11","    ","None","44"],]\n>>> \n\n>>> fw = FixedWidthFormatter(schema=schema)\n>>> fw.from_dict(listofdict).to_text(padding=0)\n>>> #=>\n>>>     ("name      ,age,hobby,job    \\n"\n>>>      "John Doe  ,20 ,swim ,       \\n"\n>>>      "John Smith,100,     ,teacher\\n")\n>>> \n>>> fw.from_dict(listofdict).to_list(padding=0)\n>>> #=>\n>>>     [["name      ", "age", "hobby", "job    "],\n>>>      ["John Doe  ", "20 ", "swim ", "       "],\n>>>      ["John Smith", "100", "     ", "teacher"],]\n\n>>> schema = [\n>>>     dict(\n>>>         justification="rjust"\n>>>     ),\n>>>     dict(\n>>>         format=":>5s"\n>>>     ),\n>>>     dict(),\n>>>     dict(\n>>>         format=":2s"\n>>>     )\n>>> ]\n>>> \n>>> fw = FixedWidthFormatter(schema=schema)\n>>> fw.from_dict(listofdict).to_text(padding=2)\n>>> #=>\n>>>     ("      name  ,    age  ,  hobby  ,  job\\n"\n>>>      "  John Doe  ,     20  ,  swim   ,    \\n"\n>>>      "John Smith  ,    100  ,         ,  teacher\\n")\n>>> \n>>> fw.from_dict(listofdict, headers=["hobby", "job", "location", "name"]).to_text(padding=1)\n>>> #=>\n>>>     (   "hobby ,     job , location , name\\n"\n>>>         " swim ,         ,          , John Doe\\n"\n>>>         "      , teacher ,          , John Smith\\n")\n\n\nRequirements\n----------------\n\n- Python 3',
    'author': 'Shoma FUKUDA',
    'author_email': 'fkshom+pypi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fkshom',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
