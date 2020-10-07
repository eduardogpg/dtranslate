import os
import json
import boto3
import tempfile

from .common import put_file
from .common import read_content
from .common import put_object

def translate(txt, source='es', target='en'):
    translate = boto3.client('translate')

    response = translate.translate_text(Text=txt,
                                        SourceLanguageCode=source, 
                                        TargetLanguageCode=target)
    
    return response

def translate_from_mediafile(bucket, mediafile_key, prefix='translate_', source='en', target='es', save=True):
    try:
        content = read_content(bucket, mediafile_key)

        if content:
            content = json.loads(content)

            transcript = content['results']['transcripts'][0]['transcript']
            response = translate(transcript, source, target)

            if save:
                content = response['TranslatedText']
                translate_mediafile_key = mediafile_key.replace('.json', '.txt')
                
                if prefix:
                    translate_mediafile_key = translate_mediafile_key.replace('transcribe_', prefix)
                
                put_object(bucket, translate_mediafile_key, content)

                return translate_mediafile_key
            
            else:
                return response
    
    except Exception as err:
        print(err)
        return None
