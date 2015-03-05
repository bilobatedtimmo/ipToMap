"""
Based on code from Violent Python
"""

import dpkt
import socket
import pygeoip
import optparse
gi = pygeoip.GeoIP('/opt/GeoIp/Geo.dat')
def retKML(ips,ipd):
    try:
        srcrec = gi.record_by_name(ips)
        dstrec = gi.record_by_name(ipd)
        srclongitude = srcrec['longitude']
        srclatitude = srcrec['latitude']
        dstlongitude = dstrec['longitude']
        dstlatitude = dstrec['latitude']
        kml = (
            '<Placemark>\n'
              '<name>from %s to %s</name>\n'
              '<LineString>\n'
                '<extrude>1</extrude>\n'
                '<tessellate>1</tessellate>\n'
                '<coordinates>\n'
                  '%6f,%6f,0 %6f,%6f,0'
                '</coordinates>\n'
              '</LineString>\n'
            '</Placemark>\n'
           )%(ips, ipd, srclongitude, srclatitude, dstlongitude, dstlatitude)
        return kml
    except Exception, e:
        return ''
def plotIPs(pcap):
    kmlPts = ''
    for ts, buf in pcap:
        try:
            eth = dpkt.ethernet.Ethernet(buf)
            ip = eth.data
            src = socket.inet_ntoa(ip.src)
            dst = socket.inet_ntoa(ip.dst)
            src2dstKML = retKML(src,dst)
            kmlPts = kmlPts + src2dstKML
        except:
            pass
    return kmlPts
def main():
    parser = optparse.OptionParser('usage%prog -p <pcap file>')
    parser.add_option('-p', dest='pcapFile', type='string', help ='specify pcap filename')
    (options, args) = parser.parse_args()
    if options.pcapFile == None:
        print parser.usage
        exit(0)
    pcapFile = options.pcapFile
    f = open(pcapFile)
    pcap = dpkt.pcap.Reader(f)
    kmlheader = '<?xml version ="1.0" encoding="UTF-8"?>\
       \n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
    kmlfooter = '</Document>\n</kml>\n'
    kmldoc=kmlheader+plotIPs(pcap)+kmlfooter
    print kmldoc
if __name__=='__main__':
    main()
