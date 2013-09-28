import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('missions/duckling.cfg')

chapters = []

for section in config.sections():
	options = config.options(section)
	missions = []
	for option in options:
		missions.append( {option: config.get(section, option)} )
	chapters.append( {section: missions} )

return chapters




