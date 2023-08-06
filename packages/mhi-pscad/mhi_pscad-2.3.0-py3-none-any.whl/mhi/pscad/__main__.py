"""
Print PSCAD Automation Library Version Information
"""
import mhi.common, mhi.pscad
from mhi.pscad.buildtime import BUILD_TIME

def main():
    print("MHI PSCAD Library v{} ({})".format(mhi.pscad.VERSION, BUILD_TIME))
    print("(c) Manitoba Hydro International Ltd.")
    print()
    print(mhi.common.version_msg())
    
if __name__ == '__main__':
    main()
