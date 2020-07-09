from instragramBot import InstagramBot
from absl import app, flags


def main(_):
    bot = InstagramBot('jondupond','Glybe25a!')
    bot.login()
    print(bot.search_for_tags(FLAGS.tag,FLAGS.limit, FLAGS.begin))

if __name__ == "__main__":
    FLAGS=flags.FLAGS
    flags.DEFINE_integer('limit', '10','limit of account we want to scrape')
    flags.DEFINE_string('tag','barbe','tab we want to scrap')
    flags.DEFINE_integer('begin','0','rank of the post we want to begin scrapping')
    app.run(main)