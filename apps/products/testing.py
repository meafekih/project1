from django.core.files.uploadedfile import SimpleUploadedFile
import json
import pytest

def response_utf8_json(resp):
    return json.loads(resp.content.decode())


@pytest.mark.parametrize(
    'client,file_text,expected_first_line',
    (
            (None, u'Fake Data\nLine2\n', u'Fake Data'),
            # Try the fire emoji
            (None, u'\U0001F525\nLine2\nLine3\n', u'\U0001F525'),
    ),
    indirect=['client']
)
def test_upload(client, file_text, expected_first_line):
    query = '''
        mutation testMutation($file: Upload!) {
            UploadProductFile(file: $file) {
                success                
            }
        }
    '''

    t_file = SimpleUploadedFile(name='test.txt', content=file_text.encode('utf-8'))

    response = client.post(
        '/api',
        data={
            'operations': json.dumps({
                'query': query,
                'variables': {
                    'file': None,
                },
            }),
            't_file': t_file,
            'map': json.dumps({
                't_file': ['variables.file'],
            }),
        }
    )
    assert response.status_code == 200
    assert response_utf8_json(response) == {
        'data': {
            'UploadProductFile': {
                'success': True,
            },
        }
    }

