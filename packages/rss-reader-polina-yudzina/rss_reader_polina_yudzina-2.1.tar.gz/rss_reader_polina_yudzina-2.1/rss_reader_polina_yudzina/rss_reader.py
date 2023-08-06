""" Main module """
from rss_reader_polina_yudzina.main_functions import get_limit_news_collection, get_news, get_com_line_args, \
    create_logger, print_news
from rss_reader_polina_yudzina.validation_functions import check_url, check_version_arg, check_internet_connection, \
    check_emptiness
from rss_reader_polina_yudzina.exceptions import Error

def main():
    try:
        # get command line arguments
        com_line_args = get_com_line_args()

        logger = create_logger(com_line_args)

        if not check_version_arg(com_line_args, logger):
                # getting news from the internet
                check_internet_connection(logger)
                check_url(com_line_args, logger)

                news_collection = get_news(com_line_args, logger)
                check_emptiness(news_collection, logger)

                # account of --limit argument
                news_collection = get_limit_news_collection(news_collection, com_line_args, logger)

                print_news(news_collection, com_line_args, logger)
    except Error as e:
        print(e)


if __name__ == "__main__":
    main()
