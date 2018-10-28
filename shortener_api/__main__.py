import bottle

import shortener_api
import shortener_api.constants as constants

shortener_api.setup_application()

bottle.run(
    app=shortener_api.application,
    host=constants.HOST,
    port=constants.PORT,
    debug=constants.DEBUG,
    reloader=constants.RELOADER
)
