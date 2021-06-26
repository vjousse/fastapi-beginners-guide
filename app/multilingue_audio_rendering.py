# In[18]:


import requests
import json
import boto3
import time
from decouple import config
from pathlib     import Path
from datetime    import datetime
from markdown_it import MarkdownIt


# In[3]:
WORKSPACE = './workspace'

### DEEPL TRANSLATION
URL = "https://api-free.deepl.com/v2/translate"
HEADERS = requests.utils.default_headers()
HEADERS.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        'Content-type': 'application/x-www-form-urlencoded'
})
AUTH_KEY = config('AUTH_KEY')
url_auth = URL + "?auth_key=" + AUTH_KEY

### POLLY AUDIO + S3 STORAGE SESSION
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')

session = boto3.Session(aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_ACCESS_KEY,region_name=AWS_S3_REGION_NAME)
bucket  = session.resource('s3').Bucket(AWS_STORAGE_BUCKET_NAME)
polly   = session.client("polly")

### SUBSTACK
substack_url_prefix = "https://rencontrerlarche.substack.com/p/"


# In[4]:


def save_json(datas,save_path,name,debug=True):
    """
        this function save list of dict into json given path and name file
        create path if not exist
    """
    path = Path(save_path)
    path.mkdir(parents=True, exist_ok=True)
    #name = decode_string_for_filename(name)

    if name.split('.')[-1] == 'json':
        filename = path.joinpath(name)
    else:
        filename = path.joinpath(f"{name}.json")

    with open(filename, 'w') as filehandle:
        json.dump(datas, filehandle)
        filehandle.close()

    if debug: print(f'[{datetime.now()}] {len(datas)} items saved in json {filename}')


# In[5]:


def init_datas(prefix):
    datas = {
        'FR': {'translate':False, 'voiceId':False,      'flag':"version 🇨🇵 🇧🇪"},
        'EN': {'translate':True,  'voiceId':'Matthew',  'flag':"🇬🇧 version"},
        'DE': {'translate':True,  'voiceId':'Hans',     'flag':"🇩🇪 version"},
        'ES': {'translate':True,  'voiceId':'Conchita', 'flag':"versión 🇪🇦"},
        'PL': {'translate':True,  'voiceId':'Ewa',      'flag':"wersja 🇵🇱"},
        'LT': {'translate':True,  'voiceId':False,      'flag':"🇱🇹 versija"},
        'UA': {'translate':False, 'voiceId':False,      'flag':"🇺🇦 kalba"},
    }
    
    for k,v in datas.items():
        v['slug'] = f"{prefix}{k}".lower()
        v['link'] = substack_url_prefix + v['slug']
        
    return datas


# In[6]:


def set_source_text(datas,lang,text):
    datas[lang]['text'] = text
    datas[lang]['translate'] = False    
    return datas


# In[13]:


def set_headers(datas):
    flags = []
    for k,v in datas.items():
        flag = v['flag']
        link = v['link']
        flags.append(f"[{flag}]({link})")
    return "\n" + ' | '.join(flags) + "\n\n***\n"


# In[8]:


def translate_text(text,target_lang,source_lang):
    r = requests.post(url_auth + "&text=" + text + "&target_lang=" + target_lang + "&source_lang=" + source_lang, headers=HEADERS )
    return r.json()['translations'][0]['text']


# In[9]:


def TTS_text(filename,text,voiceId):
    response = polly.start_speech_synthesis_task(
            OutputFormat= "mp3",
            Text = text,
            #TextType = "ssml",
            VoiceId= voiceId, 
            OutputS3BucketName=AWS_STORAGE_BUCKET_NAME,
            OutputS3KeyPrefix=filename)
    response['SynthesisTask']['CreationTime'] = response['SynthesisTask']['CreationTime'].strftime('%d/%m/%Y %H:%M:%S')
    return response


# In[10]:


def render_MD(text,headers,filename):
    md = (MarkdownIt())
    html_text = md.render(headers + text)
    Path(f"{filename}.html").write_text(html_text) 
    return 1


# In[15]:


if __name__ == "__main__":
    source_lang     = 'EN'
    filename_prefix = 'update09' 

    with open(f'{WORKSPACE}/source_text.txt') as f:
        lines = f.readlines()

    datas   = init_datas(filename_prefix)
    headers = set_headers(datas)
    datas   = set_source_text(datas,source_lang, ''.join(lines))

    for target_lang in datas.keys():

        # translation
        if datas[target_lang]['translate']:
            print(f"translate {target_lang}")
            datas[target_lang]['text'] = translate_text(datas[source_lang]['text'],target_lang,source_lang)

        # TTS
        if datas[target_lang]['voiceId']:
            print(f"TTS {target_lang}")
            datas[target_lang]['TTS'] = TTS_text(f"{filename_prefix}{target_lang}",datas[target_lang]['text'],datas[target_lang]['voiceId'])

        # rendering
        if 'text' in datas[target_lang].keys():
            print(f"rendering {target_lang}")
            render_MD(datas[target_lang]['text'],headers,f"{WORKSPACE}/{filename_prefix}{target_lang}")

    save_json(datas,'.',f'{WORKSPACE}/{filename_prefix}.json')

    print("waiting for MP3s generation")
    step = 10
    for i in range(6):
        time.sleep(step)
        print(f"{(i+1)*step} sec")

    print("requesting MP3s")
    for k,v in datas.items():
        if 'TTS' in v:
            obj = v['TTS']['SynthesisTask']['OutputUri'].split('/')[-1]
            print(f"downloading {obj}")
            bucket.download_file(obj, f"{WORKSPACE}/{obj}")

    print("slug fields")
    for k,v in datas.items():
        print(v['slug'])

