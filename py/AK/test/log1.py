
import logbook

h1 = logbook.StderrHandler(bubble=True)

h1.push_application()


h2 = logbook.RotatingFileHandler("a.log",bubble=True)

h2.push_application()

logger = logbook.Logger("cli")

logger.debug("info")

 