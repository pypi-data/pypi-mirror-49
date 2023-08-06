# pdfutil [Under Development]
Library provides a lot of operations over PDF/Image.

## Input and Output 
The Libarary expose each function with a standard set of argument which are fixed for eevry function
```
import pdfutil
coordinates = pdfutil.detect_*(pdf_location, [save_result=False], [show_result=False], [result_location='.'], [args={}])
```

| Name | Description |
| --- | --- |
|**pdf_location** | input location of PDF, image can also be passed libaray will autodetect the image|
|**save_result**| Default False, If True will save the result pdf/img in location specified by result_location|
|**show_result**| Default False, This is used for debugging only when True will popup a matplotlib plot highlighting the regions which are detected with corresponding labels|
|**result_location**| Default current directory, location where ouptut needs to be saved, ignored if save_result is set as False|
|**args**| custom set of args in form of dictionaty specific to each function|
|**coordinates**| Output returned by the function call, this will contain json output in following format|
```
[
  {
    "type": "text",
    "output": {
      "coord": [
        ["pageno_1", "startx_1", "starty_1", "width_1", "height_1"],
        ["pageno_2", "startx_2", "starty_2", "width_2", "height_2"]
      ]
    }
  },
  {
    "type": "table",
    "output": {
      "coord": [
        ["pageno_1", "startx_1", "starty_1", "width_1", "height_1"],
      ]
    }
  }
]
```

## operations

### Detecting Tables
```
import pdfutil
coordinates = pdfutil.detect_tables(pdf_location)
```

### Detecting Text Regions [Paragrahs / Unstructured Content]
```
import pdfutil
coordinates = pdfutil.detect_text(pdf_location)
```

### Detecting Non-Text Regions [Images / Logos]
```
import pdfutil
coordinates = pdfutil.detect_non_text(pdf_location)
```

### Detecting Language
```
import pdfutil
coordinates = pdfutil.detect_non_language(pdf_location)
```

### Detecting Key Value Pairs
```
import pdfutil
coordinates = pdfutil.detect_key_value_pairs(pdf_location)
```

