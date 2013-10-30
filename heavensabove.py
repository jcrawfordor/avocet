import requests
from lxml.html.soupparser import fromstring

"""Represents and provides utilities for a connection to the heavens-
above web service."""
class HAUtil:
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
        r = requests.get("http://heavens-above.com/{}&lat={}&lng={}&alt={}&tz={}".format(
            path, self.lat, self.lon, self.alt, self.tz))
        return fromstring(r.text)

"""Represents a satellite that heavens-above supports calculating passes
for. Contains utilities and the pass objects."""
class Satellite:
    def __init__(self, name, number, utils):
        """ Creates the object and sets its satellite name/number"""
        self.name = name
        self.number = number
        self.passes = []
        self.retrieve(utils)

    def retrieve(self, utils):
        """ Get this satellite's info from the web service """
        html = utils.request_page("PassSummary.aspx?satid={}".format(self.number))
        table_rows = html.xpath("//tr[contains(string(@class),\"clickableRow\")]")
        for row in table_rows:
            self.passes.append(Satellite_Pass(row))

    def __str__(self):
        output = """{0} ({1})
               Start            Peak             End
Date     Mag   Time     Al Az   Time     Al Az   Time     Al Az \n""".format(
            self.name, self.number)
        for time in self.passes:
            output += str(time)
        return output

""" Represents an instance of a satellite passing over, with times and
locations. """
class Satellite_Pass:
    def __init__(self, etree):
        """ Parses from subset of the HTML tree """
        cells = etree.findall('td')

        self.date = cells[0].text_content()
        self.mag  = cells[1].text_content()

        self.start = Satellite_Pass_Timeset(cells[2].text_content(),
            cells[3].text_content(), cells[4].text_content())
        self.peak = Satellite_Pass_Timeset(cells[5].text_content(),
            cells[6].text_content(), cells[7].text_content())
        self.end = Satellite_Pass_Timeset(cells[8].text_content(),
            cells[9].text_content(), cells[10].text_content())

    def __str__(self):
        return "{0: <7}  {1: <4}  {2}  {3}  {4}\n".format(self.date, self.mag,
            self.start, self.peak, self.end)

"""Represents a start, peak, or end time and position."""
class Satellite_Pass_Timeset:
    def __init__(self, time, alt, az):
        self.time = time
        self.alt = alt.replace(u'\xb0', '')
        self.az = az

    def __str__(self):
        """ Uses a total of 15 characters. """
        return "{0: <8} {1: <2} {2: <3}".format(self.time, self.alt, self.az)

class Iridium:
    def __init__(self, utils):
        self.flares = []
        self.retrieve(utils)

    def retrieve(self, utils):
        html = utils.request_page("IridiumFlares.aspx?")
        table_rows = html.xpath("//tr[contains(string(@class),\"clickableRow\")]")
        for row in table_rows:
            self.flares.append(Iridium_Flare(row))

    def __str__(self):
        output  = "Time             Mag   Al  Az         Satellite   Dst. Cntr.   CMag SAl\n"
        for flare in self.flares:
            output += str(flare)
        return output

class Iridium_Flare:
    def __init__(self, etree):
        cells = etree.findall('td')

        self.time = cells[0].text_content()
        self.mag = cells[1].text_content()
        self.alt = cells[2].text_content().replace(u'\xb0', '')
        self.az = cells[3].text_content().replace(u'\xb0', '')
        self.sat = cells[4].text_content()
        self.center_dist = cells[5].text_content()
        self.center_mag = cells[6].text_content()
        self.sun_alt = cells[7].text_content().replace(u'\xb0', '')

    def __str__(self):
        return "{0: <15}  {1: <4}  {2: <2} {3: <9}  {4: <10}  {5: <10} {6: <4} {7: <3}\n".format(
            self.time, self.mag, self.alt, self.az, self.sat, self.center_dist,
            self.center_mag, self.sun_alt)