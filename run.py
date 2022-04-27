from pages.gen import generate_site

# example config
ROOT = '/Users/f/SITES/'
SOURCE = f'{ROOT}blocl-pages/'
TARGET = f'{ROOT}blocl/static'
TPL = f'{ROOT}blocl/blocl/templates'
EXT = ''
CTX = dict(
    site_name='Blocl',
    site_url='https://blocl.co'
)

if __name__ == '__main__':
    generate_site(SOURCE, TARGET, TPL, EXT, CTX)
