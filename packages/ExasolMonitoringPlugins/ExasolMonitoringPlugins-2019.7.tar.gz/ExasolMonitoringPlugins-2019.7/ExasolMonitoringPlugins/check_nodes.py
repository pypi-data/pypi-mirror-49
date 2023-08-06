#!/usr/bin/python3
import ssl, json, time
from os.path            import isfile, getctime
from os                 import sep
from sys                import exit, argv, version_info, stdout, stderr
from getopt             import getopt
from xmlrpc.client      import ServerProxy
from urllib.parse       import quote_plus

pluginVersion           = "18.10"
hostName                = None
userName                = None
password                = None
opts, args              = None, None

try:
    opts, args = getopt(argv[1:], 'hVH:u:p:')

except:
    print("Unknown parameter(s): %s" % argv[1:])
    opts = []
    opts.append(['-h', None])

for opt in opts:
    parameter = opt[0]
    value     = opt[1]
    
    if parameter == '-h':
        print("""
EXAoperation XMLRPC nodes monitor (version %s)
  Options:
    -h                      shows this help
    -V                      shows the plugin version
    -H <license server>     domain of IP of your license server
    -u <user login>         EXAoperation login user
    -p <password>           EXAoperation login password
""" % (pluginVersion))
        exit(0)
    
    elif parameter == '-V':
        print("EXAoperation XMLRPC nodes monitor (version %s)" % pluginVersion)
        exit(0)

    elif parameter == '-H':
        hostName = value.strip()

    elif parameter == '-u':
        userName = value.strip()

    elif parameter == '-p':
        password = value.strip()

if not (hostName and userName and password):
    print('Please define at least the following parameters: -H -u -p')
    exit(4)

def XmlRpcCall(urlPath = ''):
    url = 'https://%s:%s@%s/cluster1%s' % (quote_plus(userName), quote_plus(password), hostName, urlPath)
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    sslcontext.verify_mode = ssl.CERT_NONE
    sslcontext.check_hostname = False
    return ServerProxy(url, context=sslcontext)

try:
    cluster = XmlRpcCall('/')
    storage = XmlRpcCall('/storage')

    notRunningNodes = {}
    nodeList = cluster.getNodeList()
    nodeStatesOutput = ''
    for node in nodeList:
        nodeState = cluster.getNodeState(node)['status']
        if nodeState != 'Running':
            notRunningNodes[node] = nodeState
            nodeStatesOutput += '\n%s: %s' % (node, nodeState)

    if len(notRunningNodes) > 0:
        print('CRITICAL - %i nodes online, %i nodes in other state |%s' % (
            len(nodeList) - len(notRunningNodes),
            len(notRunningNodes),
            nodeStatesOutput
        ))
        exit(2)
    else:
        print('OK - %i nodes online' % len(nodeList))
    exit(0)

except Exception as e:
    message = str(e).replace('%s:%s@%s' % (userName, password, hostName), hostName)
    if 'unauthorized' in message.lower():
        print('no access to EXAoperation: username or password wrong')

    elif 'Unexpected Zope exception: NotFound: Object' in message:
        print('database instance not found')

    else:
        print('UNKNOWN - internal error %s | ' % message.replace('|', '!').replace('\n', ';'))
    exit(3)
