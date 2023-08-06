import argparse
import os

from bbb_dlc.version import __version__
from bbb_dlc.bigbluebutton_api_python import BigBlueButton
from re import match

class BBBDLC:
    def run(args):
        bbb = BigBlueButton(args.server, args.secret)
        recordingParams = {
            "recordID": args.recordId,
        }

        try:
            ncCfg = open(args.ncCfg)
            ncPath = ""

            for line in ncCfg:
                line = match("^[\t ']+datadirectory[' =>]+([\/a-zA-Z.0-9]+)", line)
                if not line: continue

                ncPath = line.group(1)

            if ncPath == "": raise NameError('Could not find nextcloud config!')
            
            recordingUrl = bbb.get_recordings(recordingParams)
            recordingUrl = recordingUrl["xml"]["recordings"]["recording"]["playback"]["format"]["url"]
            passthroughArgs = ""

            for arg in vars(args):
                if arg == "recordId" or arg == "server" or arg == "secret" or arg == "ncCfg": continue
                if getattr(args, arg) == None or getattr(args, arg) == False: continue

                arg = arg.replace("_", "-")
                if arg == "encoder" or arg == "audiocodec": arg += " " +  str(getattr(args, arg))
                passthroughArgs += "--" + arg + " "

            passthroughArgs += recordingUrl
            os.system("cd " + ncPath + " & bbb-dl " + passthroughArgs)
        except Exception as e:
            print(e)
        

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser(
        description=('Big Blue Button Converter and Downloader')
    )

    parser.add_argument('ncCfg', type=str, help='Nextcloud cfg file')

    parser.add_argument('recordId', type=str, help='Recording ID of a lesson')

    parser.add_argument('server', type=str, help='BBB API Server')

    parser.add_argument('secret', type=str, help='BBB API Secret')

    parser.add_argument(
        '-aw',
        '--add-webcam',
        action='store_true',
        help='add the webcam video as an overlay to the final video',
    )

    parser.add_argument(
        '-aa',
        '--add-annotations',
        action='store_true',
        help='add the annotations of the professor to the final video',
    )

    parser.add_argument(
        '-kt',
        '--keep-tmp-files',
        action='store_true',
        help=('keep the temporary files after finish'),
    )

    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help=('print more verbose debug informations'),
    )
    parser.add_argument(
        '-ncc',
        '--no-check-certificate',
        action='store_true',
        help=('Suppress HTTPS certificate validation'),
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='bbb-dlc ' + __version__,
        help='Print program version and exit'
    )
    
    parser.add_argument(
        '--encoder',
        dest='encoder',
        type=str,
        default='libx264',
        help='Optional encoder to pass to ffmpeg (default libx264)',
    )
    parser.add_argument(
        '--audiocodec',
        dest='audiocodec',
        type=str,
        default='copy',
        help='Optional audiocodec to pass to ffmpeg (default copy the codec from the original source)',
    )

    parser.add_argument(
        '-f',
        '--filename',
        type=str,
        help='Optional output filename',
    )

    return parser


# --- called at the program invocation: -------------------------------------
def main(args=None):
    parser = get_parser()
    args = parser.parse_args(args)

    BBBDLC.run(args)