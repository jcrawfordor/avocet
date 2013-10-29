import requests
from lxml.html.soupparser import fromstring

class HAUtil():
    """ Represents and provides utilities for a connection to the heavens-
    above web service."""
	def __init__(self, lat, lon, alt, tz):
		"""
        Sets important configuration data for connection.
        lat, lon    Observer position, latitude and longitude, decimal
        alt         Observer altitude, meters
        tz          Observer time zone, three-letter code
        """
        self.lat = lat
		self.lon = lon
		self.alt = alt
        self.tz = tz

    def request_page(self, path):
        r = requests.get("http://heavens-above.com/{}&lat={}&lon={}&alt={}&tz={}".format(
            path, self.lat, self.lon, self.alt, self.tz))
        return fromstring(r.text)

class Satellite():
    """ Represents a satellite that heavens-above supports calculating passes
    for. Contains utilities and the pass objects."""
    def __init__(self, name, number):
        """ Creates the object and sets its satellite name/number"""
        self.name = name
        self.number = number
        self.passes = []

    def retrieve(utils):
        """ Get this satellite's info from the web service """
        html = utils.request_page("PassSummary.aspx?satid={}".format(self.number))
        table_rows = html.xpath("//tr[contains(string(@class),\"clickableRow\")]")
        for row in table_rows:
            self.passes.append(Satellite_Pass(row))

    def __str__(self):
        output = """{0} ({1})\n
                       Start ---------  Peak ----------  End ----------\n
        Date     Mag   Time     Al Az   Time     Al Az   Time    Al Az \n""".format(
            self.name, self.number)
        for time in passes:
            output += str(time)
        output += "---------------------------------------------------------------"
        return output

class Satellite_Pass():
    """ Represents an instance of a satellite passing over, with times and
    locations. """
    def __init__(self, etree):
        """ Parses from subset of the HTML tree """
        cells = etree.findall('tr')

        self.date = cells[0].text_content()
        self.mag  = cells[1].text_content()

        self.start = Satellite_Pass_Timeset(cells[2].text_content(),
            cells[3].text_content(), cells[4].text_content())
        self.start = Satellite_Pass_Timeset(cells[5].text_content(),
            cells[6].text_content(), cells[7].text_content())
        self.start = Satellite_Pass_Timeset(cells[8].text_content(),
            cells[9].text_content(), cells[10].text_content())

    def __str__(self):
        return "{0: <7}  {1: <4}  {2}  {3}  {4}\n".format(self.date, self.mag,
            self.start, self.peak, self.end)

class Satellite_Pass_Timeset():
    """ Represents a start, peak, or end time and position. """
    def __init__(self, time, alt, az):
        self.time = time
        self.alt = alt
        self.az = az

    def __str__(self):
        """ Uses a total of 15 characters. """
        return "{0: <8} {1: <2} {2: <3}".format(self.time, self.alt, self.az)