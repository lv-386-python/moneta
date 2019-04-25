#import nose

from core.utils import  get_logger

def test_logger_name():
    logger = get_logger(__name__)
    assert logger.name == __name__

def test_logging_info():
    logger = get_logger(__name__)
    logger.info(f'test_message {__name__}')
    print(f'test_message {__name__}')

# if __name__ == "__main__":
#     nose.main()