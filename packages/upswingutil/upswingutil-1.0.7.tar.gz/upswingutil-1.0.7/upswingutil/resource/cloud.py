import gcsfs
import pickle
import os
from loguru import logger
import upswingutil as ul


def get_model_from_cloud_storage(file_path, file_name, token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    filepath = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(filepath, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        logger.error(f'Unable to get model : {filepath}')
        logger.error(e)
        return None


def upload_model_to_cloud_storage(data, file_path, file_name, token=None):
    __G_CLOUD_PROJECT__ = os.getenv('G_CLOUD_PROJECT', ul.G_CLOUD_PROJECT)
    __secret__ = os.getenv('FIREBASE', ul.FIREBASE)
    filepath = f'{__G_CLOUD_PROJECT__}.appspot.com/{file_path}/{file_name}'
    try:
        if token:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=token)
        else:
            fs = gcsfs.GCSFileSystem(project=__G_CLOUD_PROJECT__, token=f"{__secret__}")

        with fs.open(filepath, 'wb') as f:
            f.write(bytes(data, 'utf-8'))
            return True
    except Exception as e:
        logger.error(f'Unable to write model : {filepath}')
        logger.error(e)
        return False


if __name__ == '__main__':
    # model = get_model_from_cloud_storage('revenue_forecast', 'revenue_forecast_11264.pkl')
    # result = model.forecast(10) if model else []
    # print(result)
    data = 'test'
    ul.G_CLOUD_PROJECT = 'aura-staging-31cae'
    ul.FIREBASE = '/Users/harsh/upswing/github/agent-oracle/SECRET/aura-staging-31cae-firebase-adminsdk-dyolr-7c135838e9.json'
    print(upload_model_to_cloud_storage(data, 'OHIPSB', 'test.txt'))
