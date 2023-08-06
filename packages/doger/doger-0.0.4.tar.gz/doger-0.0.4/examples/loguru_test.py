# *_*coding:utf-8 *_*
'''
Descri：
'''
import doger


if __name__ == '__main__':
    logger = doger.guru('INFO')
    logger.debug('This an debug log')
    logger.info('This an info log')
    logger.error('This an error log')