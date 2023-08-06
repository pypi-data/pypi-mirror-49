# Python分類快取
- 非常易用的Python快取
- 適合處理零碎的小快取
- 使用字首進行分類
- 支持中文檔名

# Install
```
pip install py-classification-cache
```

# Usage
## Import
```python
import py_classification_cache as pycc
pyCahce = pycc.PCC()
```

## Order cache saving path
```python
pyCahce = pycc.PCC(cache_dir="CACHE_DIR_PATH")
```

## Save and get
```python
pyCache.save("array",[1,2,3])
pyCache.save("dic",{"key1":1,"key2":2})
pyCache.get("array") # [1,2,3]
pyCache.get("dic") # {"key1":1,"key2":2}
```

## Remove and clear
```python
pyCache.remove("KEY") # remove key
py.Cache.clearCache() # remove all cache
```


