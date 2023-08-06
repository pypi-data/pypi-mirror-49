# Python分類快取
- 非常易用Python快取
- 適合處理零碎的小塊取
- 使用字首進行分類
- 支持中文檔名

# 安裝
```
pip install py-classification-cache
```

# 使用
## import
```python
import py_classification_cache as pcc
pyCahce = pcc.PCC()
```

## order cache save path
```python
pyCahce = pcc.PCC(cache_dir="CACHE_DIR_PATH")
```

## save and get
```python
pyCache.save("array",[1,2,3])
pyCache.save("dic",{"key1":1,"key2":2})
pyCache.get("array") # [1,2,3]
pyCache.get("dic") # {"key1":1,"key2":2}
```

## remove
```python
pyCache.remove("KEY") # remove key
py.Cache.clearCache() # remove all cache
```


