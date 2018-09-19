
# coding: utf-8

# In[35]:


#Imports
import os, os.path
from whoosh import index
from whoosh import fields
from whoosh.analysis import StemmingAnalyzer
from whoosh.analysis import StandardAnalyzer
from whoosh.analysis import StopFilter
from whoosh.lang.porter import stem
import glob
import codecs
from whoosh import scoring


# In[2]:


#SEM STEMMING/STOPWORDS
if not os.path.exists("stan"):
    os.mkdir("stan")
    
stan_ana = StandardAnalyzer(stoplist=None)
schema_stan = fields.Schema(title=fields.TEXT(analyzer=stan_ana, stored=True), content=fields.TEXT(analyzer=stan_ana))

ix_stan = index.create_in("stan", schema_stan)


# In[3]:


#COM STEMMING
if not os.path.exists("stem"):
    os.mkdir("stem")
    
stem_ana = StemmingAnalyzer(stoplist=None, minsize=2, maxsize=None, gaps=False, stemfn=stem, ignore=None, cachesize=50000)
schema_stem = fields.Schema(title=fields.TEXT(analyzer=stem_ana, stored=True), content=fields.TEXT(analyzer=stem_ana))

ix_stem = index.create_in("stem", schema_stem)


# In[4]:


#COM STOPWORDS
if not os.path.exists("stop"):
    os.mkdir("stop")
    
stop_ana = StandardAnalyzer(stoplist=frozenset(['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may', 'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are']))
schema_stop = fields.Schema(title=fields.TEXT(analyzer=stop_ana, stored=True), content=fields.TEXT(analyzer=stop_ana))

ix_stop = index.create_in("stop", schema_stop)


# In[5]:


#COM STEMMING E STOPWORDS
if not os.path.exists("all"):
    os.mkdir("all")
    
all_ana = StemmingAnalyzer(stoplist=frozenset(['and', 'is', 'it', 'an', 'as', 'at', 'have', 'in', 'yet', 'if', 'from', 'for', 'when', 'by', 'to', 'you', 'be', 'we', 'that', 'may', 'not', 'with', 'tbd', 'a', 'on', 'your', 'this', 'of', 'us', 'will', 'can', 'the', 'or', 'are']), minsize=2, maxsize=None, gaps=False, stemfn=stem, ignore=None, cachesize=50000)
schema_all = fields.Schema(title=fields.TEXT(analyzer=all_ana, stored=True), content=fields.TEXT(analyzer=all_ana))

ix_all = index.create_in("all", schema_all)


# In[6]:


ix_stan = index.open_dir("./stan")
ix_stem = index.open_dir("./stem")
ix_stop = index.open_dir("./stop")
ix_all = index.open_dir("./all")

w_stem = ix_stem.writer()
w_stan = ix_stan.writer()
w_stop = ix_stop.writer()
w_all = ix_all.writer()

for path in glob.glob("./docs/*.pdf"):
    path = path.replace("\\","/")
    print("LENDO ARQUIVOS...")
    with open(path, "r",encoding="utf-8", errors='ignore') as f:
        content = f.read()
        print(os.path.basename(path))
        w_stem.add_document(title=os.path.basename(path), content=content)
        w_stan.add_document(title=os.path.basename(path), content=content)
        w_stop.add_document(title=os.path.basename(path), content=content)
        w_all.add_document(title=os.path.basename(path), content=content)
        f.close()
print("LEITURA E ADIÇÃO COMPLETAS!\n")
print("Commitando Stemming")
w_stem.commit()
print("Commitando Standard")
w_stan.commit()
print("Commitando Stopwords")
w_stop.commit()
print("Commitando Stemming+Stopwords")
w_all.commit()


# In[37]:


from whoosh.qparser import QueryParser

search = "big data for health"

with ix_stan.searcher(weighting=scoring.TF_IDF()) as searcher:
    query = QueryParser("content", ix_stan.schema).parse(search)
    results = searcher.search(query)
    print("RESULTADOS STANDARD: ", len(results))
    for result in results:
        display(result)

with ix_stem.searcher(weighting=scoring.TF_IDF()) as searcher:
    query = QueryParser("content", ix_stem.schema).parse(search)
    results = searcher.search(query)
    print("RESULTADOS STEM: ", len(results))
    for result in results:
        display(result)

with ix_stop.searcher(weighting=scoring.TF_IDF()) as searcher:
    query = QueryParser("content", ix_stop.schema).parse(search)
    results = searcher.search(query)
    print("RESULTADOS STOP: ", len(results))
    for result in results:
        display(result)
        
with ix_all.searcher(weighting=scoring.TF_IDF()) as searcher:
    query = QueryParser("content", ix_all.schema).parse(search)
    results = searcher.search(query)
    print("RESULTADOS ALL: ", len(results))
    for result in results:
        display(result)


# In[33]:


print(ix_all.schema.names())

